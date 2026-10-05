import numpy as np
import matplotlib.pyplot as plt

mu = 2
N = 1000
p = np.random.rand(N)

#p = 1 - np.exp(-mu * tau)
tau = -np.log(1 - p) / mu

plt.hist(tau, bins=100, density=True, label="Simulation")

t = np.linspace(0, tau.max(), 500)

plt.plot(t, mu*np.exp(-mu*t), 'r', label=r"$\mu e^{-\mu\tau}$")

plt.xlabel(r"$\tau$"); plt.ylabel(r"$p(\tau)$"); plt.legend()

plt.show()