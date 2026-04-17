"""
Feedback Agent — post-service follow-up and feedback collection.
"""

import random
from datetime import datetime
from typing import Optional, List

from config import AgentRole, VEHICLE_COMPONENTS
from models import ServiceAppointment, CustomerFeedback
from agents.base import BaseAgent


class FeedbackAgent(BaseAgent):
    """Post-service follow-up and feedback collection"""

    def __init__(self):
        super().__init__("FeedbackAgent", AgentRole.FEEDBACK)
        self.feedback_records = []

    def execute(self, appointment: ServiceAppointment) -> Optional[CustomerFeedback]:
        """Collect post-service feedback"""
        return self.collect_feedback(appointment)

    def collect_feedback(self, appointment: ServiceAppointment) -> CustomerFeedback:
        """Simulate post-service feedback collection"""
        self.log_action("update", "customer_db", "normal")

        satisfaction = random.randint(7, 10)
        service_quality = random.randint(3, 5)
        technician_behavior = random.randint(3, 5)

        feedback_id = f"FB_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

        feedback = CustomerFeedback(
            feedback_id=feedback_id,
            vehicle_id=appointment.vehicle_id,
            appointment_id=appointment.appointment_id,
            satisfaction_score=satisfaction,
            service_quality=service_quality,
            technician_behavior=technician_behavior,
            would_recommend=satisfaction >= 8,
            issues_resolved=random.random() < 0.92,
            additional_issues_found=[] if random.random() < 0.7 else [random.choice(list(VEHICLE_COMPONENTS.keys()))]
        )

        self.feedback_records.append(feedback)
        self.logger.info(f"FEEDBACK: {appointment.vehicle_id} - Satisfaction: {satisfaction}/10")

        return feedback
