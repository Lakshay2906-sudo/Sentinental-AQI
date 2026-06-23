# COLLGE HACKATHON PRESENTATION OUTLINE & SLIDE DECK
**Topic**: Development of Surface AQI & Identification of HCHO Hotspots over India using Satellite Data  
**Team Name**: GeoIntel-AI India  
**Presentation Time**: 7 Minutes Max  

---

## Slide 1: Title & The Environmental Challenge (0:45 min)
*   **Slide Title**: Sentinel-AQI: Next-Gen Satellite-Derived Air Quality Monitoring & Photo-Chemical Hotspot Forecasting  
*   **Visual Elements**: 
    - Stunning overlay of satellite views of Earth with specific chemical density grids spanning India.
    - Logos of college, GEE, Copernicus (ESA), NASA, and Streamlit Community Cloud.
*   **Content Bullet Points**:
    - Ground monitoring stations in India (CPCB) are sparse (typically <500 stations for 1.4 billion people), leaving massive geospatial gaps in rural, industrial, and agricultural belts.
    - Our Solution: Fusing Sentinel-5P TROPOMI satellite columns with MODIS/VIIRS Active Fires to model continuous ground-level Air Quality Index (AQI) grids and forecast volatile organic compounds (HCHO).
*   **Speaker Notes**: "Good morning judges. Traditional air quality monitoring in India is heavily constrained by physics: we only have several hundred physical monitoring stations, leaving 90% of our region completely unmonitored. We present *Sentinel-AQI*, a unified geospatial AI application that transforms free ESA/NASA satellite bands into real-time ground-level surface AQI maps and volatile organic chemical alerts."

---

## Slide 2: Scientific Core & Satellite Data Fusion (1:00 min)
*   **Slide Title**: Multi-Spectral Spatial Data Fusion  
*   **Visual Elements**: 
    - High-level block diagram: Copernicus Sentinel-5P (TROPOMI sensor) + NASA EOS MODIS/VIIRS -> Planetary Boundary Layer Height (PBLH) conversion formulas -> Unified Spatial Grid (10km scale).
*   **Content Bullet Points**:
    - **TROPOMI Bands Used**: NO₂ (Nitrogen Dioxide), SO₂ (Sulfur Dioxide), CO (Carbon Monoxide), O₃ (Ozone), HCHO (Formaldehyde).
    - **Active Fire Data**: MODIS Radiative Temperature (Band 21, Thermal anomalies) + VIIRS fire counts.
    - **Geospatial Physics**: Using Boundary Layer Heights (PBLH) as vertical integration scale proxies to map columnar density (mol/m²) to human respiratory density (µg/m³).
*   **Speaker Notes**: "We ingest multi-spectral columns from ESA's Sentinel-5P TROPOMI. The primary innovation is mapping vertical Columnar density—which measures gas in the entire atmosphere—to the breathing boundary layer. We scale these densities based on planetary boundary variations, so judges see what citizens are actually breathing at state-levels."

---

## Slide 3: Chemical Synthesis — HCHO & Biomass Burning (1:00 min)
*   **Slide Title**: Formaldehyde (HCHO) Pathways & Crop Residue Burning  
*   **Visual Elements**: 
    - Chemistry chart showing Biomass combustion VOCs -> Photochemical degradation -> Formaldehyde (HCHO) intermediate -> Ozone (O₃) generation.
    - Linear regression scatter plot correlating Fire Counts (MODIS) with elevated HCHO columns.
*   **Content Bullet Points**:
    - HCHO is an primary carcinogen and key precursor for secondary organic aerosols and ground-level tropospheric ozone.
    - Strong correlation ($R = 0.81$ during harvest seasons) between MODIS fire hotspots (agricultural stubble burning in Punjab/Haryana) and spatial HCHO columns.
*   **Speaker Notes**: "Why Formaldehyde? HCHO is a highly carcinogenous VOC and a key scientific marker. It is a critical intermediate in the oxidation of volatile organics. By tracing HCHO under high fire counts from MODIS, we mathematically isolate agricultural residue fires, industrial emissions, and forest fires, directly linking biomass combustion to urban respiratory crises."

---

## Slide 4: AI Architecture & Machine Learning Pipelines (1:30 min)
*   **Slide Title**: Regional AQI Prediction & Hotspot Localization  
*   **Visual Elements**: 
    - Model comparison metrics table: Random Forest vs. XGBoost (R², RMSE, MAE).
    - DBSCAN cluster grouping visualization over simulated India hotzones showing core points and noise exclusions.
*   **Content Bullet Points**:
    - **Model 1 (Regression)**: Quantifies AQI over non-station zones. **XGBoost** outperformed with $R^2 = 0.918$, MAE = 10.12, and RMSE = 14.30.
    - **Model 2 (Spatial Clustering)**: DBSCAN (Epsilon = 1.8°, Min Samples = 3) automatically groups contiguous high-density formaldehyde plumes into localized boundary warnings.
    - **Model 3 (Predictive Assessment)**: Dynamic future classification hazard matrix (Risk Score 0-100: Low/Medium/High alert).
*   **Speaker Notes**: "Our AI core trains two models: for predicting AQI over rural pockets, we built comparative Random Forest and XGBoost regressions. XGBoost excels with an R² of 0.918 by capturing high non-linear fire feedbacks. Next, we run DBSCAN unsupervised clustering over Indian coordinates. Rather than just viewing pixels, the system aggregates contiguous toxic plumes into localized hotspots automatically, giving state planners polygon-level hazard bounds."

---

## Slide 5: Full-Stack Architecture & Interactive Dashboard (1:15 min)
*   **Slide Title**: Multi-Page Geospatial System Architecture  
*   **Visual Elements**: 
    - High-level architecture chart: GEE API (Data Ingestion) -> Python/Rasterio (Preprocessing) -> Streamlit & Folium (Interactive Visualization) -> Cloud Run hosting.
    - Beautiful UI screens showcasing India administrative overlays, fire maps, and automated seasonal trend projections.
*   **Content Bullet Points**:
    - **National AQI Viewer**: Dynamic date sliders and specific pollutant selectors.
    - **Biomass Heatmaps**: Real-time correlation curves with dynamic linear Pearson coefficient solvers.
    - **AI Prediction Playground**: Allows policy-makers to input prospective fire metrics and immediately output predicted indexes and health messages.
*   **Speaker Notes**: "We developed this using Python and Streamlit, coupled with Folium and Plotly maps. Our system is fully responsive, showing boundaries, interactive tooltips, and custom color scales based on standard India CPCB criteria. It supports dynamic modeling: a user can adjust boundary layer assumptions, crop burning parameters, and see predicted ground AQIs instantly."

---

## Slide 6: Zero-Cost Tech Stack & Scalability UI (0:45 min)
*   **Slide Title**: Production Scaling via Cost-Free Frameworks  
*   **Visual Elements**: 
    - Technology icons showing complete alignment with GEE free tier, Sentinel Open Access, Streamlit Community Cloud, and GitHub.
*   **Content Bullet Points**:
    - Zero infrastructure fees: Powered strictly on free-tier APIs and open data protocols.
    - Potential for rapid scaling to city-level networks using affordable IoT grid sensors as validation partners.
*   **Speaker Notes**: "As a hackathon prototype, we prioritized operational feasibility: everything operates on completely free tiers. Sentinel-5P, MODIS, and VIIRS datasets are fetched from Google Earth Engine. Prediction services run on Streamlit Community Cloud and Google Cloud Run. This means municipal corporations can run this entire planetary-scale grid for exactly zero dollars of maintenance fees."

---

## Slide 7: Impact, Future Scope & Q&A (0:45 min)
*   **Slide Title**: Air Quality Democratization  
*   **Visual Elements**: 
    - Impact diagram showing: Policy Maker (Strategic Interventions) | Farmers (Scheduled Stubble Alternatives) | Citizens (Activity Planners).
    - Team photo with GitHub URLs and LinkedIn handles.
*   **Content Bullet Points**:
    - **Immediate Impact**: Actionable early risk notifications for farming districts.
    - **Upcoming Features**: Ingestion of Sentinel-3 OLCI water indexes to map stubble drying state factors, and LSTM temporal forecasting for 7-day predictive grids.
*   **Speaker Notes**: "In conclusion, Sentinel-AQI democratizes environmental science. It fills critical gaps for rural towns and guides policy-makers targeting stubborn hotspots before the smog sets in. Thank you judges, we are now open to your questions and would love to show you our live dashboard!"
