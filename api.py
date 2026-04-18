from collections import Counter
import random
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from main import main as run_main

app = FastAPI(
    title="AutoSense API",
    description="Lightweight integration API for the Automotive Predictive Maintenance demo.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def generate_manufacturing_insights(results):
    failures = []
    for vehicle in results.get("vehicles", []):
        for failure in vehicle.get("failures", []):
            component = failure.get("component") if isinstance(failure, dict) else None
            if component:
                failures.append(component)

    counts = Counter([c.strip().lower() for c in failures if c])
    insights = []
    for component, count in counts.most_common():
        if count >= 2:
            title = f"{component.title()} issue recurring across {count} vehicles"
            severity = "High" if count >= 3 else "Medium"
            insights.append({"title": title, "severity": severity, "vehicles": count})

    if not insights:
        insights.append({"title": "No recurring manufacturing issues detected", "severity": "Low", "vehicles": 0})

    return insights


def enhance_schedule_and_communication(results):
    appointments = results.get("appointments", [])
    completed = 0
    for appointment in appointments:
        failures = appointment.get("predicted_failures") or []
        cost = appointment.get("estimated_cost", 0)
        priority = "Low"
        if len(failures) >= 3 or cost >= 12000:
            priority = "High"
        elif len(failures) == 2 or cost >= 7000:
            priority = "Medium"

        appointment["priority"] = priority
        appointment["suggested_slot"] = appointment.get("appointment_time") or "09:00"
        appointment["suggested_slot_detail"] = f"{appointment.get('appointment_date', datetime.now().date().isoformat())} {appointment['suggested_slot']}"
        appointment["customer_notified"] = random.random() > 0.2
        appointment["response_status"] = "Confirmed" if appointment["customer_notified"] else "Pending"
        if appointment["customer_notified"]:
            completed += 1

    summary = {
        "total_appointments": len(appointments),
        "notifications_sent": completed,
        "pending_responses": len(appointments) - completed,
        "confirmed_responses": completed,
    }
    return appointments, summary


def determine_system_status(results):
    anomalies = results.get("anomalies", [])
    if anomalies:
        return "Warning"
    return "Normal"


@app.get("/simulate")
async def simulate():
    try:
        results = run_main()
        insights = generate_manufacturing_insights(results)
        appointments, comm_summary = enhance_schedule_and_communication(results)
        system_status = determine_system_status(results)

        results["manufacturing_insights"] = insights
        results["communication_summary"] = comm_summary
        results["system_status"] = system_status
        results["scheduling_suggestions"] = appointments

        return results
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
