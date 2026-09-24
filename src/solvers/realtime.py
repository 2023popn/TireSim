# src/solvers/realtime.py
import time
import numpy as np
import matplotlib.pyplot as plt
from src.models.tire import compute_tire_forces
from src.config import TireConfig

def run_live_simulation(config: TireConfig):
    """
    Runs a continuously updating live simulation loop using interactive Matplotlib mode.
    Steps through physics calculations and updates the display without storing history.
    """
    # Turn on Matplotlib interactive mode
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Setup a live Friction Circle plot as a visualizer
    ax.set_xlim(-1500, 1500)
    ax.set_ylim(-1500, 1500)
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_title("Live Tire Force Vector (F_x vs F_y)")
    ax.set_xlabel("Longitudinal Force Fx (N)")
    ax.set_ylabel("Lateral Force Fy (N)")
    
    # Initialize a scatter point for the live force vector
    point, = ax.plot([], [], 'ro', markersize=10, label="Current Force State")
    ax.legend(loc='upper right')
    
    # Simulation state variables
    mass = 50.0
    vx = 10.0
    vy = 0.0
    dt = 0.05  # Time step size
    
    print("Starting live simulation... Close the window to exit.")
    
    try:
        step = 0
        while plt.fignum_exists(fig.number): # Runs until user closes the window
            # Create a changing steering input over time (e.g., sinusoidal wave)
            steering_angle = np.radians(10.0 * np.sin(step * 0.1))
            slip_ratio = 0.05 * np.cos(step * 0.05) # fluctuating acceleration/braking
            
            # Physics calculations for this single step
            vx_safe = max(vx, 0.1)
            slip_angle = np.arctan2(vy, vx_safe) - steering_angle
            fz = mass * 9.81
            
            # Get forces from your modular tire model
            fx, fy = compute_tire_forces(fz, slip_angle, slip_ratio, config)
            
            # Step physics forward (Euler integration)
            accel_x = fx / mass
            accel_y = fy / mass
            vx += accel_x * dt
            vy += accel_y * dt
            
            # Update the plot graphic directly (no history storage required)
            point.set_data([fx], [fy])
            
            # Refresh the canvas
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            # Control frame rate
            time.sleep(dt)
            step += 1
            
    except KeyboardInterrupt:
        print("\nLive simulation stopped by user.")
    finally:
        plt.ioff()
        plt.close()