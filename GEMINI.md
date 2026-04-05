# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC

File này chứa các quy tắc và thông tin ngữ cảnh quan trọng để hỗ trợ phát triển dự án phân tích giao thông Model_AITRAFFIC.

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Phát hiện, đếm và theo dõi (tracking) các phương tiện giao thông.
- **Luồng xử lý:** Ảnh/Video -> Roboflow API (YOLO) -> Detections -> DeepSORT -> Visualization.
- **Công nghệ chính:** `inference_sdk` (Roboflow), `deep_sort_realtime`, `supervision`, `cv2`.

## 2. Chỉ dẫn quan trọng cho AI (AI Instructions)
- **Bảo mật:** Không bao giờ in hoặc lưu thêm các API Key của Roboflow vào code mới. Nếu thấy `api_key` trong code, hãy đề xuất chuyển sang dùng biến môi trường hoặc file `.env`.
- **Thực thi Notebook:** Luôn ưu tiên việc chuyển đổi logic từ `Yolo_Model.ipynb` sang script Python (`.py`) để dễ bảo trì và chạy trong môi trường CLI.
- **Xử lý thư viện:** Khi làm việc với OpenCV (`cv2`), hãy lưu ý các lỗi về `ModuleNotFoundError`. Luôn kiểm tra sự tồn tại của file ảnh trước khi dùng `cv2.imread`.
- **Tối ưu hóa Tracking:** Khi tinh chỉnh DeepSORT, tập trung vào tham số `max_age` và `n_init` để giảm thiểu việc mất ID của phương tiện khi bị che khuất.

## 3. Quy ước phát triển (Conventions)
- **Định dạng dữ liệu:** Sử dụng thư viện `supervision` để chuẩn hóa kết quả từ Roboflow trước khi đưa vào tracker.
- **Ghi chú Code:** Mọi hàm mới phải có docstring giải thích tham số đầu vào/đầu ra (ưu tiên tiếng Việt hoặc tiếng Anh chuyên ngành).
- **Visualization:** Các hộp nhận diện (bounding boxes) cần có nhãn ID và độ tự tin (confidence score).

## 4. Lệnh quan trọng (Key Commands)
- **Cài đặt môi trường:**
  ```bash
  pip install opencv-python supervision inference-sdk deep-sort-realtime
  ```
- **Chạy Workflow Roboflow:** Sử dụng `CLIENT.run_workflow` cho các tác vụ phức tạp (đếm, vẽ tự động trên server).

## 5. Danh sách việc cần làm (TODO)
- [x] Bảo mật hóa API Key (sử dụng `.env`).
- [x] Xây dựng script `main.py` để xử lý video thay vì chỉ ảnh tĩnh.
- [x] Tích hợp logic đếm phương tiện theo vùng (Zone Counting) bằng `supervision`.
