# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC (Cập nhật 06/04/2026)

File này chứa các quy tắc, kiến trúc và thông tin ngữ cảnh quan trọng để vận hành và phát triển hệ thống phân tích giao thông thông minh Full-stack v3.0.

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Hệ thống phân tích giao thông đa tầng (Mật độ, Lưu lượng, Vận tốc) tích hợp Web Dashboard & Live Heatmap.
- **Nền tảng:** 
    - **AI Core:** YOLOv11 + Multi-Tracker (ByteTrack, StrongSORT, OC-SORT, Mask R-CNN).
    - **Web Hub:** Django Backend + REST API + Real-time Dashboard (Light Theme).
    - **Video Standard:** Sử dụng định dạng **WebM (Codec VP80)** để đảm bảo khả năng hiển thị 100% trên trình duyệt.

## 2. Kiến trúc Hệ thống (System Architecture)
Hệ thống hoạt động theo cơ chế tách biệt để tối ưu tài nguyên:
- **`traffic_platform.py`**: Nền tảng tổng hợp 4 chế độ phân tích. Hỗ trợ xuất tiến trình (`--progress`) để Frontend hiển thị thanh xử lý.
- **Django Dashboard**: 
    - `/`: Trang chủ Demo (Upload & Real-time Progress Bar).
    - `/map/`: Live Heatmap toàn thành phố.
    - `/demo/result/<id>/`: Trang kết quả video đã qua xử lý bởi AI.

## 3. Chỉ dẫn quan trọng cho AI & Developer
- **Video Output:** Luôn ưu tiên xuất tệp đuôi `.webm` với codec `VP80` cho các tính năng Web.
- **Xử lý Thời gian thực:** Duy trì `python manage.py update_traffic`. Cơ chế tự động dọn ảnh cũ đã được tích hợp để tránh đầy bộ nhớ.
- **Tối ưu RAM:** Luôn duy trì `gc.collect()` và giới hạn biểu đồ (max 20 điểm) để tránh treo server.
- **Bảo mật:** Không bao giờ lưu API Key trực tiếp vào code; luôn sử dụng biến môi trường từ `.env`.

## 4. Quy ước phát triển (Conventions)
- **Giao diện:** Tuân thủ phong cách **Light Theme** (Trắng/Xanh dương), Soft Shadows, Modern Typography.
- **Dữ liệu:** Mọi chỉ số mật độ phải tính theo chuẩn **PCE** hoặc **Pixel Density**.
- **API:** Các endpoint API phải trả về định dạng JSON chuẩn cho AJAX/Polling.

## 5. Lộ trình phát triển (Roadmap)
- [x] Giai đoạn 1: Hoàn thiện AI Core (Multi-model).
- [x] Giai đoạn 2: Xây dựng Django Backend & API.
- [x] Giai đoạn 3: Tích hợp bộ cào ảnh tự động (403 Fixed).
- [x] Giai đoạn 4: Hoàn thiện Dashboard, Live Heatmap & Video Demo Progress.
- [ ] Giai đoạn 5: Tích hợp Local Inference & Alert System.

## 6. Lệnh quan trọng (Key Commands)
- **Khởi động Web:** `./env/bin/python3 manage.py runserver`
- **Khởi động AI Crawler:** `./env/bin/python3 manage.py update_traffic`
- **Đồng bộ Git:** `git add . && git commit -m "..." && git push origin main`
