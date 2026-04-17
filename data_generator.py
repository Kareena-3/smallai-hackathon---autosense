"""
Synthetic data generation for vehicles, sensors, and maintenance history.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

from config import VEHICLE_COMPONENTS, VEHICLE_MODELS
from models import SensorData, MaintenanceRecord


class SyntheticDataGenerator:
    """Generate realistic synthetic vehicle and maintenance data"""

    @staticmethod
    def generate_vehicles(count: int = 10, region: str = "Delhi") -> Dict[str, Dict[str, Any]]:
        """Generate fleet of vehicles with profiles"""
        vehicles = {}
        regions = {"Delhi": "+91-11", "Mumbai": "+91-22", "Bangalore": "+91-80"}
        area_code = regions.get(region, "+91-11")

        for i in range(count):
            v_id = f"VEH_{region[:3].upper()}_{i+1:05d}"
            vehicles[v_id] = {
                "owner": f"Owner_{i+1}",
                "phone": f"{area_code}-{random.randint(20000000, 99999999)}",
                "model": random.choice(VEHICLE_MODELS),
                "year": random.randint(2018, 2024),
                "mileage": round(random.uniform(10000, 150000), 2),
                "last_service": (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat(),
                "registration": f"DL-{random.randint(1000, 9999)}-{random.choice('ABCDEFGH')}",
                "service_history_count": random.randint(2, 15),
                "warranty_status": random.choice(["Active", "Expired"])
            }
        return vehicles

    @staticmethod
    def generate_sensor_data(vehicle_id: str, anomaly_probability: float = 0.25) -> SensorData:
        """Generate realistic sensor readings with potential anomalies"""
        has_anomaly = random.random() < anomaly_probability

        if has_anomaly:
            rpm = random.uniform(3500, 6000)
            temp = random.uniform(95, 115)
            oil_pressure = random.uniform(0.5, 1.8)
            battery = random.uniform(11.0, 12.5)
            accel = random.uniform(0.5, 0.9)
        else:
            rpm = random.uniform(1000, 3500)
            temp = random.uniform(80, 95)
            oil_pressure = random.uniform(2.5, 3.8)
            battery = random.uniform(12.5, 14.2)
            accel = random.uniform(0.0, 0.3)

        return SensorData(
            vehicle_id=vehicle_id,
            timestamp=datetime.now().isoformat(),
            engine_rpm=round(rpm, 2),
            engine_temp=round(temp, 2),
            oil_pressure=round(oil_pressure, 2),
            battery_voltage=round(battery, 2),
            mileage=round(random.uniform(50000, 180000), 2),
            fuel_level=round(random.uniform(5, 100), 2),
            tire_pressure=[round(random.uniform(28, 38), 1) for _ in range(4)],
            acceleration=round(accel, 2),
            brake_intensity=round(random.uniform(0.0, 1.0), 2)
        )

    @staticmethod
    def generate_maintenance_history(vehicle_id: str, years: int = 3) -> List[MaintenanceRecord]:
        """Generate realistic maintenance records with cost data"""
        records = []
        services = list(VEHICLE_COMPONENTS.keys())

        base_date = datetime.now() - timedelta(days=365 * years)

        for _ in range(random.randint(5, 15)):
            component = random.choice(services)
            service_date = base_date + timedelta(days=random.randint(0, 365 * years))

            record = MaintenanceRecord(
                vehicle_id=vehicle_id,
                service_date=service_date.isoformat(),
                service_type=f"Maintenance: {component.replace('_', ' ').title()}",
                cost=VEHICLE_COMPONENTS[component]["cost"] + random.randint(-500, 1000),
                mileage=random.uniform(30000, 180000),
                components_replaced=[component],
                duration_minutes=random.randint(30, 240),
                technician=f"Tech_{random.randint(1, 50):03d}"
            )
            records.append(record)

        return sorted(records, key=lambda x: x.service_date)
