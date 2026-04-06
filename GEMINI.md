# GEMINI.md - Chỉ dẫn dự án Model_AITRAFFIC (Cập nhật 06/04/2026)

File này chứa các quy tắc, kiến trúc và thông tin ngữ cảnh quan trọng để vận hành và phát triển hệ thống phân tích giao thông thông minh Full-stack v3.5 (Final Release).

## 1. Tổng quan dự án (Project Overview)
- **Mục tiêu:** Hệ thống phân tích giao thông đa tầng tích hợp Web Dashboard & Live Heatmap chuyên nghiệp.
- **Nền tảng:** 
    - **AI Core:** YOLOv11 + Multi-Tracker (ByteTrack, StrongSORT, OC-SORT, Mask R-CNN).
    - **Web Hub:** Django Backend + REST API + Real-time Dashboard (Light Theme).
    - **Video Standard:** Sử dụng định dạng **WebM (Codec VP80)** để tương thích 100% với trình duyệt.

## 2. Kiến trúc Hệ thống (System Architecture)
- **`traffic_platform.py`**: Nền tảng AI tổng hợp hỗ trợ 4 chế độ. Tích hợp cơ chế xuất tiến độ (`--progress`).
- **Django Dashboard**: 
    - `/`: Trang chủ (Giới thiệu, Hướng dẫn & AI Demo Video).
    - `/list/`: Danh sách Camera (Tìm kiếm & Phân trang).
    - `/map/`: Live Heatmap tích hợp danh sách Điểm nóng (Hotspots).
    - `/camera/<id>/`: Chi tiết AI (Biểu đồ Chart.js 60 điểm dữ liệu, live polling).

## 3. Chỉ dẫn quan trọng cho AI & Developer
- **Mật độ chính xác:** Hệ thống sử dụng trường `road_area_pixels` trong Model `TrafficCamera` để tính mật độ. Developer cần hiệu chỉnh thông số này cho từng camera để đạt độ chính xác cao nhất.
- **Video Output:** Luôn ưu tiên tệp `.webm`. Codec `mp4v` được dùng làm dự phòng.
- **Xử lý Thời gian thực:** Duy trì lệnh `python manage.py update_traffic` để cập nhật dữ liệu.
- **Tối ưu RAM:** Duy trì cơ chế `gc.collect()` sau mỗi chu kỳ xử lý.

## 4. Quy ước phát triển (Conventions)
- **Giao diện:** Phong cách **Light Theme** hiện đại, sử dụng Bootstrap 5 và Soft Shadows.
- **Dữ liệu:** Phân tích mật độ dựa trên chuẩn **PCE** và **Diện tích lòng đường thực tế**.

## 5. Lộ trình phát triển (Roadmap)
- [x] Giai đoạn 1: Hoàn thiện AI Core (Multi-model).
- [x] Giai đoạn 2: Xây dựng Django Backend & API.
- [x] Giai đoạn 3: Tích hợp bộ cào ảnh tự động.
- [x] Giai đoạn 4: Hoàn thiện Dashboard, Heatmap & Progress Bar.
- [x] Giai đoạn 5: Tối ưu hóa giao diện (Light Theme) & Thuật toán diện tích thực tế.

## 6. Lệnh quan trọng (Key Commands)
- **Khởi động Web:** `./env/bin/python3 manage.py runserver`
- **Khởi động AI Crawler:** `./env/bin/python3 manage.py update_traffic`
- **Đồng bộ Git:** `git add . && git commit -m "..." && git push origin main`

## 7. Trạng thái To-do list (Hoàn thành 100%)
- [x] Tăng giới hạn biểu đồ lên 60 điểm.
- [x] Trang trí trang Index, giải thích mô hình, hướng dẫn sử dụng.
- [x] Trang trí toàn bộ các trang giao diện (Light Theme).
- [x] Tối ưu thuật toán đếm xe theo diện tích lòng đường từng ảnh.
- [x] Kiểm thử hệ thống không còn lỗi (v3.5).
