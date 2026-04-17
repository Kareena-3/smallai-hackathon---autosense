"""
Diagnosis Agent — runs predictive models to assess component failures.
"""

import random
from typing import Dict, List

from config import AgentRole, AlertLevel, ServicePriority
from models import SensorData, PredictedFailure
from agents.base import BaseAgent


class DiagnosisAgent(BaseAgent):
    """Runs predictive models to assess failures"""

    def __init__(self):
        super().__init__("DiagnosisAgent", AgentRole.DIAGNOSIS)

    def execute(self, sensor: SensorData, maintenance_forecast: Dict) -> List[PredictedFailure]:
        """Predict component failures using ML logic"""
        return self.predict_failures(sensor, maintenance_forecast)

    def predict_failures(self, sensor: SensorData, maintenance_forecast: Dict) -> List[PredictedFailure]:
        """Predict component failures based on sensor and maintenance data"""
        self.log_action("execute", "prediction_engine", "normal")

        failures = []

        # Brake wear prediction
        if "Maintenance: Brake Pads" in maintenance_forecast:
            days = maintenance_forecast["Maintenance: Brake Pads"].get("days_until", 999)
            if days < 60:
                failures.append(PredictedFailure(
                    vehicle_id=sensor.vehicle_id,
                    component="Brake Pads",
                    failure_probability=0.87,
                    estimated_days=max(1, days // 2),
                    estimated_km=int(sensor.mileage * 0.15),
                    severity=AlertLevel.RED if days < 30 else AlertLevel.YELLOW,
                    recommendation="Schedule brake service immediately" if days < 30 else "Brake service recommended soon",
                    priority=ServicePriority.CRITICAL if days < 30 else ServicePriority.HIGH
                ))

        # Oil change prediction
        if "Maintenance: Oil Filter" in maintenance_forecast:
            days = maintenance_forecast["Maintenance: Oil Filter"].get("days_until", 999)
            if days < 90:
                failures.append(PredictedFailure(
                    vehicle_id=sensor.vehicle_id,
                    component="Oil & Filter",
                    failure_probability=0.72,
                    estimated_days=max(1, days // 2),
                    estimated_km=int(sensor.mileage * 0.10),
                    severity=AlertLevel.YELLOW,
                    recommendation="Oil change recommended within 4 weeks",
                    priority=ServicePriority.HIGH
                ))

        # Battery prediction
        if sensor.battery_voltage < 12.8:
            failures.append(PredictedFailure(
                vehicle_id=sensor.vehicle_id,
                component="Battery",
                failure_probability=0.65,
                estimated_days=45,
                estimated_km=1000,
                severity=AlertLevel.YELLOW,
                recommendation="Battery inspection and possible replacement",
                priority=ServicePriority.MEDIUM
            ))

        # Tire wear prediction
        if sensor.mileage > 80000 and random.random() < 0.35:
            failures.append(PredictedFailure(
                vehicle_id=sensor.vehicle_id,
                component="Tires",
                failure_probability=0.58,
                estimated_days=30,
                estimated_km=800,
                severity=AlertLevel.YELLOW,
                recommendation="Tire rotation or replacement due",
                priority=ServicePriority.MEDIUM
            ))

        # Transmission fluid check
        if sensor.mileage > 120000 and random.random() < 0.25:
            failures.append(PredictedFailure(
                vehicle_id=sensor.vehicle_id,
                component="Transmission Fluid",
                failure_probability=0.42,
                estimated_days=60,
                estimated_km=1500,
                severity=AlertLevel.YELLOW,
                recommendation="Transmission fluid change recommended",
                priority=ServicePriority.MEDIUM
            ))

        return failures
