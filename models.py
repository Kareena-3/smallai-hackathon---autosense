"""
Data models (dataclasses) for vehicles, sensors, maintenance, appointments, etc.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Any

from config import AlertLevel, ServicePriority


# ═══════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SensorData:
    """Real-time vehicle sensor readings"""
    vehicle_id: str
    timestamp: str
    engine_rpm: float
    engine_temp: float
    oil_pressure: float
    battery_voltage: float
    mileage: float
    fuel_level: float
    tire_pressure: List[float]
    acceleration: float = 0.0
    brake_intensity: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MaintenanceRecord:
    """Historical maintenance log"""
    vehicle_id: str
    service_date: str
    service_type: str
    cost: float
    mileage: float
    components_replaced: List[str]
    duration_minutes: int
    technician: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PredictedFailure:
    """ML-predicted component failure"""
    vehicle_id: str
    component: str
    failure_probability: float
    estimated_days: int
    estimated_km: int
    severity: AlertLevel
    recommendation: str
    priority: ServicePriority

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ServiceAppointment:
    """Scheduled service appointment"""
    appointment_id: str
    vehicle_id: str
    customer_name: str
    customer_phone: str
    appointment_date: str
    appointment_time: str
    service_center: str
    estimated_duration_minutes: int
    predicted_failures: List[str]
    estimated_cost: float
    status: str = "confirmed"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentBehavior:
    """UEBA: Track agent behavior for security"""
    agent_name: str
    agent_role: str
    timestamp: str
    action_type: str
    resource_accessed: str
    data_sensitivity: str
    anomaly_score: float = 0.0
    is_anomalous: bool = False
    alert_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RCAInsight:
    """RCA/CAPA insight for manufacturing team"""
    insight_id: str
    defect_pattern: str
    frequency: int
    affected_vehicles: List[str]
    root_cause: str
    corrective_action: str
    affected_models: List[str]
    priority: str
    estimated_cost_saved: float
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CustomerFeedback:
    """Post-service customer feedback"""
    feedback_id: str
    vehicle_id: str
    appointment_id: str
    satisfaction_score: int       # 1-10
    service_quality: int          # 1-5
    technician_behavior: int      # 1-5
    would_recommend: bool
    issues_resolved: bool
    additional_issues_found: List[str]
    feedback_date: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
