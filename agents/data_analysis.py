"""
Data Analysis Agent — analyzes real-time telematics and maintenance history.
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Any

import numpy as np

from config import AgentRole, AlertLevel, SENSOR_THRESHOLDS
from models import SensorData, MaintenanceRecord
from agents.base import BaseAgent


class DataAnalysisAgent(BaseAgent):
    """Analyzes real-time telematics and maintenance history"""

    def __init__(self):
        super().__init__("DataAnalysisAgent", AgentRole.DATA_ANALYSIS)
        self.baseline_thresholds = SENSOR_THRESHOLDS

    def execute(self, sensor: SensorData, maintenance_history: List[MaintenanceRecord]) -> Tuple[AlertLevel, Dict[str, Any]]:
        """Analyze sensor data and forecast maintenance"""
        return self.analyze_sensor_data(sensor), self.forecast_maintenance_needs(maintenance_history, sensor.mileage)

    def analyze_sensor_data(self, sensor: SensorData) -> AlertLevel:
        """Detect anomalies in sensor readings"""
        self.log_action("read", "telematics_db", "normal")

        anomalies = []

        # Check engine temperature
        if not (SENSOR_THRESHOLDS["engine_temp"]["min"] <= sensor.engine_temp <= SENSOR_THRESHOLDS["engine_temp"]["max"]):
            severity = AlertLevel.RED if sensor.engine_temp > SENSOR_THRESHOLDS["engine_temp"]["critical_max"] else AlertLevel.YELLOW
            anomalies.append(("engine_temp", sensor.engine_temp, severity))

        # Check oil pressure
        if not (SENSOR_THRESHOLDS["oil_pressure"]["min"] <= sensor.oil_pressure <= SENSOR_THRESHOLDS["oil_pressure"]["max"]):
            severity = AlertLevel.RED if sensor.oil_pressure < SENSOR_THRESHOLDS["oil_pressure"]["critical_min"] else AlertLevel.YELLOW
            anomalies.append(("oil_pressure", sensor.oil_pressure, severity))

        # Check battery voltage
        if not (SENSOR_THRESHOLDS["battery_voltage"]["min"] <= sensor.battery_voltage <= SENSOR_THRESHOLDS["battery_voltage"]["max"]):
            severity = AlertLevel.RED if sensor.battery_voltage < SENSOR_THRESHOLDS["battery_voltage"]["critical_min"] else AlertLevel.YELLOW
            anomalies.append(("battery", sensor.battery_voltage, severity))

        # Determine overall alert level
        if any(s == AlertLevel.RED for _, _, s in anomalies):
            return AlertLevel.RED
        elif any(s == AlertLevel.YELLOW for _, _, s in anomalies):
            return AlertLevel.YELLOW

        return AlertLevel.GREEN

    def forecast_maintenance_needs(self, history: List[MaintenanceRecord], current_mileage: float) -> Dict[str, Any]:
        """Forecast upcoming maintenance based on patterns"""
        self.log_action("read", "maintenance_db", "normal")

        service_intervals = defaultdict(list)
        for record in history:
            service_intervals[record.service_type].append(record)

        forecast = {}
        for service_type, records in service_intervals.items():
            if len(records) > 1:
                mileages = [r.mileage for r in sorted(records, key=lambda x: x.mileage)]
                intervals = [mileages[i+1] - mileages[i] for i in range(len(mileages)-1) if mileages[i+1] > mileages[i]]

                if intervals:
                    avg_interval = np.mean(intervals)
                    last_mileage = mileages[-1]
                    next_due_mileage = last_mileage + avg_interval
                    days_until = max(0, int((next_due_mileage - current_mileage) / 25))

                    forecast[service_type] = {
                        "days_until": days_until,
                        "next_mileage": int(next_due_mileage),
                        "interval": int(avg_interval)
                    }

        return forecast
