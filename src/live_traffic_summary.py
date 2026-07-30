"""Summarise the TomTom snapshot and discovered IUDX traffic resources."""

import json
from datetime import datetime, timezone
from pathlib import Path


TRAFFIC_REPORT_PATH = Path("outputs/traffic_report.json")
IUDX_CATALOGUE_PATH = Path("outputs/iudx_catalogue_search.json")
IUDX_BMTC_POSITIONS_PATH = Path("outputs/iudx_live_bmtc_positions.json")
STALE_AFTER_MINUTES = 20


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot_status(path):
    if not path.exists():
        return {"available": False, "message": "No TomTom snapshot has been collected."}

    collected_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    age_minutes = round((datetime.now(timezone.utc) - collected_at).total_seconds() / 60)
    return {
        "available": True,
        "collected_at_utc": collected_at.isoformat(),
        "age_minutes": age_minutes,
        "fresh": age_minutes <= STALE_AFTER_MINUTES,
    }


def find_iudx_resource(documents, name):
    for document in documents:
        if document.get("name") == name:
            return document
    return None


def catalogue_documents():
    searches = load_json(IUDX_CATALOGUE_PATH, [])
    return [document for search in searches for document in search.get("documents", [])]


def iudx_bmtc_snapshot():
    snapshot = load_json(IUDX_BMTC_POSITIONS_PATH, {})
    if isinstance(snapshot, list):
        snapshot = {"vehicle_positions": snapshot}
    positions = snapshot.get("vehicle_positions", [])
    if not snapshot:
        return {
            "available": False,
            "vehicle_count": 0,
            "message": "No authenticated BMTC position snapshot has been collected.",
        }
    return {
        "available": True,
        "vehicle_count": len(positions),
        "collected_at_utc": snapshot.get("collected_at_utc"),
        "resource_id": snapshot.get("resource_id"),
    }


def build_live_traffic_summary():
    roads = load_json(TRAFFIC_REPORT_PATH, [])
    tomtom_snapshot = snapshot_status(TRAFFIC_REPORT_PATH)
    congestion_indexes = [
        road["free_flow_speed"] / road["current_speed"]
        for road in roads
        if road.get("current_speed", 0) > 0 and road.get("free_flow_speed", 0) > 0
    ]
    live_roads = sum(road.get("traffic_status") != "LOW TRAFFIC" for road in roads)

    documents = catalogue_documents()
    bmtc_resource = find_iudx_resource(documents, "live-bus-position-bmtc")
    event_resource = find_iudx_resource(documents, "road-traffic-events")

    iudx = {
        "catalogue_checked": IUDX_CATALOGUE_PATH.exists(),
        "bmtc_live_positions": {
            "discovered": bmtc_resource is not None,
            "resource_id": bmtc_resource.get("id") if bmtc_resource else None,
            "access_policy": bmtc_resource.get("accessPolicy") if bmtc_resource else None,
            **iudx_bmtc_snapshot(),
            "status": "Live BMTC positions collected."
            if iudx_bmtc_snapshot()["available"]
            else (
                "Credentials required before live BMTC positions can be collected."
                if bmtc_resource
                else "BMTC live-position resource was not found in the catalogue output."
            ),
        },
        "traffic_events": {
            "discovered": event_resource is not None,
            "resource_id": event_resource.get("id") if event_resource else None,
            "access_policy": event_resource.get("accessPolicy") if event_resource else None,
            "status": (
                "Open IUDX traffic-event resource discovered; live retrieval still needs IUDX client credentials."
                if event_resource
                else "Bengaluru traffic-event resource was not found in the catalogue output."
            ),
        },
    }

    return {
        "tomtom": {
            "snapshot": tomtom_snapshot,
            "roads_analyzed": len(roads),
            "average_current_speed_kmph": round(
                sum(road.get("current_speed", 0) for road in roads) / len(roads), 1
            )
            if roads
            else None,
            "average_congestion_index": round(
                sum(congestion_indexes) / len(congestion_indexes), 2
            )
            if congestion_indexes
            else None,
            "roads_with_slowdown": live_roads,
        },
        "iudx": iudx,
    }
