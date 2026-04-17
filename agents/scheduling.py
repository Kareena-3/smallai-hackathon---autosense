"""
Scheduling Agent — manages appointment scheduling and capacity optimization.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from config import AgentRole, VEHICLE_COMPONENTS
from models import PredictedFailure, ServiceAppointment
from agents.base import BaseAgent


class SchedulingAgent(BaseAgent):
    """Manages appointment scheduling and capacity optimization"""

    def __init__(self, service_centers: Dict = None):
        super().__init__("SchedulingAgent", AgentRole.SCHEDULING)
        self.service_centers = service_centers or {
            "Center_Delhi_1": {"location": "Delhi", "times": ["09:00", "10:00", "14:00", "15:00", "16:00"]},
            "Center_Delhi_2": {"location": "Delhi", "times": ["09:30", "11:00", "13:00", "15:30", "17:00"]},
            "Center_Gurgaon": {"location": "Gurgaon", "times": ["08:30", "10:30", "12:00", "14:30", "16:30"]}
        }
        self.bookings = []

    def execute(self, vehicle_id: str, customer: Dict, failures: List[PredictedFailure]) -> Optional[ServiceAppointment]:
        """Schedule appointment for vehicle"""
        return self.schedule_appointment(vehicle_id, customer, failures)

    def get_available_slots(self, days_ahead: int = 14) -> List[Tuple[str, str, str, str]]:
        """Fetch available appointment slots"""
        self.log_action("query", "service_center_db", "normal")

        slots = []
        for center_name, center_info in self.service_centers.items():
            for day in range(days_ahead):
                date = (datetime.now() + timedelta(days=day+1)).strftime("%Y-%m-%d")
                for time in center_info["times"]:
                    slots.append((center_name, center_info["location"], date, time))

        return slots[:min(20, len(slots))]

    def schedule_appointment(self, vehicle_id: str, customer: Dict, failures: List[PredictedFailure]) -> Optional[ServiceAppointment]:
        """Confirm appointment booking"""
        self.log_action("write", "booking_db", "normal")

        slots = self.get_available_slots()
        if not slots:
            return None

        selected_slot = random.choice(slots)
        appointment_id = f"APT_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

        estimated_cost = sum(
            VEHICLE_COMPONENTS.get(f.component.lower().replace(" ", "_"), {}).get("cost", 2000)
            for f in failures
        ) + random.randint(500, 2000)

        appointment = ServiceAppointment(
            appointment_id=appointment_id,
            vehicle_id=vehicle_id,
            customer_name=customer.get("owner", "Unknown"),
            customer_phone=customer.get("phone", ""),
            appointment_date=selected_slot[2],
            appointment_time=selected_slot[3],
            service_center=selected_slot[0],
            estimated_duration_minutes=random.randint(45, 240),
            predicted_failures=[f.component for f in failures],
            estimated_cost=estimated_cost,
            status="confirmed"
        )

        self.bookings.append(appointment)
        self.logger.info(f"APPOINTMENT: {vehicle_id} @ {selected_slot[0]} on {selected_slot[2]} {selected_slot[3]}")

        return appointment
