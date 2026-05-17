import matplotlib.pyplot as plt
import numpy as np

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