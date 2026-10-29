import numpy as np 
rng = np.random.default_rng()
import matplotlib.pyplot as plt

v = 1
n = 200
my = 10
dt = 1/(4*my)
probability = 0.6  # 1 - np.exp(-my *dt)
revearse = 0
positions = [0]
pos = 0

for i in range(n):
    if rng.random() < probability:
        v = -v
        revearse += 1
        pos += v * dt
        positions.append(pos)
    else:
        pos += v * dt
        positions.append(pos)


print(revearse)
berechnet = revearse / n

print (f"Berechnet: {berechnet}  Vorlage: {probability}")

plt.plot(positions, color = 'black', marker="o", markerfacecolor="black", markeredgecolor="blue", markersize=3, linewidth=1)
plt.title('Task 4')
plt.xlabel("Time")
plt.ylabel("Position")
plt.grid()
plt.show

