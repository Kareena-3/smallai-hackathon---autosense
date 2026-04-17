require("dotenv/config");
const { PrismaClient } = require("@prisma/client");
const { PrismaBetterSqlite3 } = require("@prisma/adapter-better-sqlite3");
const path = require("path");

// Resolve the DB file path from DATABASE_URL (format: "file:./dev.db")
const dbUrl = process.env.DATABASE_URL || "file:./dev.db";
const dbPath = dbUrl.replace("file:", "");
const resolvedPath = path.resolve(__dirname, "..", dbPath.startsWith("./") ? dbPath : dbPath);

const adapter = new PrismaBetterSqlite3({ url: `file:${resolvedPath}` });
const prisma = new PrismaClient({ adapter });

/**
 * Deterministic failure probability formula.
 * Weighted risk score from 0-100 based on sensor readings.
 */
function computeFailureProbability(r) {
    const rpmRisk = Math.min(r.engine_rpm / 5000, 1.0);
    const oilRisk = Math.max(0, 1 - r.lub_oil_pressure / 5.0);
    const fuelRisk = Math.max(0, 1 - r.fuel_pressure / 60.0);
    const coolantPRisk = Math.max(0, 1 - r.coolant_pressure / 35.0);
    const oilTempRisk = Math.min(r.lub_oil_temp / 140.0, 1.0);
    const coolantTempRisk = Math.min(r.coolant_temp / 120.0, 1.0);
    const brakeRisk = r.brake_wear_pct / 100.0;
    const engineRisk = r.engine_condition === 1 ? 0 : 1;

    const prob =
        0.10 * rpmRisk +
        0.15 * oilRisk +
        0.10 * fuelRisk +
        0.10 * coolantPRisk +
        0.15 * oilTempRisk +
        0.15 * coolantTempRisk +
        0.20 * brakeRisk +
        0.05 * engineRisk;

    return Math.round(Math.min(100, Math.max(0, prob * 100)) * 10) / 10;
}

const vehicles = [
    { timestamp: "2026-04-14T10:00:01Z", vehicle_id: "MH-01-AV-4421", make: "Tata", model: "Nexon EV", engine_rpm: 0, lub_oil_pressure: 0.0, fuel_pressure: 0.0, coolant_pressure: 24.2, lub_oil_temp: 32.5, coolant_temp: 35.1, engine_condition: 1, brake_wear_pct: 12.4 },
    { timestamp: "2026-04-14T10:00:02Z", vehicle_id: "DL-03-CC-9901", make: "Maruti", model: "Brezza", engine_rpm: 3200, lub_oil_pressure: 1.4, fuel_pressure: 38.5, coolant_pressure: 19.2, lub_oil_temp: 122.1, coolant_temp: 108.4, engine_condition: 0, brake_wear_pct: 88.2 },
    { timestamp: "2026-04-14T10:00:03Z", vehicle_id: "KA-05-BN-1122", make: "Mahindra", model: "XUV700", engine_rpm: 2100, lub_oil_pressure: 4.2, fuel_pressure: 56.3, coolant_pressure: 30.1, lub_oil_temp: 94.2, coolant_temp: 88.5, engine_condition: 1, brake_wear_pct: 45.1 },
    { timestamp: "2026-04-14T10:00:04Z", vehicle_id: "MH-12-DE-5566", make: "Tata", model: "Safari", engine_rpm: 2400, lub_oil_pressure: 4.0, fuel_pressure: 55.1, coolant_pressure: 29.4, lub_oil_temp: 96.4, coolant_temp: 91.2, engine_condition: 1, brake_wear_pct: 10.2 },
    { timestamp: "2026-04-14T10:00:05Z", vehicle_id: "DL-01-ZZ-0007", make: "Maruti", model: "Swift", engine_rpm: 3800, lub_oil_pressure: 0.9, fuel_pressure: 32.4, coolant_pressure: 14.2, lub_oil_temp: 130.2, coolant_temp: 115.6, engine_condition: 0, brake_wear_pct: 92.1 },
    { timestamp: "2026-04-14T10:00:06Z", vehicle_id: "HR-26-AQ-8877", make: "Mahindra", model: "Thar", engine_rpm: 1800, lub_oil_pressure: 3.9, fuel_pressure: 54.8, coolant_pressure: 28.9, lub_oil_temp: 92.5, coolant_temp: 86.4, engine_condition: 1, brake_wear_pct: 15.3 },
    { timestamp: "2026-04-14T10:00:07Z", vehicle_id: "UP-16-BK-1234", make: "Hyundai", model: "Creta", engine_rpm: 2000, lub_oil_pressure: 4.1, fuel_pressure: 55.9, coolant_pressure: 30.2, lub_oil_temp: 93.8, coolant_temp: 87.9, engine_condition: 1, brake_wear_pct: 22.4 },
    { timestamp: "2026-04-14T10:00:08Z", vehicle_id: "MH-04-ET-5678", make: "Toyota", model: "Innova Hycross", engine_rpm: 1500, lub_oil_pressure: 3.8, fuel_pressure: 54.2, coolant_pressure: 28.5, lub_oil_temp: 90.1, coolant_temp: 84.2, engine_condition: 1, brake_wear_pct: 34.8 },
    { timestamp: "2026-04-14T10:00:09Z", vehicle_id: "DL-08-CA-1111", make: "Kia", model: "Seltos", engine_rpm: 4100, lub_oil_pressure: 1.2, fuel_pressure: 35.1, coolant_pressure: 17.4, lub_oil_temp: 128.4, coolant_temp: 114.2, engine_condition: 0, brake_wear_pct: 76.5 },
    { timestamp: "2026-04-14T10:00:10Z", vehicle_id: "KA-01-MJ-9999", make: "Tata", model: "Tiago EV", engine_rpm: 0, lub_oil_pressure: 0.0, fuel_pressure: 0.0, coolant_pressure: 22.1, lub_oil_temp: 30.4, coolant_temp: 32.8, engine_condition: 1, brake_wear_pct: 8.9 },
];

async function main() {
    console.log("Seeding database...");

    await prisma.vehicleTelemetry.deleteMany();

    for (const v of vehicles) {
        const failProb = computeFailureProbability(v);
        await prisma.vehicleTelemetry.create({
            data: {
                timestamp: new Date(v.timestamp),
                vehicle_id: v.vehicle_id,
                make: v.make,
                model: v.model,
                engine_rpm: v.engine_rpm,
                lub_oil_pressure: v.lub_oil_pressure,
                fuel_pressure: v.fuel_pressure,
                coolant_pressure: v.coolant_pressure,
                lub_oil_temp: v.lub_oil_temp,
                coolant_temp: v.coolant_temp,
                engine_condition: v.engine_condition,
                brake_wear_pct: v.brake_wear_pct,
                failure_prob: failProb,
            },
        });
        console.log(`  OK ${v.vehicle_id} (${v.make} ${v.model}) - failure_prob: ${failProb}%`);
    }

    console.log("\nSeeded 10 vehicle records successfully.");
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
