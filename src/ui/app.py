import sys
import os

# Dynamically add the project root directory (TireSim/) to Python's path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# src/ui/app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Import your modular backend engines
from src.config import TireConfig
from src.solvers.sweeps import run_slip_angle_sweep
from src.solvers.dynamic import run_dynamic_simulation

# Page configuration
st.set_page_config(page_title="TireSim Dashboard", layout="wide")
st.title("Go-Kart Tire Simulation Dashboard")

# Initialize global configuration
config = TireConfig()

# Create the top-level tabs requested
tab_live, tab_dynamic, tab_sweep = st.tabs([
    "Live Simulator", 
    "Dynamic Test (Batch)", 
    "Parameter Sweeps"
])

with tab_live:
    st.header("Real-Time Single-Tire Physics")
    st.write("Stream updates step-by-step through the tire model.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Controls")
        steering_input = st.slider("Steering Angle (deg)", -15.0, 15.0, 5.0)
        load_input = st.slider("Normal Load Fz (N)", 200.0, 2000.0, 1000.0)
        run_live = st.button("Run Live Step / Loop")
        
    with col2:
        st.subheader("Live Force Output")
        # Placeholder for live plotting in Streamlit
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlim(-1500, 1500)
        ax.set_ylim(-1500, 1500)
        ax.set_aspect('equal')
        ax.axhline(0, color='gray', linestyle='--')
        ax.axvline(0, color='gray', linestyle='--')
        ax.set_xlabel("Fx (N)")
        ax.set_ylabel("Fy (N)")
        
        # Calculate single point for current slider states
        from src.models.tire import compute_tire_forces
        fx, fy = compute_tire_forces(load_input, np.radians(steering_input), 0.0, config)
        ax.plot(fx, fy, 'ro', markersize=12, label="Current Force State")
        ax.legend()
        st.pyplot(fig)

with tab_dynamic:
    st.header("Dynamic Time-Domain Simulation")
    st.write("Simulates time-history response over a set duration.")
    
    duration = st.slider("Simulation Duration (s)", 1.0, 10.0, 5.0)
    if st.button("Run Dynamic Simulation"):
        history = run_dynamic_simulation(duration=duration, dt=0.05, config=config)
        
        # Plot time history using Matplotlib
        fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        ax[0].plot(history['time'], history['vy'], label="Lateral Velocity (vy)")
        ax[0].set_ylabel("Velocity (m/s)")
        ax[0].legend()
        ax[0].grid(True)
        
        ax[1].plot(history['time'], history['fy'], color='orange', label="Lateral Force (Fy)")
        ax[1].set_xlabel("Time (s)")
        ax[1].set_ylabel("Force (N)")
        ax[1].legend()
        ax[1].grid(True)
        
        st.pyplot(fig)

with tab_sweep:
    st.header("Steady-State Parameter Sweeps")
    st.write("Generates standard slip-angle vs. force curves across multiple normal loads.")
    
    if st.button("Generate Sweep Curves"):
        test_loads = [500.0, 1000.0, 1500.0]
        results = run_slip_angle_sweep(test_loads, config)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        for fz, data in results.items():
            ax.plot(data['slip_angles_deg'], data['fy'], label=f"Fz = {fz} N")
            
        ax.set_title("Slip Angle vs. Lateral Force")
        ax.set_xlabel("Slip Angle (deg)")
        ax.set_ylabel("Lateral Force Fy (N)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)