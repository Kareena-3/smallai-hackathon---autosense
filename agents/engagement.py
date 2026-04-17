"""
Customer Engagement Agent — initiates voice-based customer conversations.
"""

import random
from typing import Dict, List, Tuple, Optional

from config import AgentRole, AlertLevel
from models import PredictedFailure
from agents.base import BaseAgent


class CustomerEngagementAgent(BaseAgent):
    """Initiates voice-based customer conversations"""

    def __init__(self):
        super().__init__("CustomerEngagementAgent", AgentRole.ENGAGEMENT)
        self.engagement_templates = [
            "Hi {owner}! I'm calling from {center}. We've detected your {model} needs {component} service in about {days} days. Your safety is our priority. Can we schedule an appointment?",
            "Hello {owner}! Your {model} is due for {component} maintenance. I recommend booking within the next {days} days to avoid any issues. Are you available this week?",
            "Good day {owner}! Our AI system detected that your {model} will benefit from {component} service soon. We have flexible slots available. When would suit you best?"
        ]

    def execute(self, vehicle: Dict, failures: List[PredictedFailure]) -> Tuple[bool, str, Optional[str]]:
        """Engage customer with appointment offer"""
        return self.engage_customer(vehicle, failures)

    def engage_customer(self, vehicle: Dict, failures: List[PredictedFailure]) -> Tuple[bool, str, Optional[str]]:
        """Simulate voice agent engagement"""
        self.log_action("initiate_call", "customer_db", "sensitive")

        if not failures:
            return False, "No urgent issues detected", None

        top_failure = max(failures, key=lambda f: f.failure_probability)
        template = random.choice(self.engagement_templates)

        message = template.format(
            owner=vehicle.get("owner", "Customer"),
            model=vehicle.get("model", "vehicle"),
            component=top_failure.component,
            days=top_failure.estimated_days,
            center="AutoCare Service Center"
        )

        self.logger.info(f"VOICE ENGAGEMENT: {message}")

        # Simulate customer response based on failure severity
        if top_failure.severity == AlertLevel.RED:
            acceptance_rate = 0.85
        elif top_failure.severity == AlertLevel.YELLOW:
            acceptance_rate = 0.68
        else:
            acceptance_rate = 0.45

        accepted = random.random() < acceptance_rate
        response = "Accepted - Customer interested" if accepted else "Declined - Customer not available"

        return accepted, message, response
