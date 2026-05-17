import numpy as np

def calculate_et_vectorized(T, W, Solar, H):
    """
    Computes Evapotranspiration using NumPy vectorization.
    ET = max(0, 0.12*T + 0.35*W + 2.4*Solar - 0.025*H)
    """
    et = 0.12 * T + 0.35 * W + 2.4 * Solar - 0.025 * H
    return np.maximum(0, et)

def soil_water_derivative(S, R, I, ET, field_capacity, drainage_coeff):
    """
    Returns dS/dt for the continuous soil-water model.
    D_t is modeled as a factor of moisture exceeding field capacity.
    """
    D = drainage_coeff * max(0, S - field_capacity)
    return R + I - ET - D

def euler_step(S_t, dt, R, I, ET, field_capacity, drainage_coeff):
    """Performs one step of the Euler method."""
    dS_dt = soil_water_derivative(S_t, R, I, ET, field_capacity, drainage_coeff)
    return S_t + dS_dt * dt

def rk4_step(S_t, dt, R, I, ET, field_capacity, drainage_coeff):
    """Performs one step of the Runge-Kutta 4 (RK4) method."""
    # Assuming R, I, ET are constant over the dt interval for simplicity
    k1 = soil_water_derivative(S_t, R, I, ET, field_capacity, drainage_coeff)
    k2 = soil_water_derivative(S_t + 0.5*dt*k1, R, I, ET, field_capacity, drainage_coeff)
    k3 = soil_water_derivative(S_t + 0.5*dt*k2, R, I, ET, field_capacity, drainage_coeff)
    k4 = soil_water_derivative(S_t + dt*k3, R, I, ET, field_capacity, drainage_coeff)
    
    return S_t + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def monte_carlo_rainfall(base_rainfall, num_scenarios=1000, std_dev=0.3):
    """
    Generates 1,000 rainfall scenarios using a normal distribution multiplier 
    to simulate weather uncertainty.
    """
    scenarios = np.zeros((num_scenarios, len(base_rainfall)))
    for i in range(num_scenarios):
        # Generate random noise (e.g., +/- 30% variation)
        noise = np.random.normal(loc=1.0, scale=std_dev, size=len(base_rainfall))
        scenario_rain = base_rainfall * noise
        # Ensure no negative rainfall
        scenarios[i] = np.maximum(0, scenario_rain)
    return scenarios