"""
UEBA (User & Entity Behavior Analytics) — security monitoring for agent actions.
"""

import logging
from typing import Dict, List, Any

from models import AgentBehavior
from agents.base import BaseAgent


class UEBAMonitor:
    """User & Entity Behavior Analytics for agent security"""

    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.logger = logging.getLogger("UEBAMonitor")
        self.baseline_profiles = self._init_baseline()
        self.anomalies = []
        self.normal_operations_count = 0

    def _init_baseline(self) -> Dict[str, Dict[str, Any]]:
        """Initialize normal behavior baselines for each agent"""
        return {
            "DataAnalysisAgent": {
                "normal_resources": ["telematics_db", "maintenance_db"],
                "normal_actions": ["read", "execute"],
                "max_calls_per_cycle": 10
            },
            "DiagnosisAgent": {
                "normal_resources": ["prediction_engine"],
                "normal_actions": ["execute"],
                "max_calls_per_cycle": 5
            },
            "CustomerEngagementAgent": {
                "normal_resources": ["customer_db"],
                "normal_actions": ["initiate_call"],
                "max_calls_per_cycle": 10
            },
            "SchedulingAgent": {
                "normal_resources": ["service_center_db", "booking_db"],
                "normal_actions": ["query", "write"],
                "max_calls_per_cycle": 10
            },
            "FeedbackAgent": {
                "normal_resources": ["customer_db"],
                "normal_actions": ["update"],
                "max_calls_per_cycle": 5
            },
            "ManufacturingQualityAgent": {
                "normal_resources": ["manufacturing_db"],
                "normal_actions": ["access"],
                "max_calls_per_cycle": 3
            }
        }

    def detect_anomalies(self) -> List[AgentBehavior]:
        """Monitor agent behaviors and detect anomalies"""
        detected = []

        for agent in self.agents:
            baseline = self.baseline_profiles.get(agent.name, {})
            normal_resources = set(baseline.get("normal_resources", []))
            normal_actions = set(baseline.get("normal_actions", []))

            for action_log in agent.ueba_actions:
                action_type = action_log.get("action_type")
                resource = action_log.get("resource")
                sensitivity = action_log.get("sensitivity")

                is_anomalous = False
                anomaly_score = 0.0
                alert_message = ""

                # Check for unauthorized resource access
                if resource not in normal_resources:
                    is_anomalous = True
                    anomaly_score = 0.85
                    alert_message = f"Unauthorized resource access: {resource}"

                # Check for unexpected action types
                if action_type not in normal_actions:
                    is_anomalous = True
                    anomaly_score = max(anomaly_score, 0.70)
                    alert_message = f"Unexpected action type: {action_type}"

                # Check for sensitive data access by unauthorized agents
                if sensitivity == "sensitive" and agent.role.value not in ["master", "quality"]:
                    is_anomalous = True
                    anomaly_score = max(anomaly_score, 0.90)
                    alert_message = f"Sensitive data access by {agent.name}"

                if is_anomalous:
                    behavior = AgentBehavior(
                        agent_name=agent.name,
                        agent_role=agent.role.value,
                        timestamp=action_log.get("timestamp"),
                        action_type=action_type,
                        resource_accessed=resource,
                        data_sensitivity=sensitivity,
                        anomaly_score=anomaly_score,
                        is_anomalous=True,
                        alert_message=alert_message
                    )
                    detected.append(behavior)
                    self.logger.warning(f"SECURITY ALERT: {agent.name} - {alert_message} (Score: {anomaly_score:.2f})")
                else:
                    self.normal_operations_count += 1

        self.anomalies.extend(detected)
        return detected
