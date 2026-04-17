"""
Base agent — abstract class all worker agents inherit from.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from config import AgentRole


class BaseAgent(ABC):
    """Abstract base class for all agents"""

    def __init__(self, name: str, role: AgentRole):
        self.name = name
        self.role = role
        self.logger = logging.getLogger(f"Agent:{name}")
        self.ueba_actions = []
        self.performance_metrics = {"calls": 0, "total_time": 0.0}

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Main execution method"""
        pass

    def log_action(self, action_type: str, resource: str, sensitivity: str = "normal"):
        """Log action for UEBA monitoring"""
        self.ueba_actions.append({
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "resource": resource,
            "sensitivity": sensitivity
        })

    def measure_time(self, func):
        """Decorator to measure execution time"""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            self.performance_metrics["calls"] += 1
            self.performance_metrics["total_time"] += elapsed
            return result
        return wrapper
