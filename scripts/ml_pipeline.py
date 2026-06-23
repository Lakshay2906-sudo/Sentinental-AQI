#!/usr/bin/env python
"""
=============================================================================
Machine Learning Predictive Pipeline: Satellite AQI & Hotspot Forecasting
=============================================================================
Author: Senior Geospatial AI Engineer
Models Implemented:
1. Regressors (Random Forest & XGBoost) matching TROPOMI arrays to Ground Stations.
2. DBSCAN Spatial Clusterers targeting volatile Formaldehyde (HCHO) plume clusters.
3. Alert Classifier (Risk Score modeling: High, Medium, Low for upcoming days).
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.cluster import DBSCAN

# Attempt importing XGBoost gracefully (fallback to GradientBoosting if not setup)
try:
    import xgboost as xgb
    USE_XGB = True
except ImportError:
    from sklearn.ensemble import GradientBoostingRegressor
    USE_XGB = False

# 1. CORE DATASET SIMULATOR FOR INDIA STATES
# This creates representative hackathon spatial indicators matching TROPOMI & FIRMS telemetry
def generate_geospatial_dataframe(samples=1000):
    np.random.seed(42)
    regions = ['Indo-Gangetic Plain', 'Western India', 'Southern Peninsula', 'Eastern India', 'Central Deccan']
    
    # Coordinates approximating locations in India
    lat_center = np.random.uniform(8.0, 35.0, samples)
    lon_center = np.random.uniform(68.0, 97.0, samples)
    
    # Satellite columns (TROPOMI densities)
    no2 = np.random.uniform(5.0, 150.0, samples)  # ug/m3 equivalent
    so2 = np.random.uniform(2.0, 60.0, samples)   # ug/m3 equivalent
    co = np.random.uniform(0.1, 4.0, samples)     # mg/m3 equivalent
    o3 = np.random.uniform(15.0, 180.0, samples)  # ug/m3 equivalent
    hcho = np.random.uniform(0.00005, 0.00045, samples) # mol/m2 column
    
    # Fire counts from MODIS
    fire_count = np.random.poisson(lam=12, size=samples)
    
    # Seasonality
    month = np.random.randint(1, 13, samples)
    
    # Introduce real physical correlation (e.g. fire count increases HCHO & CO)
    co = co + (fire_count * 0.05) + (no2 * 0.01)
    hcho = hcho + (fire_count * 0.00001)
    
    # Calculate target (Actual Ground Truth Station AQI)
    # Ground truth stations are highly correlated with primary pollutants
    indices = np.stack([
        50 + (no2 * 1.1),
        30 + (so2 * 1.5),
        20 + (co * 30),
        10 + (o3 * 1.2)
    ], axis=1)
    ground_truth_aqi = np.max(indices, axis=1) + np.random.normal(0, 8, samples)
    ground_truth_aqi = np.clip(ground_truth_aqi, 20, 500)

    df = pd.DataFrame({
        'Latitude': lat_center,
        'Longitude': lon_center,
        'Region': np.random.choice(regions, samples),
        'NO2': no2,
        'SO2': so2,
        'CO': co,
        'O3': o3,
        'HCHO': hcho,
        'FireCount': fire_count,
        'Month': month,
        'ActualAQI': ground_truth_aqi
    })
    return df

# 2. MODEL 1: COMPARATIVE REGRESSION PIPELINE (RF VS XGB)
def train_aqi_regressors(df):
    print("--- Training Machine Learning Regressors for AQI Target ---")
    
    # Feature columns
    X = df[['NO2', 'SO2', 'CO', 'O3', 'HCHO', 'FireCount', 'Month']]
    y = df['ActualAQI']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # A. RANDOM FOREST PIPELINE
    rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    
    rf_metrics = {
        'MAE': mean_absolute_error(y_test, rf_preds),
        'RMSE': np.sqrt(mean_squared_error(y_test, rf_preds)),
        'R2': r2_score(y_test, rf_preds)
    }
    
    # B. XGBOOST PIPELINE (or fallback to Scikit-Learn GradientBoost)
    if USE_XGB:
        reg = xgb.XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
        model_name = "XGBoost"
    else:
        reg = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
        model_name = "GradientBoosting (Scikit-Learn fallback)"
        
    reg.fit(X_train, y_train)
    reg_preds = reg.predict(X_test)
    
    reg_metrics = {
        'MAE': mean_absolute_error(y_test, reg_preds),
        'RMSE': np.sqrt(mean_squared_error(y_test, reg_preds)),
        'R2': r2_score(y_test, reg_preds)
    }
    
    print(f"Random Forest Metrics: MAE={rf_metrics['MAE']:.3f}, RMSE={rf_metrics['RMSE']:.3f}, R2={rf_metrics['R2']:.3f}")
    print(f"{model_name} Metrics: MAE={reg_metrics['MAE']:.3f}, RMSE={reg_metrics['RMSE']:.3f}, R2={reg_metrics['R2']:.3f}")
    
    return rf, reg, rf_metrics, reg_metrics

# 3. MODEL 2: DBSCAN SPATIAL CLUSTERING FOR HCHO HOTSPOTS
def detect_hcho_hotspots(df, eps_km=2.5, min_samples=4):
    """
    Groups dense grids of coordinates where HCHO column concentration
    exceeds critical thresholds into actionable DBSCAN clusters.
    """
    print("--- Running DBSCAN Clustering for Volatile Plumes ---")
    
    # Filter where formaldehyde columns are elevated (hotspot precursor density rule)
    threshold = 0.00028 # mol/m2
    elevated_df = df[df['HCHO'] >= threshold].copy()
    
    if len(elevated_df) < 5:
        print("Insufficient elevated columns discovered in this slice for spatial clustering.")
        return df, []
        
    # Scale latitude/longitude representing distance (approx 1 degree lat = 111km)
    coords = elevated_df[['Longitude', 'Latitude']].values
    
    # EPS is defined roughly (e.g. 1 deg = 111km. Thus 100km ~ 0.9 deg rad)
    db = DBSCAN(eps=eps_km, min_samples=min_samples)
    labels = db.fit_predict(coords)
    
    elevated_df['ClusterID'] = labels
    
    # Group and locate clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"DBSCAN detected {n_clusters} persistent/seasonal pollution hotspots in spatial mesh.")
    
    return elevated_df, n_clusters

# 4. MODEL 3: FUTURE HOTSPOT RISK ALERT
def calculate_future_risk_scores(df):
    """
    Predicts a prospective Risk Level (Low/Medium/High) indicating
    district-level hotspots using moving thresholds of fire activities.
    """
    risk_ratings = []
    risk_scores = []
    
    for idx, row in df.iterrows():
        # Score calculation formula matching geographic boundary vulnerability
        score = (row['FireCount'] * 4.5) + (row['HCHO'] * 12000) + (row['O3'] * 0.3) + (row['NO2'] * 0.2)
        score = min(100, max(0, score)) # bound between 0-100
        
        if score >= 65:
            rating = "High"
        elif score >= 35:
            rating = "Medium"
        else:
            rating = "Low"
            
        risk_scores.append(round(score, 1))
        risk_ratings.append(rating)
        
    df['RiskScore'] = risk_scores
    df['FutureRiskRating'] = risk_ratings
    return df


if __name__ == "__main__":
    df = generate_geospatial_dataframe(600)
    rf_m, xgb_m, rf_scores, xgb_scores = train_aqi_regressors(df)
    
    clust_df, cl_count = detect_hcho_hotspots(df, eps_km=1.8, min_samples=3)
    
    df_with_risk = calculate_future_risk_scores(df)
    print(f"Risk rating summary counts:\n{df_with_risk['FutureRiskRating'].value_counts()}")
