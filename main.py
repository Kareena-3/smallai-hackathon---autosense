#!/usr/bin/env python3
"""
Main entry point for the Automotive Predictive Maintenance & Agentic AI System.

Run this file to start the full simulation:
    python main.py
"""

import json
import logging

from config import MAX_WORKERS
from data_generator import SyntheticDataGenerator
from master import MasterAgent

logger = logging.getLogger(__name__)


def main():
    """Main execution pipeline"""
    print("\n" + "=" * 100)
    print("AUTOMOTIVE PREDICTIVE MAINTENANCE & AGENTIC AI SYSTEM v2.0")
    print("=" * 100 + "\n")

    try:
        # Generate synthetic data
        logger.info("Generating synthetic vehicle fleet data...")
        vehicles = SyntheticDataGenerator.generate_vehicles(count=10, region="Delhi")
        logger.info(f"Generated {len(vehicles)} vehicles")

        # Initialize master agent
        logger.info("Initializing Master Agent with 6 Worker Agents...")
        master = MasterAgent(vehicles, max_workers=MAX_WORKERS)

        # Run orchestration
        logger.info("Starting orchestration cycle...")
        results = master.orchestrate_maintenance_cycle()

        # Generate and print report
        report = master.generate_report(results)
        print(report)

        # Save detailed results to JSON
        output_file = "maintenance_system_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to {output_file}")

        # Print vehicle-level details
        print("\nVEHICLE-LEVEL DETAILS:\n")
        for v_result in results["vehicles"][:5]:  # Show first 5
            if v_result["status"] == "success":
                print(f"  {v_result['vehicle_id']} | Alert: {v_result['alert_level'].upper()}")
                print(f"     Failures: {len(v_result['failures'])} | Status: {'Appointment Scheduled' if v_result.get('appointment') else 'No Appointment'}")
                if v_result["failures"]:
                    for failure in v_result["failures"][:2]:
                        print(f"     -> {failure['component']}: {failure['recommendation']}")
                print()

        return results

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    results = main()
