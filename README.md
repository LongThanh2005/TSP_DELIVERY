# 🚚 Hệ Thống Tối Ưu Hóa Đường Đi Giao Hàng (TSP Solver)

Chào mừng bạn đến với dự án **Master Delivery**! Đây là công cụ giúp các bác tài hoặc người giao hàng tìm ra lộ trình ngắn nhất khi phải đi qua nhiều địa điểm khác nhau trong Thành phố Hồ Chí Minh.

## 🌟 Dự án này có gì hay?
- **Tìm đường siêu nhanh**: Sử dụng thuật toán thông minh (Simulated Annealing) để tính toán đường đi ngắn nhất giữa 14+ địa điểm.
- **Bản đồ trực quan**: Bạn có thể nhìn thấy lộ trình của mình ngay trên bản đồ tương tác.
- **Dễ sử dụng**: Giao diện đơn giản, hiện đại, ai cũng có thể dùng được.
- **Xuất dữ liệu**: Tải lộ trình đã tối ưu về máy dưới dạng file Excel/CSV để tiện theo dõi.

## 📊 Kết quả thực nghiệm (SA vs Greedy NN)
Dưới đây là hiệu suất thực tế của thuật toán Simulated Annealing trên bộ dữ liệu 14 địa điểm mặc định:
- **Quãng đường tốt nhất (Min)**: 44.69 km
- **Quãng đường trung bình**: 44.77 km
- **Độ lệch chuẩn**: ±0.20 km (Cực kỳ ổn định)
- **So với Greedy NN**: Cải thiện **-9.58%** (từ 49.52 km xuống 44.77 km)
- **Thời gian xử lý trung bình**: ~0.13 giây
- **Tỷ lệ hội tụ**: 100% (50/50 lần chạy đều đạt kết quả tối ưu)

## 🛠️ Công nghệ sử dụng
- **Backend (Xử lý)**: FastAPI (Python)
- **Frontend (Giao diện)**: Streamlit
- **Bản đồ**: Folium
- **Dữ liệu**: Pandas, Plotly

## 🚀 Hướng dẫn cài đặt và chạy (Dành cho người mới)

### 1. Yêu cầu chuẩn bị
Máy tính của bạn cần cài sẵn **Python** (phiên bản 3.8 trở lên).

### 2. Cài đặt
Mở terminal (hoặc Command Prompt) và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Khởi động ứng dụng
Để mở giao diện web và bắt đầu sử dụng, bạn chạy lệnh:
```bash
streamlit run backend/ui.py
```
Sau khi chạy, ứng dụng sẽ tự động mở trên trình duyệt web của bạn.

## 📍 Cách sử dụng
1. Chọn **Điểm xuất phát** của bạn (Vị trí hiện tại).
2. Nhấn nút **Tối ưu hóa toàn bộ lộ trình** và đợi vài giây.
3. Xem lộ trình trên bản đồ và danh sách chi tiết bên cạnh.
4. (Tùy chọn) Nhấn **Tải lộ trình (CSV)** nếu muốn lưu lại.

---
*Chúc bạn có những chuyến giao hàng thuận lợi và nhanh chóng!*
