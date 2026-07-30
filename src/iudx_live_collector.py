"""Fetch the latest authenticated BMTC vehicle-position snapshot from IUDX."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


BMTC_LIVE_POSITION_RESOURCE_ID = "8a9c53c2-7291-454e-b173-2d9bfe893eb1"
OUTPUT_PATH = Path("outputs/iudx_live_bmtc_positions.json")


def collect_bmtc_positions():
    client_id = os.getenv("IUDX_CLIENT_ID")
    client_secret = os.getenv("IUDX_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "Set IUDX_CLIENT_ID and IUDX_CLIENT_SECRET before collecting BMTC positions."
        )

    try:
        from iudx.auth.Token import Token
        from iudx.entity.Entity import Entity
    except ImportError as error:
        raise RuntimeError(
            "Run this using the project virtual environment after installing the IUDX SDK."
        ) from error

    token = Token(client_id=client_id, client_secret=client_secret)
    entity = Entity(entity_id=BMTC_LIVE_POSITION_RESOURCE_ID, token_obj=token)
    positions = entity.latest()

    payload = {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "IUDX live-bus-position-bmtc",
        "resource_id": BMTC_LIVE_POSITION_RESOURCE_ID,
        "vehicle_positions": json.loads(positions.to_json(orient="records", date_format="iso")),
    }
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Collected {len(payload['vehicle_positions'])} BMTC vehicle positions.")
    print(f"Saved: {OUTPUT_PATH}")
    return payload


if __name__ == "__main__":
    collect_bmtc_positions()
