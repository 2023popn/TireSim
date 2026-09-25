import numpy as np

def calculate_temperature_factor(temp: float, model_type: str = "gaussian", opt_temp: float = 80.0) -> float:
    """
    Calculates the grip friction multiplier based on tire temperature 
    using the specified mathematical model.
    """
    if model_type == "gaussian":
        # Smooth bell-curve approach centered around opt_temp
        sigma = 25.0  # Controls the width of the optimal operating window
        diff = temp - opt_temp
        factor = np.exp(-(diff ** 2) / (2 * (sigma ** 2)))
        return max(0.2, factor)  # Floor grip at 20% so it never completely zeroes out
        
    elif model_type == "quadratic":
        # Parabolic approach: drops off symmetrically away from optimum
        a = -0.00032  # Curvature tuning coefficient
        diff = temp - opt_temp
        factor = 1.0 + a * (diff ** 2)
        return max(0.2, factor)
        
    else:
        # Fallback if an unknown model string is passed
        return 1.0