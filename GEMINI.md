# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC (Cập nhật 06/04/2026)

File này chứa các quy tắc, kiến trúc và thông tin ngữ cảnh quan trọng để vận hành và phát triển hệ thống phân tích giao thông thông minh Full-stack v2.5.

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Hệ thống phân tích giao thông đa tầng tích hợp Web Dashboard & Live Heatmap.
- **Nền tảng:** 
    - **AI Core:** YOLOv11 + Multi-Tracker (ByteTrack, StrongSORT, OC-SORT, Mask R-CNN).
    - **Web Hub:** Django Backend + REST API + Real-time Dashboard (Light Theme).
    - **Giao diện:** Modern UI với hệ thống Phân trang, Bộ lọc và Bản đồ nhiệt tương tác.

## 2. Kiến trúc Hệ thống (System Architecture)
- **`traffic_platform.py`**: Nền tảng AI tổng hợp hỗ trợ 4 chế độ (`fast`, `stable`, `motion`, `mask`).
- **Django Dashboard**: 
    - `/`: Trang chủ Demo (Upload & Preview video).
    - `/list/`: Danh sách Camera (Hỗ trợ tìm kiếm & Phân trang 12 item/trang).
    - `/map/`: Live Heatmap (Leaflet.js) hiển thị mật độ toàn thành phố.
    - `/camera/<id>/`: Chi tiết AI (Biểu đồ Chart.js mượt mà, giới hạn 20 điểm dữ liệu).

## 3. Chỉ dẫn quan trọng cho AI & Developer
- **Xử lý Thời gian thực:** Duy trì `python manage.py update_traffic`. Tuyệt đối giữ nguyên bộ Headers/Cookies để tránh lỗi 403.
- **Hiển thị Biểu đồ:** Để tránh lỗi phình chiều cao, container chứa `<canvas>` phải có `height` cố định và `maintainAspectRatio: false`.
- **Dữ liệu Biểu đồ:** Chỉ truyền 20 bản ghi mới nhất từ Backend (`history[:20]`) để tối ưu hiệu suất render.
- **Tọa độ:** Mỗi Camera mới phải có `latitude` và `longitude` để hiển thị trên bản đồ.

## 4. Quy ước phát triển (Conventions)
- **Giao diện:** Sử dụng **Light Theme** sạch sẽ, Soft Shadows, màu Primary là Blue (`#0d6efd`).
- **Dữ liệu:** Phân tích mật độ dựa trên chuẩn **PCE** (cho Bounding Box) và **Pixel Density** (cho Mask R-CNN).
- **Phân trang:** Mặc định chia trang ở mức 12 camera để đảm bảo tốc độ load ảnh.

## 5. Lộ trình phát triển (Roadmap)
- [x] Giai đoạn 1: Hoàn thiện AI Core (Multi-model).
- [x] Giai đoạn 2: Xây dựng Django Backend & API.
- [x] Giai đoạn 3: Tích hợp AI Real-time Update (403 Fixed).
- [x] Giai đoạn 4: Hoàn thiện Dashboard, Phân trang, Bộ lọc & Live Heatmap.
- [ ] Giai đoạn 5: Tích hợp hệ thống cảnh báo (Alerts) qua Email/Telegram khi có tắc nghẽn.

## 6. Lệnh quan trọng (Key Commands)
- **Khởi động Web:** `./env/bin/python3 manage.py runserver`
- **Khởi động AI Crawler:** `./env/bin/python3 manage.py update_traffic`
- **Khởi tạo tọa độ Demo:** `./env/bin/python3 init_coords.py`
- **Dọn dẹp Database:** `./env/bin/python3 cleanup_db.py`
