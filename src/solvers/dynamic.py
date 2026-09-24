# src/solvers/dynamic.py
import numpy as np
from src.models.tire import compute_tire_forces
from src.config import TireConfig

def run_dynamic_simulation(duration: float, dt: float, config: TireConfig):
    """
    Simulates a single tire over time under a changing input, 
    updating velocity and acceleration via F = ma.
    """
    time_steps = np.arange(0, duration, dt)
    
    # Simple state variables for a single mass/tire system
    mass = 50.0            # kg (approx. quarter-kart mass)
    velocity_x = 10.0      # initial forward velocity (m/s)
    velocity_y = 0.0       # lateral velocity (m/s)
    
    # Storage for logging results
    history = {'time': [], 'vx': [], 'vy': [], 'fx': [], 'fy': [], 'accel_x': [], 'accel_y': []}
    
    for t in time_steps:
        # Example scenario: Introduce a sudden steering/slip angle at t = 1.0 second
        steering_angle = np.radians(5.0) if t >= 1.0 else 0.0
        slip_ratio = 0.0
        
        # Calculate slip angle dynamically from velocity vectors
        # (alpha = atan(vy / vx) - delta)
        vx_safe = max(velocity_x, 0.1) # Prevent division by zero
        slip_angle = np.arctan2(velocity_y, vx_safe) - steering_angle
        
        # Standard normal load for this quarter-mass (Newtons)
        fz = mass * 9.81 
        
        # 1. Get forces from the tire model
        fx, fy = compute_tire_forces(fz, slip_angle, slip_ratio, config)
        
        # 2. Apply Newton's Second Law (F = ma -> a = F / m)
        accel_x = fx / mass
        accel_y = fy / mass
        
        # 3. Integrate acceleration to update velocity (Euler integration)
        velocity_x += accel_x * dt
        velocity_y += accel_y * dt
        
        # Log history
        history['time'].append(t)
        history['vx'].append(velocity_x)
        history['vy'].append(velocity_y)
        history['fx'].append(fx)
        history['fy'].append(fy)
        history['accel_x'].append(accel_x)
        history['accel_y'].append(accel_y)
        
    return history