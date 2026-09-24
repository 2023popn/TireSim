# src/solvers/sweps.py
import numpy as np
from src.models.tire import compute_tire_forces
from src.config import TireConfig

def run_slip_angle_sweep(fz_values: list[float], config: TireConfig):
    """Runs a sweep of slip angles across multiple normal loads."""
    slip_angles = np.radians(np.linspace(-15, 15, 100))
    results = {}
    
    for fz in fz_values:
        fy_list = []
        fx_list = []
        for alpha in slip_angles:
            fx, fy = compute_tire_forces(fz, alpha, slip_ratio=0.0, config=config)
            fx_list.append(fx)
            fy_list.append(fy)
        results[fz] = {
            'slip_angles_deg': np.degrees(slip_angles),
            'fx': np.array(fx_list),
            'fy': np.array(fy_list)
        }
        
    return results