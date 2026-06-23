# STEP-BY-STEP LIVE DEMONSTRATION GUIDE & NARRATIVE
**Topic**: "Development of Surface AQI & Identification of HCHO Hotspots over India using Satellite Data"  
**Target Audience**: College Hackathon Evaluation Committee  
**Speaker Strategy**: High Energy, Professional, Showing Interactive Sliders and Real-time Processing.

---

## Part 1: Landing on National AQI Overview (Duration: 1.5 Minutes)
1.  **Action**: Open the dashboard view. Ensure the page displays "National AQI Overview". Set the date to a high-pollution month (e.g., November) and select the pollutant as "NO2" or "HCHO" to reveal high-contrast colors over Northern India (Gangetic Belt).
2.  **Voice Track**: 
    > "Welcome judges. We are looking at our National AQI Overview, powered by Google Earth Engine and Sentinel-5P TROPOMI streams. Traditional portals show blank spots over rural zones. But here, we have a continuous, interpolated grid spanning the whole nation. 
    > If we slide our date selector into the winter months, we see immediate yellow, orange, and red layers blooming over the Indo-Gangetic Plains. Hover over any state, like Haryana or Punjab to see calculated station base AQIs, active fire counts, and mean column densities."
3.  **Action**: Hover over different regions on the map. Click on Punjab on the map, showcasing how the sidebar / info-grid dynamically changes.

---

## Part 2: Highlighting chemical HCHO Hotspot Detection (Duration: 2 Minutes)
1.  **Action**: Click on the second tab: "HCHO Hotspot Analysis". 
2.  **Voice Track**: 
    > "Let us dive into the scientific core: Formaldehyde (HCHO) hotspots. HCHO acts as a structural organic diagnostic tracer. 
    > When we load this page, our Python backend runs DBSCAN spatial clustering over active column pixels. Notice the clustered zones highlighted. Rather than just raw grid points, the AI identifies contiguous plumes.
    > In May and June, we see significant clusters starting around major industrial chemical corridors. In November, clusters move into agricultural hubs."
3.  **Action**: Slide the DBSCAN Epsilon parameter from `2.0` down to `1.2`. Show how the number of clusters changes in real time.
4.  **Voice Track**: 
    > "Our dashboard lets administrators configure DBSCAN parameters. Lowering the epsilon radius from 2.0 to 1.2 isolates dense core plumes, telling environmental scientists exactly where the localized source coordinates of emission are, without being distracted by ambient wind dispersion."

---

## Part 3: Correlating Biomass Burning & Fire Counts (Duration: 1.5 Minutes)
1.  **Action**: Open the third tab: "Biomass Burning Analysis". 
2.  **Voice Track**: 
    > "A critical feature of our project is proving the direct causation link between crop-residue fires and respiratory load. We ingest MODIS and VIIRS thermal anomaly indices.
    > Look at this scatter diagram: our coordinates link daily fire counts directly to HCHO densities.
    > The correlation coefficient is high ($R = 0.81$ average). This proves that formaldehyde spikes in agricultural regions are directly driven by burning rather than normal urban traffic. It confirms that satellite-derived columns alone can identify burning zones before smoke drifts to Delhi."
3.  **Action**: Toggle the line of best fit indicator or adjust the regression model to show the dynamic formulas.

---

## Part 4: Interactive AI Prediction Center & Forecast Alerts (Duration: 2 Minutes)
1.  **Action**: Click on the fourth tab: "AI Prediction Center".
2.  **Voice Track**: 
    > "Now, how do we predict and mitigate this? Let's navigate to our AI Prediction Center. Here, we run Scikit-Learn Random Forest and XGBoost in parallel to compare accuracy.
    > As a demonstration, let us adjust the sliders. Let's assume we are in Punjab in November. We drag the Fire Count slider up to 120 and set the satellite HCHO column to 0.00035 mol/m²."
3.  **Action**: Drag the Fire Count slider to `120`, HCHO to `0.00035`, and click the "Generate Hotspot Analysis Report" button.
4.  **Voice Track**: 
    > "When we call our prediction model, our backend runs XGBoost—which predicts an AQI of 381, categorizing it as Severe.
    > Simultaneously, the Future Risk algorithm flags this district as a High Hazard warning. And look at our integrated Geospatial Assistant—powered by Gemini on Google Cloud. It reads our parameters and immediately writes a custom diagnostic briefing. It explains the chemical oxidation rate under active burning, warns about secondary ozone, and recommends immediate stubble mitigation tasks.
    > This transforms complex spectral bands into automated actions."

---

## Part 5: Generating Reports & Closing (Duration: 0.5 Minutes)
1.  **Action**: Open the final tab: "Analytics & Reports" or the "Code Deliverables" hub to show the judges the downloadable code, PDF formats, and full deployment guide.
2.  **Voice Track**: 
    > "Everything you've seen is built entirely on open, free layers. On our hub, judges can download the GEE harvesters, the full ML training pipeline, the deployment guides, and structured reports.
    > Thank you judges. With Sentinel-AQI, we have built a low-cost, scalable, planetary-monitoring instrument that equips India's cities and villages to predict pollution and act before they breathe it."
