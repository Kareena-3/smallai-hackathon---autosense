-- CreateTable
CREATE TABLE "VehicleTelemetry" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "timestamp" DATETIME NOT NULL,
    "vehicle_id" TEXT NOT NULL,
    "make" TEXT NOT NULL,
    "model" TEXT NOT NULL,
    "engine_rpm" REAL NOT NULL,
    "lub_oil_pressure" REAL NOT NULL,
    "fuel_pressure" REAL NOT NULL,
    "coolant_pressure" REAL NOT NULL,
    "lub_oil_temp" REAL NOT NULL,
    "coolant_temp" REAL NOT NULL,
    "engine_condition" INTEGER NOT NULL,
    "brake_wear_pct" REAL NOT NULL,
    "failure_prob" REAL NOT NULL
);

-- CreateIndex
CREATE INDEX "VehicleTelemetry_vehicle_id_idx" ON "VehicleTelemetry"("vehicle_id");

-- CreateIndex
CREATE INDEX "VehicleTelemetry_timestamp_idx" ON "VehicleTelemetry"("timestamp");
