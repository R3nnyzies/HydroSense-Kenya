import pandas as pd
import numpy as np

def load_and_clean_weather(filepath: str) -> pd.DataFrame:
    """
    Loads and cleans daily weather data.
    Addresses missing values and realistic outlier constraints.
    """
    # Load data treating 'NA' and empty strings as NaN
    df = pd.read_csv(filepath, na_values=["NA", ""])
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Handle missing values via linear interpolation (e.g., row 2026-03-08 rainfall, 03-21 humidity)
    df.set_index('date', inplace=True)
    df.interpolate(method='time', inplace=True)
    df.reset_index(inplace=True)
    
    # 2. Outlier treatment: 85.00mm rainfall on 03-26 is high but physically possible. 
    # However, if we assume an anomalous spike, we can cap it at 99th percentile or a fixed threshold.
    # For demonstration, we'll cap extreme rainfall > 50mm to 50mm to prevent skewed scale.
    df['rainfall_mm'] = np.where(df['rainfall_mm'] > 50.0, 50.0, df['rainfall_mm'])
    
    return df

def load_and_clean_soil(filepath: str) -> pd.DataFrame:
    """
    Loads and cleans soil sensor data, specifically treating sensor faults
    and blatant anomalies in tank levels.
    """
    df = pd.read_csv(filepath, na_values=["NA", ""])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 1. Handle sensor faults (e.g., 'CHECK' status)
    # Replace readings where sensor_status != 'OK' with NaN, then interpolate
    fault_mask = df['sensor_status'] != 'OK'
    cols_to_null = ['soil_moisture_pct', 'tank_level_liters', 'pump_flow_lpm', 'pump_power_watts']
    df.loc[fault_mask, cols_to_null] = np.nan
    
    # 2. Handle specific outliers (e.g., Zone_C 9900 tank level on 2026-03-14)
    # Tank level normally hovers around 3000-5000. 9900 is an anomaly.
    df['tank_level_liters'] = np.where(df['tank_level_liters'] > 6000, np.nan, df['tank_level_liters'])
    
    # Sort by zone and time to properly interpolate missing/NaNed values
    df.sort_values(by=['zone_id', 'timestamp'], inplace=True)
    df[cols_to_null] = df.groupby('zone_id')[cols_to_null].transform(lambda x: x.interpolate(method='linear'))
    
    # Fill any remaining NaNs (if at the start/end of a group) with forward/backward fill
    df[cols_to_null] = df.groupby('zone_id')[cols_to_null].transform(lambda x: x.bfill().ffill())
    
    return df

def load_parameters(filepath: str) -> pd.DataFrame:
    """
    Loads crop zone parameters.
    """
    df = pd.read_csv(filepath, na_values=["NA", ""])
    return df