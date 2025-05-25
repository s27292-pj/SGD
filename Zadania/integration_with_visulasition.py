import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt

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

# Plot the results
plt.figure(figsize=(10, 6))

# Plot acceleration
plt.subplot(3, 1, 1)
plt.plot(t_values, acceleration(t_values), label="Acceleration (a)", color="red")
plt.xlabel("Time (t)")
plt.ylabel("Acceleration (a)")
plt.title("Acceleration vs Time")
plt.grid()
plt.legend()

# Plot velocity
plt.subplot(3, 1, 2)
plt.plot(t_values, velocity, label="Velocity (v)", color="blue")
plt.xlabel("Time (t)")
plt.ylabel("Velocity (v)")
plt.title("Velocity vs Time")
plt.grid()
plt.legend()

# Plot position
plt.subplot(3, 1, 3)
plt.plot(t_values, position, label="Position (x)", color="green")
plt.xlabel("Time (t)")
plt.ylabel("Position (x)")
plt.title("Position vs Time")
plt.grid()
plt.legend()

# Adjust layout and show the plot
plt.tight_layout()
plt.show()