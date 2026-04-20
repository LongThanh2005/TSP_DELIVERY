import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import time
import io
import math
from sa_solver import SimulatedAnnealingTSP, haversine

# Cấu hình trang - Phong cách hiện đại
st.set_page_config(
    page_title="TSP Solver - Delivery Master",
    page_icon="🚚",
    layout="wide",
)

# Tùy chỉnh CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stRadio > div {
        flex-direction: row;
        gap: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Dữ liệu mặc định
DEFAULT_WARDS = [
    {"name": "Bến Nghé (Q1)", "lat": 10.776, "lon": 106.701},
    {"name": "Thảo Điền (TĐ)", "lat": 10.804, "lon": 106.738},
    {"name": "P.7 (Phú Nhuận)", "lat": 10.796, "lon": 106.685},
    {"name": "P.1 (Bình Thạnh)", "lat": 10.793, "lon": 106.697},
    {"name": "P.13 (Tân Bình)", "lat": 10.802, "lon": 106.643},
    {"name": "P.4 (Q.4)", "lat": 10.758, "lon": 106.702},
    {"name": "P.1 (Q.5)", "lat": 10.758, "lon": 106.671},
    {"name": "P.12 (Q.10)", "lat": 10.777, "lon": 106.666},
    {"name": "Tân Thuận Đông (Q.7)", "lat": 10.754, "lon": 106.723},
    {"name": "P.6 (Q.3)", "lat": 10.783, "lon": 106.694},
    {"name": "P.10 (Q.11)", "lat": 10.767, "lon": 106.653},
    {"name": "Đa Kao (Q.1)", "lat": 10.788, "lon": 106.698},
    {"name": "Bình An (TĐ)", "lat": 10.787, "lon": 106.721},
    {"name": "Linh Tây (TĐ)", "lat": 10.855, "lon": 106.757}
]

def main():
    st.title("🚚 Master Delivery - Tối ưu hóa lộ trình")
    st.subheader("Giải pháp di chuyển thông minh cho người giao hàng")

    # Khởi tạo session state
    if 'history' not in st.session_state:
        st.session_state.history = None
    if 'best_dist' not in st.session_state:
        st.session_state.best_dist = None

    # Sidebar - Cấu hình tham số
    with st.sidebar:
        st.header("📍 Cấu hình lộ trình")
        ward_names = [w["name"] for w in DEFAULT_WARDS]
        start_ward_name = st.selectbox("Điểm xuất phát (Vị trí hiện tại)", ward_names)
        start_index = ward_names.index(start_ward_name)

        st.divider()
        st.header("⚙️ Tham số tối ưu")
        t0 = st.slider("Nhiệt độ (T0)", 10.0, 500.0, 100.0)
        alpha = st.slider("Hệ số giảm nhiệt", 0.9, 0.9999, 0.999, 0.0001)
        max_iter = st.number_input("Số vòng lặp", 1000, 500000, 50000)
        
        if st.button("🚀 Tối ưu hóa toàn bộ lộ trình"):
            run_optimization_all(t0, alpha, max_iter, start_index)

        # Chỉ hiển thị nút tải về nếu có kết quả
        if st.session_state.history:
            st.divider()
            st.info("💡 Bạn có thể tải lộ trình dưới dạng CSV.")
            csv_data = generate_csv_all(st.session_state.history[-1]["route"])
            st.download_button("📥 Tải lộ trình (CSV)", csv_data, "route.csv", "text/csv")

    # Bố cục chính
    col_map, col_list = st.columns([2, 1])

    with col_map:
        st.markdown("### 🗺️ Bản đồ hiển thị")
        if st.session_state.history:
            show_final_map_all(st.session_state.history[-1]["route"], start_index)
        else:
            show_initial_map(start_index)

    with col_list:
        st.markdown("### 📋 Lịch trình chi tiết")
        if st.session_state.history:
            route_indices = st.session_state.history[-1]["route"]
            st.metric("Tổng quãng đường", f"{st.session_state.best_dist:.3f} km")
            for i, idx in enumerate(route_indices):
                ward = DEFAULT_WARDS[idx]
                if i == 0: st.success(f"**Bắt đầu:** {ward['name']}")
                else: st.write(f"{i}. {ward['name']}")
            st.info(f"Kết thúc tại **{DEFAULT_WARDS[route_indices[0]]['name']}**")
        else:
            st.info("Vui lòng cấu hình các tham số và nhấn nút 'Tối ưu hóa' để xem lộ trình.")

def show_initial_map(start_index):
    m = folium.Map(location=[10.78, 106.70], zoom_start=13)
    for i, ward in enumerate(DEFAULT_WARDS):
        if i == start_index:
            folium.Marker([ward["lat"], ward["lon"]], tooltip="XUẤT PHÁT", icon=folium.Icon(color='green', icon='home')).add_to(m)
        else:
            folium.Marker([ward["lat"], ward["lon"]], tooltip=ward["name"]).add_to(m)
    st_folium(m, width="100%", height=600, key="init_map")

def show_final_map_all(route_indices, start_index):
    lats = [DEFAULT_WARDS[i]["lat"] for i in route_indices]
    lons = [DEFAULT_WARDS[i]["lon"] for i in route_indices]
    m = folium.Map(location=[sum(lats)/len(lats), sum(lons)/len(lons)], zoom_start=13)
    
    # Vẽ các điểm
    for i, idx in enumerate(route_indices):
        ward = DEFAULT_WARDS[idx]
        color = 'green' if i == 0 else 'red'
        icon = 'home' if i == 0 else 'info-sign'
        folium.Marker([ward["lat"], ward["lon"]], tooltip=f"{i}. {ward['name']}", icon=folium.Icon(color=color, icon=icon)).add_to(m)

    # Vẽ đường
    coords = [[DEFAULT_WARDS[i]["lat"], DEFAULT_WARDS[i]["lon"]] for i in route_indices]
    coords.append(coords[0])
    folium.PolyLine(coords, color="#007bff", weight=4, opacity=0.8).add_to(m)
    
    m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])
    st_folium(m, width="100%", height=600, key="res_map_all")

def run_optimization_all(t0, alpha, max_iter, start_index):
    solver = SimulatedAnnealingTSP(DEFAULT_WARDS, t0=t0, alpha=alpha, max_iter=max_iter, start_index=start_index)
    with st.spinner("🚀 Đang tối ưu hóa 14 địa điểm..."):
        history, best_dist = solver.solve(record_interval=200)
    st.session_state.history = history
    st.session_state.best_dist = best_dist
    st.rerun()

def generate_csv_all(route_indices):
    data = []
    for i, idx in enumerate(route_indices):
        ward = DEFAULT_WARDS[idx]
        data.append({"No": i if i > 0 else "START", "Ward": ward["name"], "Lat": ward["lat"], "Lon": ward["lon"]})
    output = io.StringIO()
    pd.DataFrame(data).to_csv(output, index=False)
    return output.getvalue()

if __name__ == "__main__":
    main()
