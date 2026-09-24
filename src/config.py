# src/config.py
class TireConfig:
    # Basic tire properties
    unloaded_radius = 0.135       # meters (typical go-kart rear/front tire size proxy)
    mu_peak = 1.4                 # Peak friction coefficient
    cornering_stiffness = 500.0   # N/deg (or N/rad)
    load_sensitivity = 0.05       # How friction drops as normal load increases