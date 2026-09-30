# src/models/tire.py
import numpy as np
from src.config import TireConfig
from src.models.thermal import calculate_temperature_factor

class GoKartTire:
    def __init__(self, compound_name, mu_peak):
        """
        Initializes the Hoosier go-kart tire model for both longitudinal and lateral forces.
        
        Parameters:
        - compound_name (str): 'R55A' or 'R60B'
        - mu_peak (float): Peak friction coefficient
        """
        self.compound_name = compound_name
        self.mu_peak = mu_peak
        
        # Longitudinal Pacejka Parameters (approximate baseline for kart tires)
        self.Bx = 10.0
        self.Cx = 1.6
        self.Ex = 0.1
        
        # Lateral Pacejka Parameters (carried over from previous version)
        self.By = 8.0
        self.Cy = 1.4
        self.Ey = -0.1

    def magic_formula_longitudinal_force(self, kappa, Fz):
        """
        Calculates pure longitudinal force (Fx) using slip ratio (kappa).
        - kappa: Slip ratio (e.g., +0.1 for 10% slip acceleration, -0.1 for braking).
        - Fz: Vertical normal load.
        """
        Dx = self.mu_peak * Fz
        
        term = self.Bx * kappa
        inner_atan = np.arctan(term)
        argument = self.Cx * np.arctan(term - self.Ex * (term - inner_atan))
        
        Fx = Dx * np.sin(argument)
        return Fx

    def magic_formula_lateral_force(self, alpha_deg, gamma_deg, Fz):
        """
        Calculates lateral force (Fy) including Camber Angle (gamma).
        - alpha_deg: Slip angle in degrees
        - gamma_deg: Camber angle in degrees (positive = top of tire leans outward)
        - Fz: Vertical normal load
        """
        alpha_rad = np.radians(alpha_deg)
        gamma_rad = np.radians(gamma_deg)
        
        # 1. Camber reduces peak grip slightly due to smaller contact patch
        mu_effective = self.mu_peak * (1.0 - self.p_dy2 * (gamma_rad ** 2))
        Dy = mu_effective * Fz
        
        # 2. Calculate standard Pacejka core
        term = self.By * alpha_rad
        inner_atan = np.arctan(term)
        argument = self.Cy * np.arctan(term - self.Ey * (term - inner_atan))
        Fy_pure = Dy * np.sin(argument)
        
        # 3. Add Camber Thrust (Vertical shift S_Vy that creates force at alpha = 0)
        S_Vy = self.p_vy1 * Fz * gamma_rad
        
        # Total lateral force
        Fy_total = Fy_pure + S_Vy
        return Fy_total

    def combined_forces(self, alpha_deg, kappa, Fz):
        """
        Calculates combined longitudinal and lateral forces using a Friction Ellipse constraint.
        
        When a tire is both turning and braking/accelerating, the total force vector 
        cannot exceed the maximum friction ellipse limit defined by the tire's grip.
        """
        # 1. Calculate pure slip forces independently
        Fx0 = self.magic_formula_longitudinal_force(kappa, Fz)
        Fy0 = self.magic_formula_lateral_force(alpha_deg, Fz)
        
        # 2. Define maximum friction capacity for this vertical load
        F_max = self.mu_peak * Fz
        
        # 3. Apply Friction Ellipse / Circle Constraint
        # Calculate the magnitude of the pure force vector
        vector_magnitude = np.sqrt(Fx0**2 + Fy0**2)
        
        # If the combined demand exceeds the maximum available friction limit, 
        # scale both forces back proportionally to stay on the ellipse boundary.
        if vector_magnitude > F_max and vector_magnitude > 0:
            scaling_factor = F_max / vector_magnitude
            Fx_combined = Fx0 * scaling_factor
            Fy_combined = Fy0 * scaling_factor
        else:
            Fx_combined = Fx0
            Fy_combined = Fy0
            
        return Fx_combined, Fy_combined
