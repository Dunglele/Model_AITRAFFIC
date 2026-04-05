import os
import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ROBOFLOW_API_KEY")
CLIENT = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key=API_KEY)

PCE_MAP = {"motorbike": 0.5, "car": 1.0, "truck": 2.5, "bus": 3.0, "van": 1.5}

def analyze_image(image_path):
    """
    Phan tich anh voi nguong confidence 20%.
    """
    # Goi API voi tham so confidence bang 0.2
    # Luu y: InferenceHTTPClient su dung tham so confidence hoac tra ve toan bo roi ta loc
    result = CLIENT.infer(image_path, model_id="annonate_datatftphcm/1")
    
    predictions = result.get('predictions', [])
    if isinstance(predictions, dict):
        all_p = []
        for k, v in predictions.items():
            for p in v: p['class'] = k; all_p.append(p)
        predictions = all_p

    # Loc thu cong voi nguong 0.2 neu API khong loc san
    filtered_preds = [p for p in predictions if p.get('confidence', 0) >= 0.2]

    vehicle_count = len(filtered_preds)
    total_pce = 0
    for p in filtered_preds:
        total_pce += PCE_MAP.get(p.get('class', ''), 1.0)

    # Tinh toan mat do (Quy doi nhanh cho Snapshot)
    # 15000 pixel la dien tich gia dinh cho vung ROI tren anh 640x480
    density = min((total_pce * 8.0), 100.0) 
    
    traffic_level = "Thông thoáng"
    if density > 70: traffic_level = "Tắc nghẽn"
    elif density > 35: traffic_level = "Trung bình"

    return {
        "vehicle_count": vehicle_count,
        "density": round(density, 1),
        "traffic_level": traffic_level,
        "predictions": filtered_preds
    }
