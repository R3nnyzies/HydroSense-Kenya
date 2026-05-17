import numpy as np
from src.numerical_methods import secant
from src.simulation import rk4_step

def optimize_irrigation_schedule(initial_moisture, rainfall, et, min_moisture, target_moisture, field_capacity, drainage_coeff):
    """
    Minimizes water use while ensuring soil moisture > min_moisture.
    Uses secant root-finding to calculate the exact irrigation amount I_t needed 
    to hit the target_moisture if it drops below min_moisture.
    """
    n_days = len(rainfall)
    moisture_record = np.zeros(n_days + 1)
    irrigation_record = np.zeros(n_days)
    
    moisture_record[0] = initial_moisture
    dt = 1.0 # 1 day step
    
    for t in range(n_days):
        # Predict next day's moisture without irrigation
        S_next_pred = rk4_step(moisture_record[t], dt, rainfall[t], 0, et[t], field_capacity, drainage_coeff)
        
        if S_next_pred < min_moisture:
            # We need to find I_t such that S_{t+1}(I_t) - target_moisture = 0
            # Define the objective function for root finding
            def moisture_deficit(I):
                S_next = rk4_step(moisture_record[t], dt, rainfall[t], I, et[t], field_capacity, drainage_coeff)
                return S_next - target_moisture
            
            # Use Secant method to find required irrigation
            # Guesses: 0 and an arbitrary initial guess (e.g., target - predicted)
            guess1 = 0.0
            guess2 = target_moisture - S_next_pred
            
            try:
                opt_I, _ = secant(moisture_deficit, guess1, guess2)
                irrigation_record[t] = max(0, opt_I) # Cannot remove water
            except ZeroDivisionError:
                irrigation_record[t] = guess2 # fallback
        else:
            irrigation_record[t] = 0.0
            
        # Update actual moisture with computed irrigation
        moisture_record[t+1] = rk4_step(moisture_record[t], dt, rainfall[t], irrigation_record[t], et[t], field_capacity, drainage_coeff)
        
    return moisture_record, irrigation_record