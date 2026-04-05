import cv2
import os
import argparse
import supervision as sv
from inference_sdk import InferenceHTTPClient
from deep_sort_realtime.deepsort_tracker import DeepSort
import torch
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
from dotenv import load_dotenv
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gc
import csv

# 1. Load config
load_dotenv()
API_KEY = os.getenv("ROBOFLOW_API_KEY")
CLIENT = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=API_KEY)

# He so PCE
PCE_MAP = {"motorbike": 0.5, "car": 1.0, "truck": 2.5, "bus": 3.0, "van": 1.5}

def get_traffic_level(occupancy):
    if occupancy < 30: return "Thong thoang"
    if occupancy < 70: return "Trung binh"
    return "Tac nghen"

def process_video(source_path, output_path, mode="fast", model_id="annonate_datatftphcm/1"):
    print(f"\n--- KHOI DONG CHE DO: {mode.upper()} ---")
    video_info = sv.VideoInfo.from_video_path(source_path)
    
    # Cau hinh dac thu cho tung Mode
    if mode == "mask":
        TARGET_WIDTH = 320
        stride = 15
        weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
        mask_model = maskrcnn_resnet50_fpn(weights=weights, progress=False).eval()
        for param in mask_model.parameters(): param.requires_grad = False
        tracker = sv.ByteTrack()
    else:
        TARGET_WIDTH = 640
        stride = 5
        if mode == "fast":
            tracker = sv.ByteTrack()
        elif mode == "motion":
            tracker = sv.ByteTrack(track_activation_threshold=0.25, lost_track_buffer=30)
        elif mode == "stable":
            tracker = DeepSort(max_age=15, nn_budget=50, embedder="mobilenet", embedder_gpu=False)

    scale = TARGET_WIDTH / video_info.width
    target_height = int(video_info.height * scale)
    new_video_info = sv.VideoInfo(width=TARGET_WIDTH, height=target_height, fps=video_info.fps, total_frames=video_info.total_frames)
    
    polygon = np.array([[0, target_height], [int(TARGET_WIDTH*0.1), int(target_height*0.3)], [int(TARGET_WIDTH*0.9), int(target_height*0.3)], [TARGET_WIDTH, target_height]])
    road_area = cv2.contourArea(polygon.astype(np.int32))
    zone = sv.PolygonZone(polygon=polygon)
    
    analytics_data = []
    unique_ids = set()
    last_det = sv.Detections.empty()
    
    mask_annotator = sv.MaskAnnotator()
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.GREEN, thickness=1)

    def callback(frame, index):
        nonlocal last_det
        fr = cv2.resize(frame, (TARGET_WIDTH, target_height))
        
        if index % stride == 0:
            temp = "t_u.jpg"
            cv2.imwrite(temp, fr)
            res = CLIENT.infer(temp, model_id=model_id)
            preds = res.get('predictions', [])
            if isinstance(preds, dict):
                all_p = []
                for k, v in preds.items():
                    for p in v: p['class'] = k; all_p.append(p)
                preds = all_p
            
            yolo_det = sv.Detections.from_inference({"predictions": preds, "image": {"width": TARGET_WIDTH, "height": target_height}})
            
            if mode == "stable":
                ds_det = []
                if 'class_name' in yolo_det.data:
                    for xyxy, conf, cls in zip(yolo_det.xyxy, yolo_det.confidence, yolo_det.data['class_name']):
                        ds_det.append(([xyxy[0], xyxy[1], xyxy[2]-xyxy[0], xyxy[3]-xyxy[1]], conf, cls))
                tracks = tracker.update_tracks(ds_det, frame=fr)
                tx, ti, tc = [], [], []
                for t in tracks:
                    if t.is_confirmed(): tx.append(t.to_ltrb()); ti.append(t.track_id); tc.append(t.get_det_class())
                last_det = sv.Detections(xyxy=np.array(tx), tracker_id=np.array(ti), class_id=np.array([0]*len(ti)), data={'class_name': np.array(tc)}) if tx else sv.Detections.empty()
            elif mode == "mask":
                img_t = torch.from_numpy(fr).permute(2, 0, 1).float().div(255)
                with torch.inference_mode(): outputs = mask_model([img_t])[0]
                m_idx = np.where(outputs['scores'].cpu().numpy() > 0.5)[0]
                if len(m_idx) > 0:
                    det = sv.Detections(xyxy=outputs['boxes'][m_idx].cpu().numpy(), class_id=outputs['labels'][m_idx].cpu().numpy(), confidence=outputs['scores'][m_idx].cpu().numpy(), mask=(outputs['masks'][m_idx] > 0.5).cpu().numpy().squeeze(1))
                    det = det[np.isin(det.class_id, [3, 4, 6, 8])]
                    last_det = tracker.update_with_detections(detections=det)
                else: last_det = sv.Detections.empty()
            else: # fast & motion
                last_det = tracker.update_with_detections(detections=yolo_det)

        # Logic chung
        mask = zone.trigger(detections=last_det)
        det_in = last_det[mask]
        curr_pce = 0
        if not det_in.is_empty():
            if mode == "mask" and det_in.mask is not None:
                curr_pce = np.sum(det_in.mask) / 150 # Quy doi pixel mask sang score
            elif 'class_name' in det_in.data:
                for cls, tid in zip(det_in.data['class_name'], det_in.tracker_id):
                    curr_pce += PCE_MAP.get(cls, 1.0)
                    unique_ids.add(tid)
            elif det_in.tracker_id is not None:
                curr_pce += len(det_in.tracker_id) # Fallback
                for tid in det_in.tracker_id: unique_ids.add(tid)

        occ = min((curr_pce * 15000 / road_area) * 100 if mode != "mask" else (curr_pce*100/road_area)*100, 100.0)
        level = get_traffic_level(occ)
        if index % int(video_info.fps) == 0: analytics_data.append({"time": index // int(video_info.fps), "density": occ})

        # Render
        annotated = fr.copy()
        if mode == "mask" and not last_det.is_empty(): annotated = mask_annotator.annotate(scene=annotated, detections=last_det)
        else: annotated = box_annotator.annotate(scene=annotated, detections=last_det)
        
        annotated = zone_annotator.annotate(scene=annotated)
        cv2.putText(annotated, f"{mode.upper()} | D: {occ:.1f}% ({level})", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        return annotated

    generator = sv.get_video_frames_generator(source_path=source_path)
    with sv.VideoSink(target_path=output_path, video_info=new_video_info, codec="MJPG") as sink:
        for index, frame in enumerate(tqdm(generator, total=video_info.total_frames, desc=f"Running {mode}")):
            sink.write_frame(frame=callback(frame, index))
            if index % 10 == 0: gc.collect() 
    
    # Export Chart
    df = pd.DataFrame(analytics_data)
    if not df.empty:
        plt.figure(figsize=(10, 4)); plt.plot(df['time'], df['density'], marker='o', label=f'{mode} density'); plt.title(f"Analytics - {mode}"); plt.savefig(f"chart_{mode}.png")
    print(f"\n--- SUCCESS: {output_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--mode', type=str, default='fast', choices=['fast', 'stable', 'motion', 'mask'])
    parser.add_argument('--output', type=str, default='result.avi')
    args = parser.parse_args()
    input_p = args.input if args.input else input("Input file: ")
    if os.path.exists(input_p): process_video(input_p, args.output, mode=args.mode)
