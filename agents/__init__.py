"""
Agents package — contains all worker agents for the predictive maintenance system.
"""

from agents.base import BaseAgent
from agents.data_analysis import DataAnalysisAgent
from agents.diagnosis import DiagnosisAgent
from agents.engagement import CustomerEngagementAgent
from agents.scheduling import SchedulingAgent
from agents.feedback import FeedbackAgent
from agents.quality import ManufacturingQualityAgent

__all__ = [
    "BaseAgent",
    "DataAnalysisAgent",
    "DiagnosisAgent",
    "CustomerEngagementAgent",
    "SchedulingAgent",
    "FeedbackAgent",
    "ManufacturingQualityAgent",
]
