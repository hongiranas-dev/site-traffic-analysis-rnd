from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Site Traffic Analysis API",
    description="Backend API for architect site traffic analysis",
    version="1.0.0"
)
app.mount(
    "/dashboard",
    StaticFiles(directory="outputs", html=True),
    name="dashboard"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def read_json_file(filename):
    filepath = os.path.join("outputs", filename)

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail=f"{filename} not found"
        )

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Site Traffic Analysis API is running"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# TRAFFIC
# --------------------------------------------------

@app.get("/api/traffic")
def get_traffic():
    return read_json_file("traffic_report.json")


# --------------------------------------------------
# DIRECTIONS
# --------------------------------------------------

@app.get("/api/directions")
def get_directions():
    return read_json_file("direction_analysis.json")


# --------------------------------------------------
# TRAFFIC SIGNALS
# --------------------------------------------------

@app.get("/api/signals")
def get_signals():
    return read_json_file("traffic_signals.json")


# --------------------------------------------------
# ZONING
# --------------------------------------------------

@app.get("/api/zoning")
def get_zoning():
    return read_json_file("zoning_analysis.json")


# --------------------------------------------------
# PEDESTRIAN
# --------------------------------------------------

@app.get("/api/pedestrian")
def get_pedestrian():
    return read_json_file("pedestrian_analysis.json")


# --------------------------------------------------
# FINAL INSIGHTS
# --------------------------------------------------

@app.get("/api/insights")
def get_insights():
    return read_json_file("final_architect_report.json")