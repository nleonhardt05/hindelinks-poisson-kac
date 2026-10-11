import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

L = 10
mu = 2
s = 1
dt = 0.01
num_realizations = 2000 #Use 2000 for final results, but 20 for quick testing

#Calculated Prob.
p_flip = 1 - np.exp(-mu * dt)


def simulate_trajectory(x0, initial_v):
    pos = x0
    v = initial_v
    t = 0

    while 0 < pos < L:
        if rng.random() < p_flip:
            v = -v
        pos += v * dt
        t += dt
        # counting time until the particle exits the interval [0, L]
        # dt is the time step; we add it to t in every iteration
    exit_at_L = 1 if pos >= L else 0
    return exit_at_L, t

#different x0 values.
x0_values = np.linspace(0.1, L - 0.1, 20)

# variables to store the results for my equations
T_plus, T_minus = [], []
pi_plus, pi_minus = [], []

for x0 in x0_values:
    # when initial velocity is +s we marked them with p
    times_p, exits_p = [], []
    # when initial velocity is -s we marked them with m
    times_m, exits_m = [], []

    for _ in range(num_realizations):

        e, t = simulate_trajectory(x0, initial_v=+s) # initial velocity is +s
        exits_p.append(e)
        times_p.append(t)

        e, t = simulate_trajectory(x0, initial_v=-s) # initial velocity is -s
        exits_m.append(e)
        times_m.append(t)

    T_plus.append(np.mean(times_p)) # append the average exit time for initial velocity +s
    T_minus.append(np.mean(times_m)) # append the average exit time for initial velocity -s
    pi_plus.append(np.mean(exits_p)) # append the average exit probability for initial velocity +s
    pi_minus.append(np.mean(exits_m)) # append the average exit probability for initial velocity -s

# transform lists to numpy arrays for easier handling
T_plus, T_minus = np.array(T_plus), np.array(T_minus)
pi_plus, pi_minus = np.array(pi_plus), np.array(pi_minus)


# left sites of the equations
sim_T_avg = (T_plus + T_minus) / 2
sim_pi_expr = (pi_plus + pi_minus) / 2 * L - x0_values

# right sites of the equations
theory_T_avg = L / (2*s) + mu * x0_values * (L - x0_values) / s**2
theory_pi_expr = s * (L - 2*x0_values) / (2 * (s + mu*L))

# Plotting the results
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(x0_values, sim_T_avg, label='Simulated T_avg', marker='o')
plt.plot(x0_values, theory_T_avg, label='Theoretical T_avg', linestyle='--')
plt.xlabel('Initial Position x0')
plt.ylabel('Average Exit Time T_avg')
plt.title('Average Exit Time vs Initial Position')
plt.legend()
plt.grid()
plt.subplot(1, 2, 2)
plt.scatter(x0_values, sim_pi_expr, label='Simulated pi_expr', marker='o')
plt.plot(x0_values, theory_pi_expr, label='Theoretical pi_expr', linestyle='--')
plt.ylim(-0.3, 0.3)
plt.xlabel('Initial Position x0')
plt.ylabel('Exit Probability Expression pi_expr')
plt.title('Exit Probability Expression vs Initial Position')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()  