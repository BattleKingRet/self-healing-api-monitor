from collections import deque
from statistics import mean, stdev

class AnomalyDetector:
    def __init__(self, window_size: int = 20, z_threshold: float = 3.0):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.latencies = deque(maxlen=window_size)
        self.error_rates = deque(maxlen=window_size)

    def detect(self, latency_ms: float, error_rate: float) -> dict:
        result = {
            "is_anomaly": False,
            "confidence": 0.0,
            "reason": None
        }

        # Not enough data yet
        if len(self.latencies) < self.window_size:
            self.latencies.append(latency_ms)
            self.error_rates.append(error_rate)
            return result

        latency_mean = mean(self.latencies)
        latency_std = stdev(self.latencies) or 1.0

        latency_z = abs((latency_ms - latency_mean) / latency_std)

        error_mean = mean(self.error_rates)
        error_std = stdev(self.error_rates) or 1.0

        error_z = abs((error_rate - error_mean) / error_std)

        max_z = max(latency_z, error_z)

        if max_z >= self.z_threshold:
            result["is_anomaly"] = True
            result["confidence"] = min(max_z / (self.z_threshold * 2), 1.0)
            result["reason"] = "latency" if latency_z > error_z else "error_rate"

        self.latencies.append(latency_ms)
        self.error_rates.append(error_rate)

        return result
