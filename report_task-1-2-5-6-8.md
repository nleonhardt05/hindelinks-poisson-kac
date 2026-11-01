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

# Task 2 – Generating exponentially distributed times

Generate random times $\tau$ that follow $p(\tau)=\mu e^{-\mu\tau}$ directly, using the inverse of the cumulative distribution function (inverse transform sampling), and compare them with the analytical PDF.

## Layout of the algorithm, functions to be created

No function is defined in `T2I.py`; the script works as follows:

1. Draw `N` uniformly distributed random numbers `p` in $[0,1)$ (`np.random.rand`).
2. Transform them with the inverse CDF $\tau = -\ln(1-p)/\mu$, which follows from $p = 1 - e^{-\mu\tau}$.
3. Plot a normalized histogram of `tau` (`density=True`, 100 bins).
4. Plot the theoretical PDF $\mu e^{-\mu\tau}$ over the range $[0, \tau_{max}]$ and show the figure with `plt.show()`.

## How to run the code

      python3 T2I.py

Requires `numpy` and `matplotlib`; no command-line arguments. Parameters at the top of the script:

| Parameter | Meaning | Value |
|---|---|---|
| `mu` | reversal rate | 2 |
| `N` | number of generated times | 1000 |

## Resulting files

No file is written. The figure is only shown in the matplotlib window (`plt.show()`) and has to be saved manually.

## Successful tests

- The histogram of `tau` agrees with $p(\tau)=\mu e^{-\mu\tau}$.
- The mean value is $\langle\tau\rangle \approx \mu^{-1} = 0.5$.

## Problems

- No problems occurred. Since `np.random.rand` returns values in $[0,1)$, the argument of the logarithm $1-p$ is never 0, so $\ln(0)$ cannot occur.

## Results

Parameters: $\mu=2$, $N=1000$.

The normalized histogram of the generated times follows the theoretical curve $\mu e^{-\mu\tau}$. With only 1000 samples and 100 bins the histogram fluctuates visibly, especially in the tail.

Explanation: If $p$ is uniformly distributed in $[0,1)$, then $\tau = F^{-1}(p)$ has exactly the distribution with CDF $F$. For $F(\tau)=1-e^{-\mu\tau}$ the inverse is $\tau=-\ln(1-p)/\mu$. In contrast to Task 1, the times are independent and exactly exponentially distributed for every $N$, not only in the limit $N\to\infty$.

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
---

# Task 6 – Mean exit time and exit probability for both initial velocities

Extend Task 5: simulate trajectories with fixed time step $\Delta t$ for both initial velocities $+s$ and $-s$, and measure the mean exit times $T_\pm(x_0)$ and the exit probabilities $\pi_\pm^{(L)}(x_0)$. Compare the combinations $T_{avg}=\frac{T_++T_-}{2}$ and $\frac{\pi_+^{(L)}+\pi_-^{(L)}}{2}L-x_0$ with the analytical predictions.

## Layout of the algorithm, functions to be created

      def simulate_trajectory(x0, initial_v):
          # Starts at x0 with velocity initial_v. In every time step dt the velocity
          # is flipped with probability p_flip = 1 - exp(-mu*dt), then the particle
          # moves by v*dt and the time t is increased by dt.
          # Stops as soon as pos <= 0 or pos >= L.
          # returns (exit_at_L, t): exit_at_L = 1 if the particle left at x = L,
          # 0 if it left at x = 0, and t = exit time
          return ...

Main part of `T6I.py`:

- `x0_values`: 20 equidistant starting positions between `0.1` and `L - 0.1`.
- For each `x0`, `num_realizations` trajectories are simulated for `initial_v = +s` and for `initial_v = -s`. The averages give $T_\pm$ and $\pi_\pm^{(L)}$.
- Left-hand sides: `sim_T_avg = (T_plus + T_minus)/2` and `sim_pi_expr = (pi_plus + pi_minus)/2 * L - x0_values`.
- Right-hand sides (theory): $\frac{L}{2s}+\frac{\mu x_0(L-x_0)}{s^2}$ and $\frac{s(L-2x_0)}{2(s+\mu L)}$.
- Both are plotted against $x_0$ in two subplots (simulation as points, theory as dashed line).

## How to run the code

      python3 T6I.py

Requires `numpy` and `matplotlib`; no command-line arguments. Parameters at the top of the script:

| Parameter | Meaning | Value |
|---|---|---|
| `L` | length of the interval | 10 |
| `mu` | reversal rate | 2 |
| `s` | speed | 1 |
| `dt` | time step | 0.01 |
| `num_realizations` | trajectories per `x0` and velocity | 2000 (20 for quick tests) |

## Resulting files

No file is written. The figure with both subplots is only shown in the matplotlib window (`plt.show()`) and has to be saved manually.

## Successful tests

- The simulated $T_{avg}$ lies on the analytical curve within the statistical error.
- The simulated expression $\frac{\pi_++\pi_-}{2}L-x_0$ lies on the analytical line $\frac{s(L-2x_0)}{2(s+\mu L)}$ within the statistical error.

## Problems

- **Discretization:** As in Task 5, the particle can overshoot the boundary by up to $s\,dt$, and a reversal inside a step is not resolved. The measured exit times are therefore slightly too large by up to $dt$. The effect vanishes for $dt \ll \mu^{-1}$ (here $dt=0.01 \ll 0.5$).
- **Speed:** With 2000 realizations × 20 values of `x0` × 2 velocities there are 80 000 trajectories, each in a pure Python `while` loop, so the run is slow. Hence the quick-test value of 20 realizations.
- **Statistics:** The expression $\frac{\pi_++\pi_-}{2}L-x_0$ is a small difference of large numbers (it lies only between $-0.3$ and $0.3$, see `plt.ylim`), so the statistical error is clearly visible.

## Results

Parameters: $L=10$, $\mu=2$, $s=1$, $\Delta t=0.01$, 2000 realizations per $x_0$ and initial velocity (final run).

Result: Both simulated quantities reproduce the analytical predictions. $T_{avg}$ is a parabola in $x_0$ that is symmetric around $L/2$ with its maximum at $x_0=L/2$. The expression $\frac{\pi_++\pi_-}{2}L-x_0$ is a straight line that decreases linearly from $\frac{sL}{2(s+\mu L)}$ at $x_0=0$ to $-\frac{sL}{2(s+\mu L)}$ at $x_0=L$ and vanishes at $x_0=L/2$.

Explanation of the exit-probability expression: Using $\pi_+^{(L)}=\frac{s+\mu x_0}{s+\mu L}$ and $\pi_-^{(L)}=\frac{\mu x_0}{s+\mu L}$ one gets

$$\frac{\pi_+^{(L)}+\pi_-^{(L)}}{2}L-x_0=\frac{L(s+2\mu x_0)}{2(s+\mu L)}-x_0=\frac{s(L-2x_0)}{2(s+\mu L)}.$$

The $\mu$-dependent terms cancel, so only the slope $-s/(s+\mu L)$ remains.

---
# Task 8 – Velocity autocorrelation function $C_v(t)$

Generate velocity time series $v_k$ on a grid with time step $\Delta t$, compute their autocorrelation function $C_v(j\Delta t)$, average it over many realizations and compare it with the analytical prediction $C_v(t)=s^2e^{-2\mu t}$.

## Layout of the algorithm, functions to be created

      def generate_velocities(n):
          # Draws v_1 ~ N(0, s^2) and then iterates
          # v_i = a*v_{i-1} + b*xi_i with a = exp(-2*mu*dt), b = s*sqrt(1-a^2)
          # and xi_i ~ N(0,1). Returns an array of n velocities.
          return v

      def autocorr(v):
          # C_v(j dt) = 1/(N-j) * sum_{k=1}^{N-j} v_k v_{k+j}  for j = 0, ..., N-1
          return C

      def main():
          # Sets up the plot with a STOP button, averages C_v over realizations
          # until STOP is clicked, saves the CSV and the GIF, returns the final C_v.
          return final_cv

Main part of `main()`:

- Time grid: `T = np.arange(N_STEPS) * DT` with `T_MAX = 5/MU` and `N_STEPS = round(T_MAX/DT)`.
- In every loop pass a new velocity series is generated, its autocorrelation is added to `c_sum`, and the running average `c_sum / m` is drawn into the plot together with the expected curve $s^2e^{-2\mu t}$.
- Every intermediate average is stored in `c_history`. After the STOP button (or closing the window) the final result is written to a CSV file and the evolution of the average is saved as a GIF.

## How to run the code

      python3 T8I.py

Requires `numpy`, `matplotlib` and `pillow` (for the GIF); no command-line arguments. The program runs until the STOP button is clicked or the window is closed. Parameters at the top of the script:

| Parameter | Meaning | Value |
|---|---|---|
| `MU` | reversal rate | 0.5 |
| `S` | speed | 1.0 |
| `DT` | time step | 0.5 |
| `T_MAX` | length of one time series, `5/MU` | 10 |
| `N_STEPS` | points per time series, `T_MAX/DT` | 20 |
| `MAX_FRAMES` | optional limit for the number of realizations (`None` = until STOP) | `None` |

On macOS the `MacOSX` backend (`%matplotlib osx` in IPython) is selected automatically.

## Resulting files

| File | Format | Meaning |
|---|---|---|
| `Cv.csv` | CSV (columns `t,Cv`) | Final averaged $C_v(t)$ over all realizations |
| `Cv_evolution.gif` | GIF | Evolution of the averaged $C_v(t)$ with the number of realizations |

Both files are written to `~/hindelinks-poisson-kac/PoissonKac/` (the folder is created if it does not exist). The path is hard-coded and has to be changed on other computers.

## Successful tests

- The measured $C_v(0)$ agrees with the expected value $s^2=1$ (printed at the end of the run).
- The averaged curve approaches $s^2e^{-2\mu t}$ with a growing number of realizations; the fluctuations around the theory curve shrink visibly.

## Problems

- **Mac backend:** With the default settings, the plot window did not work properly on macOS. The backend had to be set explicitly (`matplotlib.use("MacOSX")` or `%matplotlib osx`), and this has to happen before `matplotlib.pyplot` is imported. This is why the script begins with the `get_ipython()` check.
- **Plot did not update:** At the beginning the window always showed the same picture, although the simulation kept running in the background and the data were computed correctly. The reason was that the GUI event loop was never given time to redraw. This is solved by `plt.ion()`, `plt.show(block=False)` and, in every pass of the loop, `fig.canvas.draw_idle()`, `fig.canvas.flush_events()` and `plt.pause(0.02)`.
- **Saving the image series:** Saving the frames as a GIF was confusing at first. `FuncAnimation` is created only after the simulation has stopped and replays `c_history` with `PillowWriter`. Saving takes noticeably longer the more realizations were run, since every realization is one frame, and the GIF becomes large.
- **Velocity distribution:** The generated velocities are Gaussian-distributed (an AR(1) process), not $\pm s$ as in the real Poisson-Kac process. Both have the same autocorrelation $s^2e^{-2\mu t}$, which is all that is tested here, but the series are not real Poisson-Kac trajectories.
- **Statistics for large $t$:** With $N=20$ points per series the estimator for large $j$ uses only a few products ($N-j$ terms), so single realizations are very noisy and only the average over many realizations is meaningful.

## Results

Parameters: $\mu=0.5$, $s=1$, $\Delta t=0.5$, $T_{max}=10$, number of realizations $m$ determined by the STOP button.

Result: The averaged autocorrelation $C_v(t)$ decays exponentially from $C_v(0)=s^2$ and follows the theoretical curve $s^2e^{-2\mu t}$. In the GIF one can see how the very noisy average of the first realizations converges to the theory curve.

Explanation: The recursion $v_i=a\,v_{i-1}+b\,\xi_i$ with $a=e^{-2\mu\Delta t}$ and $b=s\sqrt{1-a^2}$ generates a stationary series with variance $s^2$, since $a^2s^2+b^2=s^2$. Its correlation is $\langle v_kv_{k+j}\rangle=a^j s^2=s^2e^{-2\mu j\Delta t}$. For the Poisson-Kac process this is the exact result: the product $v(0)v(t)$ is $s^2$ if the number of reversals in $[0,t]$ is even and $-s^2$ if it is odd, and for Poisson-distributed reversal numbers this gives $s^2e^{-2\mu t}$.
