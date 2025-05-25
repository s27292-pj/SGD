import numpy as np
import scipy.integrate

# Define the acceleration function (example: a = 2t)
def acceleration(t):
    return 2 * t

# Define the initial conditions
v0 = 0.0  # Initial velocity
x0 = 0.0  # Initial position

# Define the time range for integration
t_start = 0.0
t_end = 5.0
t_values = np.linspace(t_start, t_end, 100)

# Integrate acceleration to get velocity
velocity = scipy.integrate.cumulative_trapezoid(acceleration(t_values), t_values, initial=v0)

# Integrate velocity to get position
position = scipy.integrate.cumulative_trapezoid(velocity, t_values, initial=x0)

# Print the results
print("Time (t):", t_values)
print("Velocity (v):", velocity)
print("Position (x):", position)