## Measured Constants

g = 9.81 # gravity (m / s^2)
m_wheel = 5 # mass of wheel (kg)
m_applied = 10 # mass applied to wheel (kg)

mu_static = 0.9 # coeff of static friction
mu_dynamic = 0.5 # coeff of dynamic friction

r = 0.25 # wheel radius (m)


## Calculated Constants

m_total = m_wheel + m_applied # total mass supported by contact patch

I = 0.5 * m_wheel * r**2 # moment of inertia of the wheel

N = m_total * g # Normal Force
max_static_friction = N * mu_static # maximum static friction
dynamic_friction = N * mu_dynamic # dynamic friction