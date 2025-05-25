import random
import matplotlib.pyplot as plt

INTERVAL = 100

circle_points = 0
square_points = 0

# Lists to store points for visualization
inside_x = []
inside_y = []
outside_x = []
outside_y = []

# Total Random numbers generated = possible x values * possible y values
for i in range(INTERVAL ** 2):
    # Randomly generated x and y values from a uniform distribution
    rand_x = random.uniform(-1, 1)
    rand_y = random.uniform(-1, 1)

    # Distance between (x, y) from the origin
    origin_dist = rand_x ** 2 + rand_y ** 2

    # Checking if (x, y) lies inside the circle
    if origin_dist <= 1:
        circle_points += 1
        inside_x.append(rand_x)
        inside_y.append(rand_y)
    else:
        outside_x.append(rand_x)
        outside_y.append(rand_y)

    square_points += 1

# Estimating value of pi
pi = 4 * circle_points / square_points
print("Final Estimation of Pi =", pi)

# Visualization
plt.figure(figsize=(8, 8))
plt.scatter(inside_x, inside_y, color='blue', s=1, label='Inside Circle')
plt.scatter(outside_x, outside_y, color='red', s=1, label='Outside Circle')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.title(f"Monte Carlo Pi Estimation\nEstimated Pi = {pi}")
plt.legend()
plt.show()