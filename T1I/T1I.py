import numpy as np
import matplotlib.pyplot as plt

#Deff. Params.
N = 5000       # Number of random reversal events
T = 1000.0     # Total time interval
mu = N / T     # Average event rate (events per unit time)


reversal_times = np.random.uniform(0, T, N)

reversal_times.sort()

tau = np.diff(reversal_times)

#Plot
plt.figure(figsize=(8, 5))
plt.hist(tau, bins=50, density=True, label='Simulated Intervals (Histogram)')

#therortical PDF vals.
tau_axis = np.linspace(0, np.max(tau), 200)
theoretical_pdf = mu * np.exp(-mu * tau_axis)

#Plot the theoretical curve
plt.plot(tau_axis, theoretical_pdf, label='Theoretical PDF: tau = mu e^-(mu*tau)')
plt.title('Poisson Kac')
plt.xlabel('Time between events (tau)')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)

plt.show()
