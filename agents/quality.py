"""
Manufacturing Quality Agent — RCA/CAPA analysis and manufacturing insights.
"""

import random
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from config import AgentRole, VEHICLE_COMPONENTS
from models import PredictedFailure, RCAInsight
from agents.base import BaseAgent


class ManufacturingQualityAgent(BaseAgent):
    """RCA/CAPA analysis and manufacturing insights"""

    def __init__(self):
        super().__init__("ManufacturingQualityAgent", AgentRole.QUALITY)
        self.insights = []

    def execute(self, all_failures: List[PredictedFailure], vehicles: Dict[str, Dict]) -> List[RCAInsight]:
        """Analyze defect patterns and generate insights"""
        return self.analyze_defect_patterns(all_failures, vehicles)

    def analyze_defect_patterns(self, all_failures: List[PredictedFailure], vehicles: Dict[str, Dict]) -> List[RCAInsight]:
        """Cross-reference failures with manufacturing data"""
        self.log_action("access", "manufacturing_db", "sensitive")

        defect_patterns = defaultdict(list)

        for failure in all_failures:
            vehicle_info = vehicles.get(failure.vehicle_id, {})
            model = vehicle_info.get("model", "Unknown")
            pattern_key = f"{model}_{failure.component}"
            defect_patterns[pattern_key].append(failure)

        insights = []

        for pattern, failures in defect_patterns.items():
            if len(failures) >= 2:
                model = pattern.split("_")[0]
                component = "_".join(pattern.split("_")[1:])
                affected_models = list(set([vehicles.get(f.vehicle_id, {}).get("model") for f in failures]))

                insight_id = f"RCA_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

                insight = RCAInsight(
                    insight_id=insight_id,
                    defect_pattern=pattern,
                    frequency=len(failures),
                    affected_vehicles=[f.vehicle_id for f in failures],
                    root_cause=f"Manufacturing variance in {component} assembly/specification",
                    corrective_action=f"Implement enhanced QC check; Adjust torque/assembly specs by +/-2%; Revalidate supplier parts",
                    affected_models=affected_models,
                    priority="CRITICAL" if len(failures) > 5 else ("HIGH" if len(failures) > 3 else "MEDIUM"),
                    estimated_cost_saved=len(failures) * VEHICLE_COMPONENTS.get(component.lower().replace(" ", "_"), {}).get("cost", 5000)
                )
                insights.append(insight)
                self.logger.info(f"RCA INSIGHT: {pattern} - {len(failures)} vehicles affected - Cost saved: Rs.{insight.estimated_cost_saved}")

        self.insights.extend(insights)
        return insights
