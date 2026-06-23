/**
 * @title Sentinel-5P & MODIS Active Fire Data Extractor for India Surface AQI
 * @author Senior Geospatial AI Engineer
 * @description Google Earth Engine (GEE) script to filter, reduce, and export 
 *              multispectral pollution columns and burning counts over India boundaries.
 * @platform Google Earth Engine Code Editor (JavaScript)
 */

// 1. DEFINE AREA OF INTEREST (India Administrative Boundary)
var countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');
var india = countries.filter(ee.Filter.eq('country_na', 'India'));
Map.centerObject(india, 5);
Map.addLayer(india, {color: 'grey'}, 'India Boundary', false);

// 2. DEFINE TEMPORAL WINDOWS
var startDate = '2025-01-01';
var endDate = '2025-12-31';

// 3. RETRIEVE SENTINEL-5P (TROPOMI) SATELLITE MEASUREMENTS
// A. Formaldehyde (HCHO)
var hchoCol = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_HCHO')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('tropospheric_HCHO_column_number_density');

// B. Nitrogen Dioxide (NO2)
var no2Col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('NO2_column_number_density');

// C. Sulfur Dioxide (SO2)
var so2Col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_SO2')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('SO2_column_number_density');

// D. Carbon Monoxide (CO)
var coCol = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CO')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('CO_column_number_density');

// E. Ozone (O3)
var o3Col = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_O3')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('O3_column_number_density');

// 4. RETRIEVE MODIS ACTIVE FIRE & THERMAL ANOMALIES (FIRMS)
var fireCol = ee.ImageCollection('FIRMS')
  .filterBounds(india)
  .filterDate(startDate, endDate)
  .select('T21'); // Brightness temperature band representing active thermal anomaly

// 5. CALCULATE MONTHLY CLIMATOLOGY (COMPOSITES)
var months = ee.List.sequence(1, 12);
var monthlyComposites = months.map(function(m) {
  var startStr = ee.String('2025-').cat(ee.Number(m).format('%02d')).cat('-01');
  var endStr = ee.Date(startStr).advance(1, 'month').format('YYYY-MM-dd');
  
  // Create temporal filter
  var hchoMean = hchoCol.filterDate(startStr, endStr).mean().clip(india);
  var no2Mean = no2Col.filterDate(startStr, endStr).mean().clip(india);
  var so2Mean = so2Col.filterDate(startStr, endStr).mean().clip(india);
  var coMean = coCol.filterDate(startStr, endStr).mean().clip(india);
  var o3Mean = o3Col.filterDate(startStr, endStr).mean().clip(india);
  
  // Count active fires in the region in this month
  var localFires = fireCol.filterDate(startStr, endStr).count().clip(india);

  // Combine into single composite image with renamed bands
  return hchoMean.rename('HCHO')
    .addBands(no2Mean.rename('NO2'))
    .addBands(so2Mean.rename('SO2'))
    .addBands(coMean.rename('CO'))
    .addBands(o3Mean.rename('O3'))
    .addBands(localFires.rename('FIRE_COUNTS'))
    .set('month', m)
    .set('year', 2025);
});

// Convert list of composite images back to an ImageCollection
var compositeColection = ee.ImageCollection.fromImages(monthlyComposites);

// 6. VISUALIZE SATELLITE LAYERS FOR INSPECTION OR HACKATHON DEMO
var hchoPalette = ['blue', 'teal', 'green', 'yellow', 'orange', 'red', 'darkred'];
var hchoVis = {
  min: 0.0,
  max: 0.0003,
  palette: hchoPalette
};
var selectedComposite = ee.Image(compositeColection.filter(ee.Filter.eq('month', 5)).first()); // May composite
Map.addLayer(selectedComposite.select('HCHO'), hchoVis, 'HCHO Tropospheric density (May 2025)');

// 7. EXPORT COMPILED MULTIBAND METRICS TO GOOGLE DRIVE
// This enables offline downloading and consumption by SQLite/PostgreSQL databases 
// or Python machine learning modules.
months.evaluate(function(monthList) {
  monthList.forEach(function(m) {
    var monthlyComp = ee.Image(compositeColection.filter(ee.Filter.eq('month', m)).first());
    
    Export.image.toDrive({
      image: monthlyComp,
      description: 'India_Pollution_Composite_2025_Month_' + m,
      scale: 10000, // 10km grid representing excellent resolution balance
      region: india.geometry().bounds(),
      maxPixels: 1e9,
      crs: 'EPSGS:4326', // Standard WGS 84 coordinate system
      fileFormat: 'GeoTIFF'
    });
  });
  print("Scheduled GEE Monthly Raster Exports. Click 'Run' in Task Panel to execute exports to Drive!");
});
