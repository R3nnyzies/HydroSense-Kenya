import pytest
import numpy as np
from src.simulation import calculate_et_vectorized, euler_step, rk4_step, monte_carlo_rainfall

def test_calculate_et_vectorized():
    """Test Evapotranspiration formula using array inputs and negative clamping (max 0)."""
    T = np.array([25, 30])
    W = np.array([2.0, 3.0])
    Solar = np.array([0.7, 0.8])
    H = np.array([60, 90]) # High humidity might push ET negative if solar/temp are low
    
    et = calculate_et_vectorized(T, W, Solar, H)
    
    assert len(et) == 2
    assert (et >= 0).all() # ET should never be negative due to np.maximum(0, et)
    
def test_euler_step():
    """Test single step of Euler method for soil water balance."""
    S_t = 30.0
    dt = 1.0
    R = 10.0   # 10mm rain
    I = 5.0    # 5mm irrigation
    ET = 3.0   # 3mm evapotranspiration
    field_cap = 40.0
    drain_coeff = 0.2
    
    # Since S_t < field_cap, drainage D = 0. 
    # dS/dt = R + I - ET - D = 10 + 5 - 3 - 0 = 12
    # S_next = 30 + 12(1) = 42
    S_next = euler_step(S_t, dt, R, I, ET, field_cap, drain_coeff)
    
    assert S_next == pytest.approx(42.0)

def test_rk4_step_consistency():
    """
    Test that RK4 and Euler give identical results for completely linear/constant rates.
    If the rates of change don't depend on S (no drainage triggered), RK4 and Euler are identical.
    """
    S_t = 20.0
    dt = 1.0
    R, I, ET = 5.0, 2.0, 4.0
    field_cap = 50.0 # High enough to prevent drainage
    drain_coeff = 0.1
    
    s_euler = euler_step(S_t, dt, R, I, ET, field_cap, drain_coeff)
    s_rk4 = rk4_step(S_t, dt, R, I, ET, field_cap, drain_coeff)
    
    assert s_euler == pytest.approx(s_rk4)

def test_monte_carlo_rainfall():
    """Test Monte Carlo generator for correct shape and no negative rainfall logic."""
    base_rainfall = np.array([0.0, 5.0, 10.0, 0.0, 2.0])
    num_scenarios = 100
    
    scenarios = monte_carlo_rainfall(base_rainfall, num_scenarios=num_scenarios, std_dev=0.2)
    
    # Check shape
    assert scenarios.shape == (num_scenarios, len(base_rainfall))
    
    # Ensure no negative rainfall
    assert np.min(scenarios) >= 0.0
    
    # Zeros in base rainfall should remain zeros (0 * noise = 0)
    assert np.all(scenarios[:, 0] == 0.0)