from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from sa_solver import SimulatedAnnealingTSP

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ward(BaseModel):
    name: str
    lat: float
    lon: float

class OptimizeRequest(BaseModel):
    wards: List[Ward]
    t0: float = 100.0
    alpha: float = 0.999
    min_t: float = 0.01

# Dữ liệu mẫu (Phường tại TP.HCM)
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

@app.get("/wards")
def get_wards():
    return DEFAULT_WARDS

@app.post("/optimize")
def optimize(req: OptimizeRequest):
    wards_data = [w.dict() for w in req.wards]
    solver = SimulatedAnnealingTSP(
        wards_data, 
        t0=req.t0, 
        alpha=req.alpha, 
        min_t=req.min_t
    )
    
    # Chúng ta ghi lại mỗi 200 bước để animation mượt mà mà không làm nặng payload
    history, best_dist = solver.solve(record_interval=200)
    
    return {
        "best_dist": best_dist,
        "history": history
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
