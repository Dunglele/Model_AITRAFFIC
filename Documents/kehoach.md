# 🚀 KẾ HOẠCH PHÁT TRIỂN HỆ THỐNG GIAO THÔNG THÔNG MINH (SMART TRAFFIC ANALYTICS)

## 1. TẦM NHÌN DỰ ÁN
Xây dựng một nền tảng Web-based tích hợp AI, có khả năng phân tích đa dạng các chỉ số giao thông (Mật độ, Lưu lượng, Vận tốc) với khả năng tùy biến mô hình linh hoạt theo cấu hình máy chủ và nhu cầu người dùng.

---

## 2. KIẾN TRÚC HỆ THỐNG: PHÂN TẦNG LINH HOẠT (MODULAR AI ARCHITECTURE)

Hệ thống được thiết kế theo triết lý: **"Lõi mạnh mẽ - Mô-đun tùy chọn"**.

### A. Thành phần lõi (Core Engine) - Luôn chạy
*   **Detector:** YOLOv11 (via Roboflow API) - Đảm nhiệm nhận diện nhanh phương tiện.
*   **Pre-processor:** Resizing (640p/480p) & ROI Polygon Mask.
*   **Analytics Logic:** Tính toán PCE Density, Traffic Level & Frequency.

### B. Thành phần tùy chọn (Optional Modules) - Chạy độc lập theo yêu cầu
| Chế độ phân tích | Thành phần kết hợp | Ưu điểm | Mục tiêu sử dụng |
| :--- | :--- | :--- | :--- |
| **Tiêu chuẩn (Fast)** | ByteTrack | Cực nhanh, tốn ít RAM | Giám sát thời gian thực, camera đô thị. |
| **Nâng cao (Precision)** | OC-SORT | Chính xác khi xe chuyển hướng phức tạp | Ngã tư lớn, vòng xoay. |
| **Nghiên cứu (Mask)** | Mask R-CNN | Tính diện tích pixel thực tế 99% | Báo cáo khoa học, quy hoạch hạ tầng. |
| **An ninh (Deep)** | StrongSORT | Nhận diện lại xe bị che khuất lâu | Theo dõi đối tượng nghi vấn, xe vi phạm. |

---

## 3. LỘ TRÌNH TRIỂN KHAI (ROADMAP)

### Giai đoạn 1: Hoàn thiện Lõi AI & Local Script (ĐÃ HOÀN THÀNH ✅)
- [x] Tích hợp YOLO + ByteTrack ổn định.
- [x] Tính mật độ theo chuẩn PCE và phân loại mức độ kẹt.
- [x] Tối ưu hóa bộ nhớ (Memory Management) để chạy trên môi trường hạn chế.
- [x] Xuất báo cáo tự động (CSV & PNG).

### Giai đoạn 2: Tích hợp Backend Django (SẮP TỚI 🛠️)
- [ ] Xây dựng Model Database để lưu trữ `TrafficSession`, `VehicleLogs`.
- [ ] Thiết lập **Celery + Redis** để xử lý video bất đồng bộ (ngăn lỗi timeout web).
- [ ] Viết API cho Dashboard (Django Rest Framework).

### Giai đoạn 3: Dashboard & Visualization
- [ ] Xây dựng giao diện Dashboard bằng Bootstrap 5.
- [ ] Tích hợp **Chart.js** để vẽ biểu đồ mật độ tương tác.
- [ ] Chức năng cho người dùng chọn "Chế độ phân tích" (Fast/Precision/Mask).

---

## 4. CHIẾN LƯỢC TỐI ƯU HÓA TÀI NGUYÊN (RESOURCE STRATEGY)

Để vận hành mượt mà trên Server (ví dụ: Render, AWS, Heroku):
1.  **Worker Isolation:** Tách biệt Server Web và Server AI.
2.  **Streaming Inference:** Gửi frame theo Stride (nhảy khung hình) để giảm chi phí API và RAM.
3.  **On-Demand Loading:** Chỉ tải mô hình (Weights) vào RAM khi chế độ đó được kích hoạt. Sau khi xử lý xong, giải phóng RAM ngay lập tức bằng `gc.collect()`.

---

## 5. KẾT LUẬN
Dự án hướng tới một hệ thống phân tích giao thông toàn diện, không bị gò bó bởi một thuật toán duy nhất. Việc kết hợp **YOLO + ByteTrack** làm lõi và các mô hình khác làm tùy chọn là giải pháp tối ưu nhất để cân bằng giữa **Hiệu năng**, **Tốc độ** và **Chi phí**.

---
*Người lập kế hoạch: Gemini CLI Agent*
*Ngày: 05/04/2026*
