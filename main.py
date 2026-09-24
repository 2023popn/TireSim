# main.py
from src.config import TireConfig
from src.solvers.sweeps import run_slip_angle_sweep
from src.solvers.realtime import run_live_simulation
from src.utils.plotting import plot_sweep_results

def main():
    config = TireConfig()
    
    mode = "live" # Change to "sweep" or "dynamic" whenever you want
    
    if mode == "sweep":
        print("Running static slip angle sweep...")
        results = run_slip_angle_sweep([500.0, 1000.0, 1500.0], config)
        plot_sweep_results(results)
        
    elif mode == "live":
        print("Launching live tire physics simulator...")
        run_live_simulation(config)

if __name__ == "__main__":
    main()