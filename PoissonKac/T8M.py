

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np

print("Matplotlib Backend:", matplotlib.get_backend())

x = np.linspace(0, 10, 100)
y = np.exp(-x)

fig, ax = plt.subplots()
ax.plot(x, y, "o-", label="Testkurve")
ax.set_xlabel("t")
ax.set_ylabel("y")
ax.set_title("Matplotlib-Test")
ax.grid(True)
ax.legend()

plt.show()
