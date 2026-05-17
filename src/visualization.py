import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_soil_moisture_trends(df_soil):
    """Plots clean soil moisture data across all three zones."""
    plt.figure(figsize=(10, 5))
    for zone in df_soil['zone_id'].unique():
        subset = df_soil[df_soil['zone_id'] == zone]
        plt.plot(subset['timestamp'], subset['soil_moisture_pct'], marker='o', label=f'{zone}')
    
    plt.title('Daily Soil Moisture by Zone')
    plt.xlabel('Date')
    plt.ylabel('Soil Moisture (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_weather_balance(dates, rainfall, et):
    """Visualizes Rainfall vs. Evapotranspiration."""
    plt.figure(figsize=(10, 5))
    plt.bar(dates, rainfall, alpha=0.6, color='blue', label='Rainfall (mm)')
    plt.plot(dates, et, color='red', marker='x', label='ET (mm/day)')
    plt.title('Rainfall vs. Estimated Evapotranspiration')
    plt.xlabel('Date')
    plt.ylabel('Water Level (mm)')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_monte_carlo_envelope(dates, mc_scenarios, baseline_rain):
    """Plots uncertainty envelope for 1000 Monte Carlo rainfall scenarios."""
    plt.figure(figsize=(10, 5))
    
    # Calculate percentiles
    p5 = np.percentile(mc_scenarios, 5, axis=0)
    p95 = np.percentile(mc_scenarios, 95, axis=0)
    mean_scenario = np.mean(mc_scenarios, axis=0)
    
    plt.fill_between(dates, p5, p95, color='gray', alpha=0.3, label='90% Confidence Interval')
    plt.plot(dates, mean_scenario, 'k--', label='Mean Simulated Rainfall')
    plt.plot(dates, baseline_rain, 'b-', label='Baseline Recorded Rainfall')
    
    plt.title('Monte Carlo Rainfall Simulation (1,000 Scenarios)')
    plt.xlabel('Date')
    plt.ylabel('Rainfall (mm)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_optimized_schedule(dates, moisture, irrigation, min_threshold, target):
    """Plots the moisture curve alongside the recommended irrigation interventions."""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Soil Moisture (%)', color=color)
    # Note: moisture array is n+1, so we plot moisture[:-1] against dates
    ax1.plot(dates, moisture[:-1], color=color, label='Simulated Moisture')
    ax1.axhline(y=min_threshold, color='red', linestyle=':', label='Min Stress Threshold')
    ax1.axhline(y=target, color='green', linestyle='--', label='Target Moisture')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()  
    color = 'tab:cyan'
    ax2.set_ylabel('Irrigation Applied (mm/L)', color=color)
    ax2.bar(dates, irrigation, color=color, alpha=0.5, label='Irrigation Volume')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    plt.title('Optimized Irrigation Schedule & Moisture Tracking')
    fig.tight_layout() 
    plt.xticks(rotation=45)
    plt.show()
    
def plot_numerical_derivatives(dates, S_values, dS_dt):
    """Plots the soil moisture and its estimated rate of change (derivative)."""
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    ax1.plot(dates, S_values, 'b-', marker='o', label='Soil Moisture (%)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Moisture (%)', color='b')
    
    ax2 = ax1.twinx()
    ax2.plot(dates, dS_dt, 'r--', label='Rate of Change (Central Diff)')
    ax2.set_ylabel('dS/dt', color='r')
    
    plt.title('Soil Moisture Dynamics and Derivative')
    fig.tight_layout()
    plt.show()


def plot_climate_drivers(weather_clean):
    """Plot 1: Climatic Drivers (Rainfall & Solar Intensity)"""
    fig, ax1 = plt.subplots(figsize=(12, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Rainfall (mm)', color=color)
    ax1.bar(weather_clean['date'], weather_clean['rainfall_mm'], color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Solar Index', color=color)
    ax2.plot(weather_clean['date'], weather_clean['solar_index'], color=color, marker='o', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Daily Rainfall vs. Solar Intensity')
    plt.tight_layout()
    plt.show()

def plot_soil_moisture_trends_with_threshold(df_soil):
    """Plot 2: Soil Moisture Depletion Across Zones with threshold line"""
    plt.figure(figsize=(12, 6))
    for zone in df_soil['zone_id'].unique():
        zone_data = df_soil[df_soil['zone_id'] == zone]
        plt.plot(zone_data['timestamp'], zone_data['soil_moisture_pct'], label=zone, linewidth=2)

    plt.axhline(y=20, color='r', linestyle='--', label='Critical Wilting Point (Maize)')
    plt.title('Soil Moisture Dynamics by Crop Zone')
    plt.xlabel('Date')
    plt.ylabel('Soil Moisture (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_pump_efficiency(df_soil):
    """Plot 3: Pump Power vs Flow Rate"""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_soil, x='pump_flow_lpm', y='pump_power_watts', hue='zone_id', s=100)
    plt.title('Pump Efficiency: Flow Rate vs Power Draw')
    plt.xlabel('Pump Flow (Liters per Minute)')
    plt.ylabel('Power Draw (Watts)')
    plt.grid(True)
    plt.show()

def plot_dashboard(weather_clean, df_soil):
    """Plot 4 & 5: Tank Drawdown and System Heatmap side-by-side"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 4: Tank Level
    zone_a_data = df_soil[df_soil['zone_id'] == 'Zone_A']
    axes[0].plot(zone_a_data['timestamp'], zone_a_data['tank_level_liters'], color='teal', linewidth=2)
    axes[0].set_title('Main Storage Tank Level Drawdown')
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Volume (Liters)')
    axes[0].grid(True)

    # Plot 5: Weather Correlation Heatmap
    corr_cols = ['temperature_c', 'humidity_pct', 'wind_speed_mps', 'solar_index', 'rainfall_mm']
    sns.heatmap(weather_clean[corr_cols].corr(), annot=True, cmap='coolwarm', center=0, ax=axes[1])
    axes[1].set_title('Weather Variable Correlation Matrix')

    plt.tight_layout()
    plt.show()