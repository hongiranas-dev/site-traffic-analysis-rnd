"""Refresh the architect dashboard using a new TomTom traffic snapshot."""
import os
from dotenv import load_dotenv

load_dotenv()

from architect_dashboard_generator import generate_dashboard
from direction_analyzer import analyze_directions
from final_insight_generator import generate_report
from final_map_generator import create_final_map
from iudx_live_collector import collect_bmtc_positions
from osm_extractor import extract_roads
from traffic_integrator import analyze_site_traffic


def refresh_live_dashboard():
    if not os.getenv("TOMTOM_API_KEY"):
        raise RuntimeError(
            "Set TOMTOM_API_KEY in this Command Prompt window before refreshing "
            "the live dashboard."
        )

    print("Collecting a fresh TomTom traffic snapshot...")
    analyze_site_traffic(extract_roads())

    if os.getenv("IUDX_CLIENT_ID") and os.getenv("IUDX_CLIENT_SECRET"):
        try:
            print("Collecting an IUDX BMTC vehicle-position snapshot...")
            collect_bmtc_positions()
        except (RuntimeError, ValueError, OSError) as error:
            print(f"IUDX BMTC collection skipped: {error}")
    analyze_directions()
    generate_report()
    generate_dashboard()
    create_final_map()

    print("\nRefresh complete.")
    print("Open outputs/architect_dashboard.html for the live source panel.")
    print("Open outputs/final_circulation_map.html for the final site report.")


if __name__ == "__main__":
    refresh_live_dashboard()
