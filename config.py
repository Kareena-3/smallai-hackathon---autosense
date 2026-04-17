"""
Configuration, constants, enums, and threshold definitions.
"""

import logging
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ═══════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(threadName)-12s | %(name)-20s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('automotive_maintenance.log', encoding='utf-8')
    ]
)

# ═══════════════════════════════════════════════════════════════════════════
# PERFORMANCE TUNING
# ═══════════════════════════════════════════════════════════════════════════

MAX_WORKERS = 6
THREAD_TIMEOUT = 30
BATCH_SIZE = 10
CACHE_SIZE = 256
VEHICLE_BATCH_SIZE = 3


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════

class AlertLevel(Enum):
    """Vehicle health alert severity levels"""
    GREEN = "green"      # All systems normal
    YELLOW = "yellow"    # Warning - preventive service needed
    RED = "red"          # Critical - urgent service required


class ServicePriority(Enum):
    """Service scheduling priority"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AgentRole(Enum):
    """Agent types in the system"""
    MASTER = "master"
    DATA_ANALYSIS = "data_analysis"
    DIAGNOSIS = "diagnosis"
    ENGAGEMENT = "engagement"
    SCHEDULING = "scheduling"
    FEEDBACK = "feedback"
    QUALITY = "quality"


# ═══════════════════════════════════════════════════════════════════════════
# AUTOMOTIVE CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

VEHICLE_COMPONENTS = {
    "engine": {"interval_km": 100000, "cost": 50000},
    "brake_pads": {"interval_km": 50000, "cost": 3000},
    "oil_filter": {"interval_km": 10000, "cost": 500},
    "air_filter": {"interval_km": 30000, "cost": 800},
    "battery": {"interval_km": 80000, "cost": 8000},
    "tires": {"interval_km": 70000, "cost": 15000},
    "transmission": {"interval_km": 150000, "cost": 80000},
}

SENSOR_THRESHOLDS = {
    "engine_temp": {"min": 70, "max": 100, "critical_max": 110},
    "oil_pressure": {"min": 2.0, "max": 4.0, "critical_min": 1.5},
    "battery_voltage": {"min": 12.0, "max": 14.5, "critical_min": 11.5},
    "engine_rpm": {"min": 800, "max": 6500},
    "fuel_level": {"min": 0, "max": 100},
}

VEHICLE_MODELS = [
    "Maruti Swift", "Hyundai Creta", "Tata Nexon", "Mahindra XUV",
    "Kia Seltos", "Renault Duster", "Honda CRV", "Skoda Rapid"
]
