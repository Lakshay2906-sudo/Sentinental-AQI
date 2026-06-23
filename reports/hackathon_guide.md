# SYSTEM ARCHITECTURE, DATABASE SCHEMAS & DEPLOYMENT GUIDE

This document summarizes the technological architecture, database tables, and free hosting pipelines required to deploy the **Sentinel-AQI** remote monitoring platform.

---

## 🗺️ System Architecture Diagram

This ASCII map highlights data flows from remote orbits down to the client browsers:

```text
  [Copernicus Sentinel-5P]        [NASA Earth Observing System]
             |                                 |
             | tropospheric                    | thermal fire
             | columns (VCD)                   | anomalies (FIRMS)
             v                                 v
   =======================================================
   ||         GOOGLE EARTH ENGINE CLOUD PLATFORM        || -- Ingestion & Reduction
   =======================================================
                             |
                             | Export multivariant rasters (GeoTIFF)
                             v
   =======================================================
   ||             CLOUD DATA PROCESSING PIPELINE        || -- rasterio, xarray,
   ||                                                   ||    geopandas (Python)
   =======================================================
         |                             |
         | Convert column to surface   | DBSCAN pixel grouping &
         | CPCB AQI approximations     | ML Predictors (Scikit-Learn/XGBoost)
         v                             v
   =======================================================
   ||             PERSISTENT STAGING DATABASE           || -- PostgreSQL / SQLite
   =======================================================
                             |
                             | SQL Queries / GeoDataFrame reads
                             v
   =======================================================
   ||               STREAMLIT DATA INTERFACE            || -- Plotly scattergeos, 
   ||                                                   ||    folium mapping overlays
   =======================================================
                             |
                             v
                  [COLLEGE HACKATHON PREVIEW]
```

---

## 🗄️ Database Schema Design

For staging daily gridded averages, boundary anomalies, and ground validation data, we recommend a lightweight **PostgreSQL** or **SQLite** relational structure.

### 1. Table: `regional_air_grids`
Holds calculated continuous grid data aggregated by district boundaries.

```sql
CREATE TABLE regional_air_grids (
    grid_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    district_name VARCHAR(100) NOT NULL,
    latitude DEF_NUMERIC(10, 6) NOT NULL,
    longitude DEF_NUMERIC(10, 6) NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    no2_column_density DOUBLE PRECISION,   -- mol/m2 from Sentinel-5P
    so2_column_density DOUBLE PRECISION,   -- mol/m2 from Sentinel-5P
    co_column_density DOUBLE PRECISION,    -- mol/m2 from Sentinel-5P
    o3_column_density DOUBLE PRECISION,    -- mol/m2 from Sentinel-5P
    hcho_column_density DOUBLE PRECISION,  -- mol/m2 from Sentinel-5P
    fire_count INTEGER DEFAULT 0,          -- Count from NASA FIRMS in polygon
    calculated_aqi INTEGER,                -- Piecewise linear CPCB output
    aqi_category VARCHAR(30),              -- Good / Satisfactory / Moderate etc.
    risk_score NUMERIC(5, 2)               -- Predictive hazard coefficient
);

CREATE INDEX idx_spatial_coords ON regional_air_grids (latitude, longitude);
CREATE INDEX idx_temporal_trend ON regional_air_grids (timestamp);
```

### 2. Table: `cpcb_ground_validation`
Stores historical reference monitors validation datasets to evaluate model error margins.

```sql
CREATE TABLE cpcb_ground_validation (
    station_id VARCHAR(50) PRIMARY KEY,
    station_name VARCHAR(250) NOT NULL,
    state_name VARCHAR(100) NOT NULL,
    ground_no2_ugm3 NUMERIC(6, 2),
    ground_so2_ugm3 NUMERIC(6, 2),
    ground_co_mgm3 NUMERIC(4, 2),
    ground_o3_ugm3 NUMERIC(6, 2),
    ground_aqi_value INTEGER,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL
);
```

### 3. Table: `detected_hotspots`
Saves spatial hotspot clusters detected by DBSCAN algorithms daily.

```sql
CREATE TABLE detected_hotspots (
    cluster_id INTEGER NOT NULL,
    centroid_lat NUMERIC(10, 6) NOT NULL,
    centroid_lon NUMERIC(10, 6) NOT NULL,
    average_hcho_density DOUBLE PRECISION NOT NULL,
    active_fire_count INTEGER DEFAULT 0,
    month_index INTEGER NOT NULL,
    hazard_level VARCHAR(30), -- High / Medium / Low
    observed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
```

---

## ☁️ Zero-Cost Cloud Deployment Guide

To deploy the unified system for hackathon submissions without incurring billing:

### Option A: Streamlit Community Cloud (Recommended for python)
1. Push your full repository directly to a public **GitHub** repository containing `/requirements.txt` and `/app.py`.
2. Visit [share.streamlit.io](https://share.streamlit.io) and authenticate with your GitHub credentials.
3. Select "New App", specify standard details:
   - **Repository**: Your GitHub project URL
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **Deploy**. Your live dashboard will be accessible via a `*.streamlit.app` subdomain in under 2 minutes.

### Option B: Render Web Service (Free Tier)
1. Register on [Render.com](https://render.com). Link your GitHub repository.
2. Select **New Web Service**. Set configuration parameters:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3. Click "Create Web Service". Render will provision a container and auto-deploy your Streamlit dashboard for free.
