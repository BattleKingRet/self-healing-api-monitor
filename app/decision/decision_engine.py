from collections import deque
from datetime import datetime, timedelta

class DecisionEngine:
    def __init__(
        self,
        confidence_threshold: float = 0.85,
        required_anomalies: int = 3,
        window_seconds: int = 120,
        cooldown_seconds: int = 300
    ):
        self.confidence_threshold = confidence_threshold
        self.required_anomalies = required_anomalies
        self.window = timedelta(seconds=window_seconds)
        self.cooldown = timedelta(seconds=cooldown_seconds)

        self.anomaly_history = deque()
        self.last_recovery_time = None

    def decide(self, detection: dict) -> str:
        now = datetime.utcnow()

        while self.anomaly_history and now - self.anomaly_history[0] > self.window:
            self.anomaly_history.popleft()

        if detection["is_anomaly"] and detection["confidence"] >= self.confidence_threshold:
            self.anomaly_history.append(now)

        if self.last_recovery_time and now - self.last_recovery_time < self.cooldown:
            return "MONITOR"

        if len(self.anomaly_history) >= self.required_anomalies:
            self.last_recovery_time = now
            self.anomaly_history.clear()
            return "RECOVER"

        return "MONITOR"
