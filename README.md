# Master Delivery - Route Optimizer 🚚

A smart delivery route optimization tool for Ho Chi Minh City using the **Simulated Annealing** algorithm. This project helps delivery drivers find the most efficient path between multiple wards in HCMC.

## 🌟 Features
- **Smart Optimization**: Calculates the shortest route for 14+ delivery locations.
- **Interactive Maps**: Real-time visualization using Folium and OpenStreetMap.
- **Modern UI**: Sleek, responsive dashboard built with Streamlit.
- **Flexible Backend**: FastAPI-powered solver integration.
- **Data Export**: Export optimized routes to CSV format.

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Mapping**: [Folium](https://python-visualization.github.io/folium/)
- **Algorithm**: Simulated Annealing (Metaheuristic)
- **Visualization**: Plotly, Pandas

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd "Dự án AI"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To launch the interactive dashboard:
```bash
streamlit run backend/ui.py
```

To run the FastAPI backend (optional):
```bash
uvicorn backend.main:app --reload
```

## 📍 Algorithm Details
The project uses the **Simulated Annealing** algorithm with a **2-opt swap** neighbor function to efficiently solve the Traveling Salesman Problem (TSP) for delivery points.
