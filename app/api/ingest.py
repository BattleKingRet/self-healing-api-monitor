from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from app.core.logger import get_logger
from app.ml.anomaly_detector import AnomalyDetector
from app.decision.decision_engine import DecisionEngine
from app.recovery.executor import RecoveryExecutor

executor = RecoveryExecutor()

decision_engines = {}


detectors = {}


router = APIRouter()
logger = get_logger("metrics-ingest")


class MetricPayload(BaseModel):
    service: str
    latency_ms: float
    error_rate: float
    timestamp: datetime


@router.post("/metrics", status_code=status.HTTP_202_ACCEPTED)
def ingest_metrics(payload: MetricPayload):

    if payload.service not in detectors:
        detectors[payload.service] = AnomalyDetector()

    detector = detectors[payload.service]
    detection = detector.detect(
        latency_ms=payload.latency_ms,
        error_rate=payload.error_rate
    )

    if payload.service not in decision_engines:
        decision_engines[payload.service] = DecisionEngine()

    decision_engine = decision_engines[payload.service]
    decision = decision_engine.decide(detection)

    if detection["is_anomaly"]:
        logger.warning(
            "anomaly_detected service=%s confidence=%.2f reason=%s",
            payload.service,
            detection["confidence"],
            detection["reason"]
        )
    else:
        logger.info(
            "metrics_normal service=%s",
            payload.service
        )

    if decision == "RECOVER":
        executor.execute(payload.service, detection["reason"])
        logger.error(
            "recovery_approved service=%s confidence=%.2f",
            payload.service,
            detection["confidence"]
        )
    else:
        logger.info(
            "decision=%s service=%s",
            decision,
            payload.service
        )

    return {
        "message": "Metrics processed",
        "service": payload.service,
        "decision": decision,
        "anomaly": detection
    }

