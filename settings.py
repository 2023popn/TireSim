## Simulation parameters

duration = 10 # simulation duration (s)
step = 0.001 # simulation time step (s)

simulation_type = "passive"

## Simulation procedure definition

# Passive type setup

def get_ground_speed(time):
  if time <= 0.03:
    return 100*time
    # speed increases linearly for the first 3 seconds

  elif time <= 7:
    return 3
    # speed is constant between 3 and 7 seconds

  else:
    return 10-time
    # speed decreases linearly for the last 3 seconds