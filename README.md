# site-traffic-analysis-rnd
Geospatial R&amp;D prototype for site-level traffic impact analysis using OSM data
# Vehicular & Pedestrian Circulation Analysis - R&D Prototype

## Overview

This project is an R&D exploration focused on generating data-driven site circulation insights for architects during the early design analysis phase.

Architects often rely on manual surveys or assumptions to understand vehicular movement, pedestrian activity, congestion patterns, and suitable entry/exit planning around a site.

This system explores how geospatial data, traffic APIs, graph analytics, and contextual intelligence can transform raw location data into architectural decision insights.

---

# Objective

Given a site coordinate, analyze the surrounding 1 km radius and generate insights for:

- Vehicular circulation patterns
- Road network complexity
- Traffic congestion impact
- Conflict/bottleneck identification
- Traffic signal influence
- Pedestrian activity estimation
- Context-aware entry/exit planning

---

# System Architecture

```text

                         Site Coordinates
                                |
                                |
                                v
                    +-----------------------+
                    |  OpenStreetMap (OSM)  |
                    |  Road Data Extraction |
                    +-----------------------+
                                |
                                v
                    +-----------------------+
                    | Road Network Graph    |
                    | Nodes = Intersections |
                    | Edges = Roads         |
                    +-----------------------+
                                |
              -------------------------------------
              |                                   |
              v                                   v

    +--------------------+             +--------------------+
    | TomTom Traffic API |             | Context Analysis   |
    |                    |             |                    |
    | Real-time Speed    |             | Zoning Detection   |
    | Free Flow Speed    |             | Land Use Impact    |
    | Peak Analysis      |             +--------------------+
    +--------------------+
              |
              v

      +-------------------+
      | Traffic Analysis  |
      | Engine            |
      |                   |
      | - Road Risk       |
      | - Congestion      |
      | - Conflict Points |
      +-------------------+
              |
              v

      +-----------------------+
      | Pedestrian Estimation |
      |                       |
      | Transit proximity     |
      | Amenities             |
      | Activity generators   |
      +-----------------------+
              |
              v

      +-------------------------+
      | Circulation Insight     |
      | Generation Engine       |
      |                         |
      | Entry Recommendation    |
      | Safety Suggestions      |
      +-------------------------+
              |
              v

        Architect Dashboard
        (Interactive Map + JSON)

```

---

# Implemented Modules

## 1. Road Network Extraction

File:

```
osm_extractor.py
```

Purpose:

Extracts the road network around a site using OpenStreetMap data.

Implementation:

- 1 km radius extraction
- Road geometry collection
- Road hierarchy identification

---

## 2. Graph Based Road Analysis

Files:

```
road_analyzer.py
conflict_visualizer.py
```

Purpose:

Models road infrastructure as a graph.

Concept:

```
Intersections = Nodes

Road Connections = Edges
```

Used for:

- Junction complexity analysis
- Conflict point identification
- Bottleneck detection

---

## 3. Real-Time Traffic Integration

Files:

```
traffic_api.py
traffic_integrator.py
```

Data Source:

TomTom Traffic API

Collected parameters:

- Current traffic speed
- Free-flow speed
- Traffic condition

Example:

```
Current Speed: 30 km/h

Free Flow Speed: 40 km/h

Traffic Status: Moderate
```

---

## 4. Peak / Off-Peak Traffic Analysis

File:

```
traffic_history_analyzer.py
```

Purpose:

Creates a pipeline for analyzing movement variation based on time.

Categories:

- Morning peak movement
- Evening peak movement
- Off-peak movement

---

## 5. Traffic Signal Mapping

File:

```
signal_analyzer.py
```

Purpose:

Detects nearby traffic control points.

Uses:

- OSM traffic signal data
- Junction influence analysis

---

## 6. Contextual Zoning Analysis

File:

```
zoning_analyzer.py
```

Purpose:

Traffic behavior changes based on land usage.

Classifies areas into:

- Residential
- Commercial
- Mixed-use

Factors considered:

- Buildings
- Shops
- Offices
- Public amenities

---

## 7. Pedestrian Flow Estimation

File:

```
pedestrian_estimator.py
```

Current approach:

Proxy-based estimation.

Factors:

- Bus stops
- Transit availability
- Shops
- Public facilities

Output:

```
Low / Medium / High Pedestrian Activity
```

---

## 8. Final Circulation Insight Engine

Files:

```
final_insight_generator.py
architect_dashboard_generator.py
```

Generates:

- Recommended entry direction
- Roads to avoid
- Safety suggestions
- Pedestrian segregation recommendations

Example:

```
Recommended Entry:
North-East side access

Avoid:
High traffic main road side

Reason:
- Commercial movement
- Signal congestion
- Pedestrian activity
```

---



## Interactive Dashboard

```
architect_dashboard.html
![alt text](image.png)
```

Includes:

- Traffic risk points
- Signal locations
- Circulation recommendations
- Site-level insights

---

# Current Limitations

Since this is an R&D prototype:

## Traffic Volume

Current:

Uses speed-based congestion estimation.

Future:

Integrate actual vehicle count / flow volume datasets.

---

## Pedestrian Analysis

Current:

Uses location-based proxy estimation.



---

## Zoning Classification

Current:

Rule-based classification using OSM metadata.

Future:

Machine Learning based land-use classification.

---


---

# Future Improvements

- Cloud deployment using GCP/AWS
- API based architecture
- Database storage for historical analysis
- ML based pedestrian prediction
- Computer vision traffic analysis
- Automated entry/exit optimization
- Advanced heatmap generation

---

# Research Status

Completed:

- Road network extraction
- Traffic API integration
- Graph-based analysis
- Conflict identification
- Traffic signal mapping
- Zoning context analysis
- Pedestrian estimation prototype
- Architect insight generation

Future Research:

- ML based prediction models
- Large-scale deployment architecture
- 
Explore ML approaches:

- Computer vision based pedestrian counting
- CCTV/video analysis
- Object detection models
- Movement prediction
  <img width="800" height="858" alt="image" src="https://github.com/user-attachments/assets/d60daa94-7129-47c8-9a95-5a9c5c6c6c46" />


---

