# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC (Cập nhật 05/04/2026)

File này chứa các quy tắc, kiến trúc và thông tin ngữ cảnh quan trọng để tiếp tục phát triển hệ thống phân tích giao thông thông minh.

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Hệ thống phân tích giao thông đa tầng (Mật độ, Lưu lượng, Vận tốc).
- **Luồng xử lý:** Video -> Resize (480p/640p) -> YOLO Inference -> Tracker (ByteTrack/StrongSORT/OC-SORT) -> Analytics Logic (PCE/Mask) -> Visualization & Reports.
- **Công nghệ chính:** `inference_sdk`, `supervision`, `deep_sort_realtime`, `torchvision`, `pandas`, `matplotlib`.

## 2. Kiến trúc Mô-đun (Modular Architecture)
Hệ thống được thiết kế để chạy độc lập các chế độ phân tích nhằm tối ưu tài nguyên:
- **`main.py`**: Chế độ Tiêu chuẩn (Fast). Sử dụng **ByteTrack**. Phù hợp nhất cho Production/Web nhờ tốc độ cao và cực nhẹ RAM.
- **`ocsort.py`**: Chế độ Nâng cao (Motion Precision). Sử dụng **OC-SORT**. Tối ưu cho các tình huống chuyển động lắt léo, ngã tư phức tạp.
- **`strongsort.py`**: Chế độ Theo dõi Bền vững (Stable ID). Sử dụng **StrongSORT** với Appearance Features để giảm nhảy ID khi phương tiện bị che khuất.
- **`maskrcnn.py`**: Chế độ Nghiên cứu (Mask Segmentation). Sử dụng **Hybrid Mask R-CNN** để tính diện tích chiếm dụng thực tế theo từng pixel.

## 3. Chỉ dẫn quan trọng cho AI (AI Instructions)
- **Tối ưu RAM:** Luôn sử dụng `gc.collect()` và `stride` (nhảy khung hình) khi xử lý video dài để tránh lỗi "Terminated".
- **Xử lý Video:** Sử dụng codec `MJPG` và định dạng `.avi` để đảm bảo khả năng ghi file ổn định trên môi trường Linux/Codespace.
- **Dữ liệu:** Mọi kết quả phân tích phải được xuất ra cả hai định dạng: Ảnh biểu đồ (`.png`) và Dữ liệu thô (`.csv`).
- **Bảo mật:** Tuyệt đối không commit file `.env` chứa API Key lên Git.

## 4. Quy ước phát triển (Conventions)
- **Định dạng:** Mọi logic phân tích mật độ phải tuân theo chuẩn **PCE (Passenger Car Equivalent)** hoặc **Pixel-level Density**.
- **Tọa độ:** Vùng quan tâm (ROI) luôn được định nghĩa bằng `sv.PolygonZone` để đảm bảo tính linh hoạt khi thay đổi góc camera.
- **Thư mục:** Giữ các file báo cáo và kế hoạch trong thư mục `Documents/`.

## 5. Lộ trình phát triển (Roadmap)
- [x] Giai đoạn 1: Hoàn thiện AI Core & Multi-model support (ByteTrack, StrongSORT, Mask R-CNN, OC-SORT).
- [ ] Giai đoạn 2: Xây dựng Backend Django & Celery Worker.
- [ ] Giai đoạn 3: Dashboard hiển thị biểu đồ thời gian thực dùng WebSockets.

## 6. Lệnh quan trọng (Key Commands)
- **Chạy bản ByteTrack:** `./env/bin/python3 main.py`
- **Chạy bản OC-SORT:** `./env/bin/python3 ocsort.py`
- **Chạy bản StrongSORT:** `./env/bin/python3 strongsort.py`
- **Chạy bản Mask R-CNN:** `./env/bin/python3 maskrcnn.py`
- **Đồng bộ Git:** `git add . && git commit -m "..." && git push origin main`
## 7. Danh sách cần làm (TODO)