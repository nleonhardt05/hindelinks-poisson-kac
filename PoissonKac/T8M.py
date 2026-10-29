
import numpy as np
import matplotlib

# Interaktives Fenster (vor dem Import von pyplot). Im normalen Start auf dem Mac: MacOSX.
try:
    _ip = get_ipython()                      # nur im Interactive Window / IPython definiert
except NameError:
    _ip = None

if _ip is not None:
    try:
        _ip.run_line_magic("matplotlib", "osx")
    except Exception:
        pass
else:
    import sys
    if sys.platform == "darwin":             # nur auf dem Mac erzwingen
        matplotlib.use("MacOSX", force=True)

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ADDED: saving the animation and CSV
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

MU, S, DT = 0.5, 1.0, 0.5
T_MAX = 5.0 / MU                       # Laenge einer Realisierung: t < 5/mu = 10
N_STEPS = int(round(T_MAX / DT))       # 20 Schritte -> t = 0 ... 9.5
T = np.arange(N_STEPS) * DT
MAX_FRAMES = None                      # nur zum Testen: z.B. 200, sonst None

rng = np.random.default_rng()


def generate_velocities(n):
    """Eine stationaere Realisierung (Annahme: OU-Geschwindigkeit, exaktes Update).
    <-- Hier ggf. deinen Task-4-Algorithmus einsetzen."""
    a = np.exp(-2.0 * MU * DT)
    b = S * np.sqrt(1.0 - a * a)
    v = np.empty(n)
    v[0] = rng.normal(0.0, S)
    for i in range(1, n):
        v[i] = a * v[i - 1] + b * rng.normal()
    return v


def autocorr(v):
    """C_v(j dt) = 1/(N-j) * sum_{k=1}^{N-j} v_k v_{k+j}"""
    n = len(v)
    return np.array([
        np.dot(v[: n - j], v[j:]) / (n - j)
        for j in range(n)
    ])


def main():
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.subplots_adjust(bottom=0.22)

    tf = np.linspace(0, T[-1], 400)
    ax.plot(
        tf,
        S**2 * np.exp(-2 * MU * tf),
        color="tab:blue",
        lw=2.5,
        label=r"erwartet: $s^2 e^{-2\mu t}$"
    )

    (line,) = ax.plot(
        T, np.zeros(N_STEPS), "-o",
        color="k", ms=6, lw=1,
        label="gemessen (gemittelt)"
    )

    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlim(0, T_MAX)
    ax.set_ylim(-0.4, 1.2)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$C_v(t)$")
    ax.legend(loc="upper right")

    txt = ax.text(
        0.97, 0.62, "Frame 0",
        transform=ax.transAxes,
        ha="right", va="top", fontsize=13
    )

    btn_ax = fig.add_axes([0.40, 0.04, 0.20, 0.09])
    btn = Button(
        btn_ax, "STOP",
        color="#f4b6b6",
        hovercolor="#e57373"
    )

    state = {"stop": False}
    btn.on_clicked(lambda _e: state.update(stop=True))
    fig.canvas.mpl_connect(
        "close_event",
        lambda _e: state.update(stop=True)
    )

    plt.ion()
    plt.show(block=False)

    c_sum = np.zeros(N_STEPS)
    m = 0

    # ADDED: store the averaged curve after every realization
    c_history = []

    while not state["stop"]:
        m += 1
        c_sum += autocorr(generate_velocities(N_STEPS))

        current_cv = c_sum / m
        line.set_ydata(current_cv)
        txt.set_text(f"Frame {m}")

        # Save each intermediate averaged curve for the GIF
        c_history.append(current_cv.copy())

        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        plt.pause(0.02)                    # laesst das Fenster neu zeichnen + Klicks zu

        if MAX_FRAMES and m >= MAX_FRAMES:
            break

    print(f"Gestoppt nach {m} Realisierungen.")

    final_cv = c_sum / m
    print("C_v(0) gemessen:", final_cv[0], " erwartet:", S**2)

    # ADDED: save files in the correct repository directory
    output_dir = (
        Path.home()
        / "hindelinks-poisson-kac"
        / "PoissonKac"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    print("Saving results to:", output_dir)

    # ADDED: save final t and Cv(t) values to CSV
    np.savetxt(
        output_dir / "Cv.csv",
        np.column_stack((T, final_cv)),
        delimiter=",",
        header="t,Cv",
        comments=""
    )

    print(f"CSV saved to: {output_dir / 'Cv.csv'}")

    # ADDED: create a movie from the stored realizations
    def update_animation(frame):
        line.set_ydata(c_history[frame])
        txt.set_text(f"Frame {frame + 1}")
        return line, txt

    animation = FuncAnimation(
        fig,
        update_animation,
        frames=len(c_history),
        interval=100,
        repeat=False,
        blit=False
    )

    # ADDED: save the animation as a GIF
    animation.save(
        output_dir / "Cv_evolution.gif",
        writer=PillowWriter(fps=10)
    )

    # Restore the final curve in the interactive figure
    line.set_ydata(final_cv)
    txt.set_text(f"Frame {m}")
    fig.canvas.draw_idle()

    print(f"Animation saved to: {output_dir / 'Cv_evolution.gif'}")

    return final_cv


if __name__ == "__main__":
    main()
