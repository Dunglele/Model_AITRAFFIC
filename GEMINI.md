# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC (Cập nhật 05/04/2026)

File này chứa các quy tắc, kiến trúc và thông tin ngữ cảnh quan trọng để vận hành và phát triển hệ thống phân tích giao thông thông minh Full-stack.

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Hệ thống phân tích giao thông đa tầng (Mật độ, Lưu lượng, Vận tốc) tích hợp Web Dashboard.
- **Nền tảng:** 
    - **AI Core:** YOLOv11 + Multi-Tracker (ByteTrack, StrongSORT, OC-SORT, Mask R-CNN).
    - **Web Hub:** Django Backend + REST API + Real-time Dashboard (Templates/React).
- **Công nghệ:** `django`, `djangorestframework`, `inference_sdk`, `supervision`, `chart.js`.

## 2. Kiến trúc Hệ thống (System Architecture)
Hệ thống hoạt động theo cơ chế tách biệt để tối ưu tài nguyên:
- **`traffic_platform.py`**: Nền tảng tổng hợp 4 chế độ phân tích (fast, stable, motion, mask).
- **Django Server**: Quản lý Database, cung cấp API và hiển thị Dashboard.
- **`update_traffic` Command**: Bộ phận cào ảnh tự động từ website giao thông, tích hợp AI để cập nhật dữ liệu thời gian thực vào Database.

## 3. Chỉ dẫn quan trọng cho AI (AI Instructions)
- **Xử lý Thời gian thực:** Sử dụng lệnh `python manage.py update_traffic` để duy trì luồng dữ liệu "sống". Tuyệt đối giữ nguyên bộ Headers/Cookies để tránh lỗi 403 Forbidden.
- **Tối ưu RAM:** Duy trì cơ chế `gc.collect()` và giới hạn lịch sử biểu đồ (`limit 20`) để tránh treo trình duyệt và server.
- **AI Precision:** Mặc định sử dụng ngưỡng `confidence = 0.2` cho ảnh Snapshot để tối đa hóa khả năng phát hiện phương tiện.
- **Bảo mật:** Không bao giờ lưu API Key trực tiếp vào code; luôn sử dụng biến môi trường từ `.env`.

## 4. Quy ước phát triển (Conventions)
- **Dữ liệu:** Mọi chỉ số mật độ phải tính theo chuẩn **PCE (Passenger Car Equivalent)**.
- **Giao diện:** Tuân thủ phong cách **Glassmorphism** (Stitch UI): Nền tối, hiệu ứng mờ, màu Neon Cyan chủ đạo.
- **API:** Các endpoint API phải bắt đầu bằng `/api/` và trả về định dạng JSON chuẩn.

## 5. Lộ trình phát triển (Roadmap)
- [x] Giai đoạn 1: Hoàn thiện AI Core (Multi-model support).
- [x] Giai đoạn 2: Xây dựng Django Backend, API và Dashboard cơ bản.
- [x] Giai đoạn 3: Tích hợp bộ cào ảnh tự động & AI Real-time Update.
- [ ] Giai đoạn 4: Triển khai Frontend React hoàn chỉnh & Bản đồ nhiệt (Heatmap).

## 6. Lệnh quan trọng (Key Commands)
- **Khởi động Web:** `./env/bin/python3 manage.py runserver`
- **Khởi động AI Crawler:** `./env/bin/python3 manage.py update_traffic`
- **Chạy Platform đơn lẻ:** `./env/bin/python3 traffic_platform.py --mode fast`
- **Dọn dẹp DB:** `./env/bin/python3 cleanup_db.py` (nếu có nhân bản).
