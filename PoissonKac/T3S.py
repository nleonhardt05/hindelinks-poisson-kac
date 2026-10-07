import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()



s = 1
m = 10
N = 40
delta_t = 0.25 / m
Ereignis = np.zeros((2,N+1))
Ereignis[0,0] = 0
Gleichmässig = [0]
t_g = delta_t

for i in range(1,N+1):
    P = rng.random()
    t = -np.log(1 - P) / m
    Ereignis[1,i] = Ereignis[1,i-1] + t * s
    Ereignis[0,i] = Ereignis[0,i-1] + t

    while t_g < Ereignis[0,i]:
        Gleichmässig.append(Ereignis[1,i-1] + s * (t_g - Ereignis[0,i-1]))
        t_g += delta_t
    s = -s


x = Gleichmässig
y = np.arange(0, Ereignis[0,-1], delta_t)


plt.plot(y, x, marker='o', markersize=2)
plt.plot(Ereignis[0], Ereignis[1], marker='o', fillstyle='none', linestyle='None')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Poisson Process Simulation')
plt.grid()
plt.show()




