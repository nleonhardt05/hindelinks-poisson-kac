import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

L = 10
mu = 2
s = 1
dt = 0.01
num_realizations = 20 #Use 2000 for final results, but 20 for quick testing

#Calculated Prob.
p_flip = 1 - np.exp(-mu * dt)

def simulate_trajectory(x0, initial_v):
    pos = x0
    v = initial_v

    while 0 < pos < L:
        if rng.random() < p_flip:
            v = -v
        pos += v * dt

    return 1 if pos >= L else 0 # Return 1 if it exited at L, 0 if it exited at 0

#different x0 vals.
x0_values = np.linspace(0.1, L - 0.1, 20)
simulated_pi_plus_L = []

#Run 2000 times for each x0
for x0 in x0_values:
    exits_at_L = 0
    for _ in range(num_realizations):
        exits_at_L += simulate_trajectory(x0, initial_v=s)
    
    #Calculate simulated probability
    simulated_pi_plus_L.append(exits_at_L / num_realizations)

#Simulated probabilities
analytical_pi_plus_L = (s + mu * x0_values) / (s + mu * L)

#Plotting
plt.figure(figsize=(8, 5))
plt.scatter(x0_values, simulated_pi_plus_L, color='blue', label='Simulation (2000 runs)')
plt.plot(x0_values, analytical_pi_plus_L, color='red', linestyle='--', label='Analytical Prediction')

plt.title('Task 5: Verification of Exit Probability pi^L(x_0)')
plt.xlabel('Initial Position x_0')
plt.ylabel('Probability')
plt.xlim(0, L)
plt.ylim(0, 1.05)
plt.grid(True, linestyle=':')
plt.legend()
plt.show()
