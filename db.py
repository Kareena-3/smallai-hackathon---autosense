"""
Database utility — reads vehicle telemetry from the Prisma SQLite database.

Usage:
    from db import get_all_vehicles, get_vehicle, compute_failure_probability

The failure probability formula is deterministic: same sensor inputs always
produce the same output (no randomness).
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional


DB_PATH = os.path.join(os.path.dirname(__file__), "dev.db")


def _get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def compute_failure_probability(record: Dict[str, Any]) -> float:
    """
    Deterministic failure probability formula (0–100%).

    Weighted risk score based on sensor readings:
      RPM risk (10%)     — higher RPM = more stress
      Oil pressure (15%) — lower pressure = worse
      Fuel pressure (10%) — lower = worse
      Coolant pressure (10%) — lower = worse
      Oil temp (15%)     — hotter = worse
      Coolant temp (15%) — hotter = worse
      Brake wear (20%)   — direct percentage
      Engine cond (5%)   — 0=faulty adds risk
    """
    rpm_risk = min(record["engine_rpm"] / 5000.0, 1.0)
    oil_risk = max(0.0, 1.0 - record["lub_oil_pressure"] / 5.0)
    fuel_risk = max(0.0, 1.0 - record["fuel_pressure"] / 60.0)
    coolant_p_risk = max(0.0, 1.0 - record["coolant_pressure"] / 35.0)
    oil_temp_risk = min(record["lub_oil_temp"] / 140.0, 1.0)
    coolant_temp_risk = min(record["coolant_temp"] / 120.0, 1.0)
    brake_risk = record["brake_wear_pct"] / 100.0
    engine_risk = 0.0 if record["engine_condition"] == 1 else 1.0

    prob = (
        0.10 * rpm_risk
        + 0.15 * oil_risk
        + 0.10 * fuel_risk
        + 0.10 * coolant_p_risk
        + 0.15 * oil_temp_risk
        + 0.15 * coolant_temp_risk
        + 0.20 * brake_risk
        + 0.05 * engine_risk
    )

    return round(min(100.0, max(0.0, prob * 100.0)), 1)


def get_all_vehicles() -> List[Dict[str, Any]]:
    """Fetch all vehicle telemetry records from the database."""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM VehicleTelemetry ORDER BY timestamp"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_vehicle(vehicle_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single vehicle by its vehicle_id."""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM VehicleTelemetry WHERE vehicle_id = ?",
            (vehicle_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


if __name__ == "__main__":
    print("Vehicle Telemetry Database")
    print("=" * 70)
    vehicles = get_all_vehicles()
    for v in vehicles:
        print(
            f"  {v['vehicle_id']:16s} | {v['make']:10s} {v['model']:16s} | "
            f"Fail: {v['failure_prob']:5.1f}% | Engine: {'OK' if v['engine_condition'] else 'FAULT'}"
        )
    print(f"\nTotal: {len(vehicles)} vehicles")
