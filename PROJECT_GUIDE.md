# AutoSense AI — Complete In-Depth Project Guide

> **Autonomous Predictive Maintenance & Service Scheduling Platform for Indian Automotive OEMs**
> Built for EY Techathon 6.0

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [File Structure](#2-file-structure)
3. [Skills & Technologies Required](#3-skills--technologies-required)
4. [Python Backend — File-by-File Breakdown](#4-python-backend--file-by-file-breakdown)
5. [HTML Dashboard — Full Breakdown](#5-html-dashboard--autosense_dashboardhtml)
6. [How to Run the Project](#6-how-to-run-the-project)
7. [How Each Feature Maps to the Business Case](#7-feature-to-business-mapping)

---

## 1. Project Overview

This project simulates a full **Agentic AI system** for automotive predictive maintenance. The codebase is split into clean, organized modules.

**What this project demonstrates:**
- A Master Agent orchestrating 6 specialized Worker Agents
- Parallel processing of vehicle fleets using thread pools
- ML-style predictive failure detection (rule-based simulation)
- Voice-based customer engagement simulation
- Autonomous appointment scheduling
- Manufacturing feedback loop (RCA / CAPA)
- Security monitoring via UEBA (User & Entity Behavior Analytics)

---

## 2. File Structure

```
Auto/
│
├── main.py                    ← ENTRY POINT — run this to start
├── config.py                  ← All settings, enums, thresholds
├── models.py                  ← Data structures (7 dataclasses)
├── data_generator.py          ← Fake vehicle/sensor/history data
├── master.py                  ← MasterAgent orchestrator (the brain)
├── ueba.py                    ← Security monitoring for agents
│
├── agents/                    ← One file per agent (clean separation)
│   ├── __init__.py            ← Package — re-exports all agents
│   ├── base.py                ← BaseAgent abstract class
│   ├── data_analysis.py       ← Sensor anomaly detection + forecasting
│   ├── diagnosis.py           ← Failure prediction (brake, battery, etc.)
│   ├── engagement.py          ← Voice-bot customer outreach simulation
│   ├── scheduling.py          ← Appointment slot management + booking
│   ├── feedback.py            ← Post-service satisfaction collection
│   └── quality.py             ← RCA/CAPA manufacturing defect analysis
│
├── autosense_dashboard.html   ← Single-file frontend demo (no server)
├── PROJECT_GUIDE.md           ← This guide
├── remixed-734d1398.md        ← Business pitch document
└── automotive_ai_system.py    ← Original monolith (kept for reference)
```

### Why this structure?

| Principle | How it's applied |
|-----------|-----------------|
| **Single Responsibility** | Each file does ONE thing — config, models, one agent, etc. |
| **Package Organization** | All 6 agents live in `agents/` with a clean `__init__.py` |
| **Import Clarity** | `from agents import DiagnosisAgent` — immediately clear where it comes from |
| **Testability** | Each agent can be unit-tested independently |
| **Readability** | Open any file and understand it in isolation |

---

## 3. Skills & Technologies Required

### A. Python Skills

| Skill | Where Used | Why It's Needed |
|-------|-----------|-----------------|
| **OOP (Classes & Inheritance)** | Every agent inherits from `BaseAgent` in `agents/base.py` | Shared logging, UEBA tracking, performance metrics |
| **Abstract Base Classes** | `BaseAgent` uses `ABC` + `@abstractmethod` | Forces every agent to implement `execute()` |
| **Dataclasses** | `models.py` — 7 data containers | Auto-generated `__init__`, serialization via `asdict()` |
| **Enums** | `config.py` — `AlertLevel`, `ServicePriority`, `AgentRole` | Type-safe constants (no magic strings) |
| **Type Hints** | Throughout all files | `Dict[str, Any]`, `List[PredictedFailure]`, `Tuple[bool, str, Optional[str]]` |
| **Threading** | `master.py` — `ThreadPoolExecutor`, `as_completed` | Process 10 vehicles in parallel across 6 threads |
| **Logging** | `config.py` sets it up, every file uses it | Dual-output (console + file), thread-aware format |
| **NumPy** | `agents/data_analysis.py` — `np.mean()` | Calculate average service intervals |
| **Collections** | `defaultdict(list)` in `data_analysis.py` and `quality.py` | Group data by key without checking if key exists |
| **Package Imports** | `agents/__init__.py` re-exports all classes | Clean imports like `from agents import DiagnosisAgent` |

### B. HTML / CSS / JavaScript Skills

| Skill | Where Used | Why |
|-------|-----------|-----|
| **CSS Variables** | `:root { --accent: #3b82f6 }` | One place to change the entire theme |
| **CSS Grid + Flexbox** | `.grid-4`, `.grid-2`, nav layout | Responsive multi-column enterprise layout |
| **CSS Animations** | `@keyframes pulse-btn`, `fadein` | Micro-interactions that make it feel alive |
| **DOM Manipulation** | `getElementById`, `innerHTML`, `createElement` | Rendering data dynamically |
| **Template Literals** | `` `${v.health}%` `` | Building HTML from JavaScript data |
| **setTimeout** | Simulation animation | Step-by-step reveal with 1.4s gaps |

### C. Domain Knowledge

| Concept | What to Know |
|---------|-------------|
| **Agentic AI** | Software agents that perceive, decide, and act autonomously |
| **Multi-Agent Systems** | A master orchestrator + specialized workers |
| **Predictive Maintenance** | Using data patterns to predict failures BEFORE they happen |
| **UEBA** | Security monitoring — tracking what each agent does and flagging anomalies |
| **RCA / CAPA** | Root Cause Analysis + Corrective Actions — manufacturing quality methodology |
| **Telematics** | Real-time vehicle data from OBD-II / IoT sensors |

---

## 4. Python Backend — File-by-File Breakdown

---

### 4.1 `config.py` — Settings & Constants

**Purpose:** Single source of truth for all configuration. Change a threshold or add a vehicle model? Do it here.

**Contents:**

```python
# Logging — dual output (console + file), includes thread name for parallel debugging
logging.basicConfig(
    format='%(asctime)s | %(threadName)-12s | %(name)-20s | %(levelname)-8s | %(message)s',
    handlers=[StreamHandler(), FileHandler('automotive_maintenance.log', encoding='utf-8')]
)

# Performance tuning
MAX_WORKERS = 6           # Parallel threads (one per agent type)
THREAD_TIMEOUT = 30       # Max seconds per vehicle before giving up

# Enums — type-safe constants
class AlertLevel(Enum):   # GREEN / YELLOW / RED
class ServicePriority(Enum):  # LOW (1) to CRITICAL (4)
class AgentRole(Enum):    # MASTER, DATA_ANALYSIS, DIAGNOSIS, etc.

# Component definitions — service interval (km) + cost (₹)
VEHICLE_COMPONENTS = {
    "engine": {"interval_km": 100000, "cost": 50000},
    "brake_pads": {"interval_km": 50000, "cost": 3000},
    ...
}

# Sensor thresholds — normal range + critical limits
SENSOR_THRESHOLDS = {
    "engine_temp": {"min": 70, "max": 100, "critical_max": 110},
    ...
}
```

**Key design decision:** Encoding is set to `utf-8` in the FileHandler to avoid Windows `cp1252` crashes with special characters.

---

### 4.2 `models.py` — Data Structures

**Purpose:** Defines the shape of every piece of data in the system. All 7 dataclasses live here.

| Dataclass | What it represents | Key fields |
|-----------|-------------------|-----------|
| `SensorData` | One snapshot of vehicle sensors | `engine_temp`, `oil_pressure`, `battery_voltage`, `tire_pressure[4]` |
| `MaintenanceRecord` | One past service event | `service_type`, `cost`, `mileage`, `components_replaced` |
| `PredictedFailure` | AI prediction output | `failure_probability` (0-1), `estimated_days`, `severity`, `recommendation` |
| `ServiceAppointment` | Confirmed booking | `appointment_date`, `service_center`, `estimated_cost`, `predicted_failures[]` |
| `AgentBehavior` | UEBA security log | `anomaly_score` (0-1), `is_anomalous`, `alert_message` |
| `RCAInsight` | Manufacturing defect pattern | `defect_pattern`, `root_cause`, `corrective_action`, `estimated_cost_saved` |
| `CustomerFeedback` | Post-service review | `satisfaction_score` (1-10), `would_recommend`, `issues_resolved` |

Every dataclass has a `to_dict()` method using `asdict()` for JSON serialization.

**Why dataclasses?** They auto-generate `__init__()`, `__repr__()`, and `__eq__()`. Compare:

```python
# Without dataclass — 15 lines of boilerplate:
class SensorData:
    def __init__(self, vehicle_id, timestamp, engine_rpm, ...):
        self.vehicle_id = vehicle_id
        self.timestamp = timestamp
        ...

# With dataclass — 3 lines:
@dataclass
class SensorData:
    vehicle_id: str
    timestamp: str
    engine_rpm: float
```

---

### 4.3 `data_generator.py` — Synthetic Data

**Purpose:** Creates fake but realistic data for the demo. In production, this would be replaced by database queries and telematics APIs.

#### `generate_vehicles(count, region)` → Dict of vehicle profiles
- Creates `count` vehicles with random models, mileage (10k-150k km), years (2018-2024)
- IDs follow pattern: `VEH_DEL_00001`, `VEH_MUM_00002`, etc.
- Each gets a Delhi-style registration number and random owner info

#### `generate_sensor_data(vehicle_id, anomaly_probability=0.25)` → SensorData
- 75% chance: generates **normal** readings (temp 80-95°C, oil 2.5-3.8 bar)
- 25% chance: generates **anomalous** readings (temp 95-115°C, oil 0.5-1.8 bar)
- This split ensures the downstream agents always have something interesting to detect

#### `generate_maintenance_history(vehicle_id, years=3)` → List[MaintenanceRecord]
- Creates 5-15 past services spread over `years` years
- Randomly picks components, calculates cost (base ± variance)
- Sorted by date so history looks chronological

---

### 4.4 `agents/base.py` — The Foundation

**Purpose:** Abstract class every agent inherits from. Provides shared infrastructure.

```python
class BaseAgent(ABC):
    def __init__(self, name, role):
        self.name = name                    # "DiagnosisAgent"
        self.role = role                    # AgentRole.DIAGNOSIS
        self.logger = logging.getLogger()   # Dedicated logger per agent
        self.ueba_actions = []              # Security audit trail
        self.performance_metrics = {}       # Call count + timing

    @abstractmethod
    def execute(self, *args, **kwargs):     # Every subclass MUST implement this
        pass

    def log_action(self, action_type, resource, sensitivity):
        # Records action for UEBA monitoring
        # e.g., log_action("read", "telematics_db", "normal")
```

**Why abstract?** The `@abstractmethod` on `execute()` means Python will crash at initialization if any subclass forgets to implement it. This catches bugs early.

---

### 4.5 `agents/data_analysis.py` — Sensor Anomaly Detection

**Purpose:** First agent to process each vehicle. Checks if sensors are in normal range and forecasts next service dates.

#### `analyze_sensor_data(sensor) → AlertLevel`

Checks 3 sensors against thresholds:

| Sensor | Normal Range | Warning | Critical |
|--------|-------------|---------|----------|
| Engine Temp | 70-100°C | > 100°C → YELLOW | > 110°C → RED |
| Oil Pressure | 2.0-4.0 bar | < 2.0 → YELLOW | < 1.5 → RED |
| Battery | 12.0-14.5V | < 12.0 → YELLOW | < 11.5 → RED |

Returns the WORST anomaly found (any RED → RED, else any YELLOW → YELLOW, else GREEN).

#### `forecast_maintenance_needs(history, current_mileage) → Dict`

Predicts when next service is due:
1. Groups past services by type (oil changes, brake replacements, etc.)
2. Calculates average km between services for each type
3. Projects when the next one is due based on current mileage
4. Converts remaining km to days (assuming ~25 km/day driving)

**Example:** Oil changes at 30k, 40k, 50k km → average interval = 10k km → at 55k now → next due at 60k → 5k km away → ~200 days.

---

### 4.6 `agents/diagnosis.py` — Failure Prediction

**Purpose:** Takes sensor data + maintenance forecast and produces specific failure predictions with probabilities.

Checks 5 components:

| Component | Trigger Condition | Probability | Severity |
|-----------|------------------|-------------|----------|
| **Brake Pads** | Due within 60 days (per forecast) | 87% | RED if <30 days, else YELLOW |
| **Oil & Filter** | Due within 90 days | 72% | YELLOW |
| **Battery** | Voltage < 12.8V (from sensor) | 65% | YELLOW |
| **Tires** | Mileage > 80k km + 35% chance | 58% | YELLOW |
| **Transmission** | Mileage > 120k km + 25% chance | 42% | YELLOW |

Each produces a `PredictedFailure` with probability, estimated days, severity, and a human-readable recommendation.

---

### 4.7 `agents/engagement.py` — Voice Bot Simulation

**Purpose:** Simulates calling the customer to offer a service appointment.

**Flow:**
1. Picks the highest-probability failure from the diagnosis
2. Fills in a conversation template with vehicle-specific details
3. Simulates customer response:
   - RED severity → **85% acceptance** (urgent = customers listen)
   - YELLOW severity → **68% acceptance**
   - GREEN severity → **45% acceptance**

**Note:** This agent logs `sensitivity="sensitive"` because it accesses customer phone numbers — which triggers a UEBA alert by design.

---

### 4.8 `agents/scheduling.py` — Appointment Booking

**Purpose:** Finds available slots across 3 service centers and books the best one.

**Service Centers:**
| Center | Location | Slots |
|--------|----------|-------|
| Center_Delhi_1 | Delhi | 09:00, 10:00, 14:00, 15:00, 16:00 |
| Center_Delhi_2 | Delhi | 09:30, 11:00, 13:00, 15:30, 17:00 |
| Center_Gurgaon | Gurgaon | 08:30, 10:30, 12:00, 14:30, 16:30 |

**Cost calculation:** Sums up component replacement costs + random labor charge (₹500-2000).

---

### 4.9 `agents/feedback.py` — Post-Service Follow-up

**Purpose:** Simulates collecting customer feedback after service completion.

Generated metrics:
- Satisfaction: 7-10 (biased positive — most customers are satisfied)
- Service quality: 3-5
- Technician behavior: 3-5
- Would recommend: True if satisfaction ≥ 8
- Issues resolved: 92% chance
- 30% chance of finding additional issues during service

---

### 4.10 `agents/quality.py` — Manufacturing Feedback Loop

**Purpose:** Analyzes ALL failures across the entire fleet to find patterns. This is the "closed loop" from aftersales back to manufacturing.

**How it works:**
1. Groups all failures by `{vehicle_model}_{component}` (e.g., "Tata Nexon_Brake Pads")
2. If ≥ 2 vehicles share the same pattern → it's a manufacturing issue
3. Generates an RCA insight with:
   - Root cause hypothesis
   - Corrective action plan
   - Priority: CRITICAL (>5 vehicles), HIGH (>3), MEDIUM (≥2)
   - Estimated cost saved = affected vehicles × component cost

---

### 4.11 `ueba.py` — Security Monitor

**Purpose:** Watches everything every agent does and flags suspicious behavior. Prevents compromised agents from accessing unauthorized data.

**Baseline profiles** define what each agent is ALLOWED to do:
```
DataAnalysisAgent  → can READ telematics_db, maintenance_db
DiagnosisAgent     → can EXECUTE prediction_engine
EngagementAgent    → can INITIATE_CALL customer_db
SchedulingAgent    → can QUERY/WRITE service_center_db, booking_db
FeedbackAgent      → can UPDATE customer_db
QualityAgent       → can ACCESS manufacturing_db
```

**Three anomaly checks:**
1. **Wrong resource** (score: 0.85) — Agent touched a database it shouldn't
2. **Wrong action** (score: 0.70) — Agent did something not in its baseline
3. **Sensitive data by non-privileged agent** (score: 0.90) — Only Master and Quality can access "sensitive" data

---

### 4.12 `master.py` — The Orchestrator

**Purpose:** The brain. Creates all agents, dispatches work in parallel, aggregates results, runs security checks.

#### `__init__` — Setup
Creates one instance of each of the 6 agents + the UEBA monitor. Stores the vehicle fleet.

#### `_process_vehicle_parallel(vehicle_id)` — Per-Vehicle Pipeline
This runs for EACH vehicle (inside a thread):
```
Step 1: generate_sensor_data()     → fake sensor snapshot
Step 2: generate_maintenance_history() → fake service records
Step 3: DataAnalysisAgent.execute()    → anomaly detection + forecast
Step 4: DiagnosisAgent.execute()       → failure predictions
Step 5: EngagementAgent.execute()      → call customer
Step 6: SchedulingAgent.execute()      → book appointment (if accepted)
Step 7: FeedbackAgent.execute()        → collect feedback (70% chance)
```

#### `orchestrate_maintenance_cycle()` — Main Loop
```python
with ThreadPoolExecutor(max_workers=6) as executor:
    # Submit ALL 10 vehicles for parallel processing
    futures = {executor.submit(process, vid): vid for vid in vehicle_ids}
    # Collect results as they complete
    for future in as_completed(futures):
        result = future.result()
```
After all vehicles finish: runs UEBA anomaly detection, then RCA/CAPA analysis on the full fleet.

#### `generate_report()` — Executive Summary
Formats a text report with fleet stats, failures predicted, appointments booked, revenue, security status.

---

### 4.13 `main.py` — Entry Point

**Purpose:** The file you actually run. Clean and simple:

```python
def main():
    # 1. Generate 10 synthetic vehicles in Delhi
    vehicles = SyntheticDataGenerator.generate_vehicles(count=10, region="Delhi")

    # 2. Create master agent with 6 workers
    master = MasterAgent(vehicles, max_workers=MAX_WORKERS)

    # 3. Run the full orchestration cycle
    results = master.orchestrate_maintenance_cycle()

    # 4. Print executive report
    print(master.generate_report(results))

    # 5. Save detailed results to JSON
    json.dump(results, open("maintenance_system_results.json", "w"))

    # 6. Print vehicle-level details
    for v in results["vehicles"][:5]:
        print(f"{v['vehicle_id']} | Alert: {v['alert_level']}")
```

---

## 5. HTML Dashboard — `autosense_dashboard.html`

### Structure
Single HTML file with embedded CSS + JS. No server, no build tools, no npm.

```
<html>
├── <style>           ← Dark theme CSS with variables, grid, animations
├── <nav>             ← Top bar: logo, 4 tabs, LIVE badge, simulation button
├── #tab-dashboard    ← Stat cards + fleet table + diagnostic panel
├── #tab-scheduling   ← AI agent activity log + available slots
├── #tab-servicecenter ← Utilization bars + heatmap + appointments
├── #tab-manufacturing ← Defect patterns + failure distribution + UEBA
├── #sim-overlay      ← Animated 8-step simulation modal
└── <script>          ← Mock data arrays + rendering functions + simulation
```

### Key Functions

| Function | What it does |
|----------|-------------|
| `showTab(name)` | Hides all panels, shows the selected one, updates active tab |
| `renderFleet()` | Builds the 12-row vehicle table with health bars and status badges |
| `showDetail(i)` | Click a vehicle → shows 6 sensor cards + failure probability meter |
| `addAgentLog()` | Adds a new log line to the agent activity feed (cycles through events) |
| `renderSlots()` | Shows 3 service centers with clickable available time slots |
| `renderServiceCenter()` | Utilization bars + hourly capacity heatmap + appointment cards |
| `renderManufacturing()` | 3 defect pattern cards with RCA/CAPA status + failure bar chart |
| `runSimulation()` | Animates 8 steps (1.4s each): detect → diagnose → call → book → RCA → UEBA |

### Mock Data

| Array | Count | Content |
|-------|-------|---------|
| `VEHICLES` | 12 | 3 RED, 4 YELLOW, 5 GREEN — each with sensor values, health score, issues |
| `APPOINTMENTS` | 5 | Pre-loaded bookings with time, vehicle, issue, technician |
| `DEFECTS` | 3 | RCA patterns: brake wear, battery drain, tire pressure loss |
| `CENTERS` | 3 | Delhi 1, Delhi 2, Gurgaon — with utilization % and slot times |

---

## 6. How to Run the Project

### Python Backend
```bash
cd c:\Users\HP\Programming\Auto
python main.py
```
**Output:** Console logs → executive report → `maintenance_system_results.json`

### HTML Dashboard
Double-click `autosense_dashboard.html` — opens in browser, zero setup.

---

## 7. Feature-to-Business Mapping

| Code File | Function | Business Problem | Business Value |
|-----------|----------|-----------------|----------------|
| `agents/data_analysis.py` | `analyze_sensor_data()` | Detecting anomalies before breakdown | 40-50% fewer unplanned failures |
| `agents/diagnosis.py` | `predict_failures()` | Predicting failures 14-60 days early | ₹50-105 Cr warranty savings |
| `agents/engagement.py` | `engage_customer()` | Proactive voice outreach | 75% acceptance vs 45% for SMS |
| `agents/scheduling.py` | `schedule_appointment()` | Automated booking | Service center utilization: 40% → 85% |
| `agents/feedback.py` | `collect_feedback()` | Post-service quality tracking | NPS: 45 → 75 |
| `agents/quality.py` | `analyze_defect_patterns()` | Manufacturing feedback loop | 80% faster defect detection |
| `ueba.py` | `detect_anomalies()` | Security for autonomous AI | Prevents unauthorized data access |
| `master.py` | `orchestrate_maintenance_cycle()` | Parallel fleet processing | 10+ vehicles/sec throughput |

---

> **Document Version:** 2.0 (Updated for modular structure)
> **Project:** AutoSense AI — EY Techathon 6.0
