import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()


s = 1                              
v = s                              
mu = 0.5                           
L = 3000                           
dt = 0.5                           
x_0 = 50                           
probability = 1 - np.exp(-mu * dt) 


velocity = [v]                     # Liste aller Geschwindigkeiten, eine pro Zeitschritt
pos = x_0

while 0 < pos < L:                 # läuft, bis das Teilchen einen Rand erreicht
    if rng.random() < probability: # mit Wahrscheinlichkeit f: Richtung umkehren
        v = -v
    pos += v * dt                  # Teilchen um v*dt bewegen
    velocity.append(v)             # Geschwindigkeit dieses Schritts speichern



n_lags = 40
C_v = np.zeros(n_lags)

for i in range(len(velocity) - n_lags):   # Startindex k
    for j in range(n_lags):                # Zeitverschiebung j
        C_v[j] += velocity[i] * velocity[i + j]

C_v /= len(velocity) - n_lags              # Mittelwert über alle Paare
print(C_v)


t = np.arange(n_lags) * dt                 # Zeitachse t = j*dt
C_theory = s**2 * np.exp(-2 * mu * t)      # theoretische Vorhersage s^2 * exp(-2*mu*t)

plt.plot(t, C_v, 'o', markersize=4, label='Simulation')
plt.plot(t, C_theory, '-', label=r'Theorie $s^2 e^{-2\mu t}$')
plt.xlabel('t')
plt.ylabel(r'$C_v(t)$')
plt.title('Geschwindigkeitsautokorrelation')
plt.legend()
plt.grid()
plt.show()