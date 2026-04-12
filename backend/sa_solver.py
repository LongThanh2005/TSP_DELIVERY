import math
import random

def haversine(coord1, coord2):
    """
    Tính khoảng cách giữa hai tọa độ (lat, lon) dùng công thức Haversine (km).
    """
    R = 6371  # Bán kính Trái Đất
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

class SimulatedAnnealingTSP:
    def __init__(self, wards, t0=100, alpha=0.9995, min_t=0.01, max_iter=100000, start_index=None):
        self.wards = wards  # List of dicts: {"name": "...", "lat": ..., "lon": ...}
        self.t = t0
        self.alpha = alpha
        self.min_t = min_t
        self.max_iter = max_iter
        self.start_index = start_index 
        
        # Lộ trình khởi tạo
        if self.start_index is not None:
            # Nếu có điểm xuất phát, cố định nó ở đầu và xáo trộn phần còn lại
            remaining = [i for i in range(len(wards)) if i != self.start_index]
            random.shuffle(remaining)
            self.current_route = [self.start_index] + remaining
        else:
            self.current_route = list(range(len(wards)))
            random.shuffle(self.current_route)
        
        self.best_route = self.current_route[:]
        self.current_dist = self.calculate_total_dist(self.current_route)
        self.best_dist = self.current_dist

    def calculate_total_dist(self, route):
        dist = 0
        for i in range(len(route)):
            ward1 = self.wards[route[i]]
            ward2 = self.wards[route[(i + 1) % len(route)]]
            dist += haversine((ward1["lat"], ward1["lon"]), (ward2["lat"], ward2["lon"]))
        return dist

    def get_neighbor(self, route):
        """
        Sử dụng 2-opt swap (đảo ngược một đoạn lộ trình).
        Điều này rất hiệu quả trong việc gỡ các nút thắt (đường chéo nhau).
        """
        new_route = route[:]
        # Chọn hai chỉ số ngẫu nhiên
        # Nếu có điểm bắt đầu cố định, ta không được phép chọn chỉ số 0
        start_range = 1 if self.start_index is not None else 0
        i, j = random.sample(range(start_range, len(route)), 2)
        
        if i > j:
            i, j = j, i
        # Đảo ngược đoạn từ i đến j
        new_route[i:j+1] = reversed(new_route[i:j+1])
        return new_route

    def solve(self, record_interval=100):
        """
        Chạy thuật toán và ghi lại các bước tiến triển.
        """
        history = []
        iteration = 0
        
        # Ghi lại trạng thái ban đầu
        history.append({
            "iteration": 0,
            "t": self.t,
            "dist": self.current_dist,
            "route": self.current_route[:]
        })

        while self.t > self.min_t and iteration < self.max_iter:
            new_route = self.get_neighbor(self.current_route)
            new_dist = self.calculate_total_dist(new_route)
            
            # Chấp nhận lời giải mới nếu tốt hơn, hoặc xác suất ngẫu nhiên nếu tệ hơn
            delta = new_dist - self.current_dist
            if delta < 0 or random.random() < math.exp(-delta / self.t):
                self.current_route = new_route
                self.current_dist = new_dist
                
                if self.current_dist < self.best_dist:
                    self.best_dist = self.current_dist
                    self.best_route = self.current_route[:]
            
            # Ghi lại lịch sử sau mỗi record_interval bước
            if iteration % record_interval == 0:
                history.append({
                    "iteration": iteration,
                    "t": self.t,
                    "dist": self.current_dist,
                    "route": self.current_route[:]
                })
            
            # Hạ nhiệt
            self.t *= self.alpha
            iteration += 1

        # Ghi lại kết quả cuối cùng
        history.append({
            "iteration": iteration,
            "t": self.t,
            "dist": self.best_dist,
            "route": self.best_route
        })
        
        return history, self.best_dist
