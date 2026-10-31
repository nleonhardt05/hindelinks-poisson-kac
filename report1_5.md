Group report

# Poisson-Kac Process

This project simulates a Poisson-Kac process: a particle moves with constant speed $s=|v|$ along a line segment $[0,L]$ and reverses its velocity ($v \rightarrow -v$) at random times. The mean time between reversals is $\mu^{-1}$, where $\mu$ is the reversal rate. The experiment ends when the particle reaches $x=0$ or $x=L$. The full task description is in [README.md](README.md).

---

# Task 1 – Distribution of times between reversal events

Pick $N$ random times in $[0,T]$ as velocity reversal events and show that the intervals $\tau$ between them follow $p(\tau)=\mu e^{-\mu\tau}$ with $\mu=N/T$.

## Layout of the algorithm, functions to be created

No function is defined in `T1I.py`; the script works as follows:

1. Draw `N` uniformly distributed random reversal times in `[0, T]` (`np.random.uniform`).
2. Sort them and compute the intervals between consecutive events: `tau = np.diff(reversal_times)`.
3. Set `mu = N / T`.
4. Plot a normalized histogram of `tau` (`density=True`) together with the theoretical PDF $p(\tau)=\mu e^{-\mu\tau}$.
5. Save the plot with `plt.savefig("T1I.png")`.

## How to run the code

      python3 T1I.py

Requires `numpy` and `matplotlib`; no command-line arguments. Parameters at the top of the script:

| Parameter | Meaning | Value |
|---|---|---|
| `N` | number of random reversal events | 5000 |
| `T` | length of the time interval | 1000.0 |
| `mu` | event rate, computed as `N/T` | 5 |

## Resulting files

| File | Format | Meaning |
|---|---|---|
| `T1I.png` | PNG | Histogram of $\tau$ with the theoretical PDF, written by `plt.savefig("T1I.png")` into the folder the script is run from |

## Successful tests

- The histogram of the intervals agrees with $p(\tau)=\mu e^{-\mu\tau}$.
- The mean interval is $\langle\tau\rangle \approx T/N = \mu^{-1}$.

## Problems

- The 5000 events are drawn on a fixed interval, so the intervals are not exactly independent (only in the limit $N\to\infty$). No problems seen in practice.

## Results

Parameters: $N=5000$, $T=1000$, hence $\mu=5$. The resulting plot is saved as `T1I.png`.

The normalized histogram of the intervals between the 5000 random events follows the theoretical curve $p(\tau)=\mu e^{-\mu\tau}$.

Explanation: Picking $N$ uniformly random times in $[0,T]$ gives, for large $N$, a Poisson process with rate $\mu = N/T$. The probability that no event falls into an interval of length $\tau$ is $(1-\tau/T)^N \rightarrow e^{-\mu\tau}$. Differentiating this survival function gives $p(\tau)=\mu e^{-\mu\tau}$, with $\int_0^\infty p\,d\tau = 1$ and $\langle \tau \rangle = \mu^{-1} = T/N$.

---

# Task 5 – Exit probability $\pi_+^{(L)}(x_0)$

Simulate many trajectories with fixed time step $\Delta t$ that start at $x_0$ with velocity $+s$ and end at $x\le 0$ or $x\ge L$. Estimate the probability that the particle exits at $x=L$ and compare it with the analytical prediction $\frac{s+\mu x_0}{s+\mu L}$.

## Layout of the algorithm, functions to be created

      def simulate_trajectory(x0, initial_v):
          # Starts at x0 with velocity initial_v. In every time step dt the velocity
          # is flipped with probability p_flip = 1 - exp(-mu*dt), then the particle
          # moves by v*dt. Stops as soon as pos <= 0 or pos >= L.
          # returns 1 if the particle left at x = L, and 0 if it left at x = 0
          return ...

Main part of `T5I.py`:

- `x0_values`: 20 equidistant starting positions between `0.1` and `L - 0.1`.
- For each `x0`, `num_realizations` trajectories with `initial_v = +s` are simulated; the fraction that exits at `L` is the estimate of $\pi_+^{(L)}(x_0)$.
- The result is plotted together with the analytical prediction.

## How to run the code

      python3 T5I.py

Requires `numpy` and `matplotlib`; no command-line arguments. Parameters at the top of the script:

| Parameter | Meaning | Value |
|---|---|---|
| `L` | length of the interval | 10 |
| `mu` | reversal rate | 2 |
| `s` | speed | 1 |
| `dt` | time step | 0.01 |
| `num_realizations` | trajectories per `x0` | 2000 |

## Resulting files

| File | Format | Meaning |
|---|---|---|
| `images/task5.png` | PNG | $\pi_+^{(L)}(x_0)$, simulation vs. analytical |

The figure is saved from the matplotlib window into the same folder as the script runs in.

## Successful tests

- The simulated exit probabilities lie on the analytical line $\frac{s+\mu x_0}{s+\mu L}$ within the statistical error.

## Problems

- **Discretization:** With step `dt`, the particle can overshoot the boundary by up to $s\,dt$, and a reversal inside a step is not resolved. This causes a small systematic deviation that vanishes for $dt \ll \mu^{-1}$ (here $dt = 0.01 \ll 0.5$).
- **Speed:** The `while` loop in pure Python is slow for 2000 runs × 20 values of `x0`. Vectorizing over many particles with numpy would help.

## Results

Parameters: $L=10$, $\mu=2$, $s=1$, $\Delta t=0.01$, initial velocity $+s$, 2000 realizations per $x_0$ (final run).

Result: The simulation reproduces the linear dependence on $x_0$. At $x_0\rightarrow 0$ the probability is $s/(s+\mu L) = 1/21 \approx 0.048$, and at $x_0 \rightarrow L$ it tends to 1.

**Why it is not necessary to calculate all four probabilities:**

1. The particle always exits eventually, so $\pi_+^{(L)}(x_0) + \pi_+^{(0)}(x_0) = 1$ and $\pi_-^{(L)}(x_0) + \pi_-^{(0)}(x_0) = 1$. Each pair contains only one independent quantity.
2. The process is symmetric under reflection $x \rightarrow L-x$, $v \rightarrow -v$. A particle starting at $x_0$ with velocity $-s$ and exiting at $0$ corresponds to a particle starting at $L-x_0$ with velocity $+s$ and exiting at $L$, so $\pi_-^{(0)}(x_0)=\pi_+^{(L)}(L-x_0)$.

Together these give all four probabilities from $\pi_+^{(L)}(x_0)$ alone:

$$\pi_+^{(L)}(x_0) = 1-\pi_+^{(0)}(x_0) = \pi_-^{(0)}(L-x_0) = 1 - \pi_-^{(L)}(L-x_0).$$
