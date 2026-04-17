"""
Master Agent — main orchestrator coordinating all worker agents.
"""

import json
import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Any

from config import AgentRole, MAX_WORKERS, THREAD_TIMEOUT
from models import PredictedFailure
from data_generator import SyntheticDataGenerator
from agents import (
    DataAnalysisAgent,
    DiagnosisAgent,
    CustomerEngagementAgent,
    SchedulingAgent,
    FeedbackAgent,
    ManufacturingQualityAgent,
)
from ueba import UEBAMonitor


class MasterAgent:
    """Main orchestrator coordinating all worker agents"""

    def __init__(self, vehicles: Dict[str, Dict], max_workers: int = MAX_WORKERS):
        self.name = "MasterAgent"
        self.role = AgentRole.MASTER
        self.vehicles = vehicles
        self.vehicle_ids = list(vehicles.keys())
        self.max_workers = max_workers
        self.logger = logging.getLogger("MasterAgent")

        # Initialize worker agents
        self.data_agent = DataAnalysisAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.engagement_agent = CustomerEngagementAgent()
        self.scheduling_agent = SchedulingAgent()
        self.feedback_agent = FeedbackAgent()
        self.quality_agent = ManufacturingQualityAgent()

        # Security monitoring
        self.ueba_monitor = UEBAMonitor([
            self.data_agent, self.diagnosis_agent, self.engagement_agent,
            self.scheduling_agent, self.feedback_agent, self.quality_agent
        ])

        # Results storage
        self.all_failures = []
        self.appointments = []
        self.feedbacks = []
        self.insights = []
        self.execution_log = []

        self.logger.info(f"MASTER AGENT INITIALIZED | Max Workers: {max_workers} | Fleet Size: {len(vehicles)}")

    def _process_vehicle_parallel(self, vehicle_id: str) -> Dict[str, Any]:
        """Process single vehicle (for parallel execution)"""
        try:
            vehicle = self.vehicles[vehicle_id]

            # Step 1: Generate sensor data
            sensor = SyntheticDataGenerator.generate_sensor_data(vehicle_id)

            # Step 2: Get maintenance history
            history = SyntheticDataGenerator.generate_maintenance_history(vehicle_id)

            # Step 3: Analyze sensor data
            alert_level, forecast = self.data_agent.execute(sensor, history)

            # Step 4: Diagnose failures
            failures = self.diagnosis_agent.execute(sensor, forecast)

            # Step 5: Customer engagement
            accepted, message, response = self.engagement_agent.execute(vehicle, failures)

            # Step 6: Schedule appointment if accepted
            appointment = None
            if accepted and failures:
                appointment = self.scheduling_agent.execute(vehicle_id, vehicle, failures)

            # Step 7: Simulate post-service feedback (for demo)
            feedback = None
            if appointment and random.random() < 0.7:  # 70% completion rate
                feedback = self.feedback_agent.execute(appointment)

            return {
                "vehicle_id": vehicle_id,
                "status": "success",
                "alert_level": alert_level.value,
                "failures": [f.to_dict() for f in failures],
                "appointment": appointment.to_dict() if appointment else None,
                "feedback": feedback.to_dict() if feedback else None,
                "customer_response": response
            }

        except Exception as e:
            self.logger.error(f"Error processing {vehicle_id}: {str(e)}", exc_info=True)
            return {
                "vehicle_id": vehicle_id,
                "status": "error",
                "error": str(e)
            }

    def orchestrate_maintenance_cycle(self) -> Dict[str, Any]:
        """Main orchestration loop using parallel processing"""
        start_time = time.time()
        self.logger.info(f"MASTER AGENT: Starting maintenance orchestration cycle | Vehicles: {len(self.vehicle_ids)}")

        results = {
            "metadata": {
                "cycle_id": f"CYCLE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "start_time": datetime.now().isoformat(),
                "total_vehicles": len(self.vehicle_ids),
                "max_workers": self.max_workers
            },
            "vehicles": [],
            "summary": {},
            "appointments": [],
            "insights": [],
            "anomalies": [],
            "performance": {}
        }

        # PARALLEL PROCESSING: Process all vehicles concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_vehicle_parallel, vid): vid
                for vid in self.vehicle_ids
            }

            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=THREAD_TIMEOUT)
                    results["vehicles"].append(result)
                    completed += 1

                    # Aggregate results
                    if result["status"] == "success":
                        if result.get("failures"):
                            self.all_failures.extend([
                                PredictedFailure(**f) if isinstance(f, dict) else f
                                for f in result["failures"]
                            ])
                        if result.get("appointment"):
                            self.appointments.append(result["appointment"])
                        if result.get("feedback"):
                            self.feedbacks.append(result["feedback"])

                except Exception as e:
                    self.logger.error(f"Future exception: {str(e)}")

            self.logger.info(f"Processed {completed}/{len(self.vehicle_ids)} vehicles")

        # SECURITY MONITORING: UEBA anomaly detection
        anomalies = self.ueba_monitor.detect_anomalies()
        results["anomalies"] = [a.to_dict() for a in anomalies]

        # MANUFACTURING INSIGHTS: RCA/CAPA analysis
        if self.all_failures:
            insights = self.quality_agent.execute(self.all_failures, self.vehicles)
            results["insights"] = [i.to_dict() for i in insights]
            self.insights = insights

        # PERFORMANCE METRICS
        elapsed_time = time.time() - start_time
        results["metadata"]["end_time"] = datetime.now().isoformat()
        results["metadata"]["execution_time_seconds"] = round(elapsed_time, 2)

        results["summary"] = {
            "total_appointments": len(self.appointments),
            "total_failures_predicted": len(self.all_failures),
            "total_insights_generated": len(self.insights),
            "security_anomalies_detected": len(anomalies),
            "normal_operations": self.ueba_monitor.normal_operations_count,
            "vehicles_processed_per_second": round(len(self.vehicle_ids) / elapsed_time, 2)
        }

        results["performance"] = {
            "data_analysis_agent": self.data_agent.performance_metrics,
            "diagnosis_agent": self.diagnosis_agent.performance_metrics,
            "engagement_agent": self.engagement_agent.performance_metrics,
            "scheduling_agent": self.scheduling_agent.performance_metrics,
            "feedback_agent": self.feedback_agent.performance_metrics,
            "quality_agent": self.quality_agent.performance_metrics
        }

        self.logger.info(f"ORCHESTRATION COMPLETE | Time: {elapsed_time:.2f}s | Throughput: {results['summary']['vehicles_processed_per_second']} vehicles/sec")

        return results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate executive summary report"""
        report = f"\n{'='*100}\n"
        report += "AUTONOMOUS PREDICTIVE MAINTENANCE SYSTEM - EXECUTIVE REPORT\n"
        report += f"{'='*100}\n\n"

        report += f"FLEET ANALYSIS:\n"
        report += f"  - Total Vehicles Processed: {results['metadata']['total_vehicles']}\n"
        report += f"  - Processing Time: {results['metadata']['execution_time_seconds']}s\n"
        report += f"  - Throughput: {results['summary']['vehicles_processed_per_second']} vehicles/sec\n"
        report += f"  - Parallel Workers: {results['metadata']['max_workers']}\n\n"

        report += f"PREDICTIVE MAINTENANCE SUMMARY:\n"
        report += f"  - Failures Predicted: {results['summary']['total_failures_predicted']}\n"
        report += f"  - Appointments Scheduled: {results['summary']['total_appointments']}\n"
        report += f"  - Forecasted Revenue: Rs.{self.calculate_total_revenue()}\n\n"

        report += f"MANUFACTURING INSIGHTS (RCA/CAPA):\n"
        if self.insights:
            for insight in self.insights[:5]:
                report += f"  - {insight.defect_pattern} ({insight.frequency} vehicles)\n"
                report += f"    Priority: {insight.priority} | Cost Saved: Rs.{insight.estimated_cost_saved}\n"
                report += f"    Action: {insight.corrective_action[:60]}...\n\n"
        else:
            report += "  - No critical patterns detected\n\n"

        report += f"SECURITY (UEBA) MONITORING:\n"
        report += f"  - Anomalies Detected: {results['summary']['security_anomalies_detected']}\n"
        report += f"  - Normal Operations: {results['summary']['normal_operations']}\n"
        if results.get("anomalies"):
            for anomaly in results["anomalies"][:3]:
                report += f"  WARNING: {anomaly['agent_name']}: {anomaly['alert_message']}\n"
        else:
            report += "  All agent behaviors normal - No security threats detected\n\n"

        report += f"\nFINANCIAL IMPACT:\n"
        report += f"  - Potential Revenue: Rs.{self.calculate_total_revenue()}\n"
        report += f"  - Estimated Customer Retention Increase: 35-45%\n"
        report += f"  - Preventive Savings: Rs.{self.calculate_preventive_savings()}\n\n"

        report += f"{'='*100}\n"

        return report

    def calculate_total_revenue(self) -> int:
        """Calculate forecasted service revenue"""
        total = sum(apt.get("estimated_cost", 0) for apt in self.appointments)
        return int(total)

    def calculate_preventive_savings(self) -> int:
        """Calculate savings from preventive maintenance"""
        preventive_cost = self.calculate_total_revenue()
        return preventive_cost * 2  # 2x savings
