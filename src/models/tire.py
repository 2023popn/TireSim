# src/models/tire.py
import numpy as np
from src.config import TireConfig
from src.models.thermal import calculate_temperature_factor

def compute_tire_forces(fz: float, slip_angle: float, slip_ratio: float, config: TireConfig, tire_temp: float) -> tuple[float, float]:
    """
    Computes longitudinal (Fx) and lateral (Fy) forces for a given normal load,
    slip angle (rad), and slip ratio.
    """
    # 1. Get thermal multiplier using the model specified in config
    temp_factor = calculate_temperature_factor(
        temp=tire_temp, 
        model_type=config.thermal_model_type, 
        opt_temp=config.opt_temp
    )
    
    # 2. Adjust peak friction combining load sensitivity and temperature factor
    mu = config.mu_peak * (1.0 - config.load_sensitivity * (fz / 1000.0)) * temp_factor
    max_force = mu * fz

    # Simple linear brush-style or combined slip approximation for testing
    # (Replace or expand this with your full physics equations later)
    
    # Effective friction adjusted for load sensitivity
    mu = config.mu_peak * (1.0 - config.load_sensitivity * (fz / 1000.0))
    max_force = mu * fz
    
    # Lateral force calculation (simplified linear region + saturation)
    fy = -config.cornering_stiffness * slip_angle
    fy = np.clip(fy, -max_force, max_force) # Cap at friction limit
    
    # Longitudinal force calculation (simplified)
    fx = config.cornering_stiffness * slip_ratio
    fx = np.clip(fx, -max_force, max_force)
    
    # Enforce friction circle constraint (combined slip limit)
    total_force = np.sqrt(fx**2 + fy**2)
    if total_force > max_force:
        scale = max_force / total_force
        fx *= scale
        fy *= scale
        
    return fx, fy