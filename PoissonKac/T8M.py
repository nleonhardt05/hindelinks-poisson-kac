#!/usr/bin/env python3
"""
Task 8 - Gemittelte Geschwindigkeits-Autokorrelation C_v(t) ueber viele kurze Realisierungen.

Start: in VS Code einfach auf das Play-Symbol (Run Python File) klicken.
(Nicht "Run in Interactive Window"/Jupyter-Zellen verwenden - dort funktioniert
der STOP-Button nicht.)

Bedienung:
    * Pro hinzugefuegter Realisierung wird ein neuer Frame gezeichnet
      (Frame-Nummer steht in der Abbildung).
    * Klick auf "STOP" -> speichert Cv.csv (t, C_v(t)), schliesst den Film
      (Cv_movie.mp4, bzw. .gif als Fallback) und beendet das Programm.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib

# Interaktives Fenster erzwingen, damit der STOP-Button auch beim Start ueber
# den Play-Button in VS Code funktioniert (muss VOR dem Import von pyplot stehen).
try:
    _ip = get_ipython()          # nur definiert, wenn in IPython/Interactive Window
except NameError:
    _ip = None

if _ip is not None:
    # Interactive Window / IPython: Backend ueber die Magic setzen
    for _gui in ("osx", "tk", "qt"):
        try:
            _ip.run_line_magic("matplotlib", _gui)
            break
        except Exception:
            continue
else:
    # Normaler Start (Play-Button -> Run Python File)
    for _backend in ("MacOSX", "TkAgg", "QtAgg"):
        try:
            matplotlib.use(_backend, force=True)
            break
        except Exception:
            continue

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import animation

# ----------------------------------------------------------------------------
# Parameter (Aufgabenstellung)
# ----------------------------------------------------------------------------
X0 = 50.0      # Startposition (fuer die Trajektorie, hier nicht relevant fuer C_v)
MU = 0.5
S = 1.0
L = 3000.0     # Abbruchgrenze der langen Trajektorie (Task 4), hier irrelevant
DT = 0.5

T_MAX = 5.0 / MU                       # Laenge einer Realisierung: t < 5/mu = 10
N_STEPS = int(round(T_MAX / DT))       # 20 Schritte  -> Lags j = 0..19 -> t = 0..9.5
T = np.arange(N_STEPS) * DT            # Zeitachse t_j = j*dt

FPS = 20
# Ausgabedateien liegen immer neben diesem Skript, egal von wo gestartet wird
OUT_DIR = Path(__file__).resolve().parent
CSV_NAME = str(OUT_DIR / "Cv.csv")
MOVIE_BASENAME = str(OUT_DIR / "Cv_movie")

rng = np.random.default_rng()


# ----------------------------------------------------------------------------
# Trajektorien-Generator  <-- HIER ggf. DEINEN Algorithmus aus Task 4 einsetzen
# ----------------------------------------------------------------------------
def generate_velocities(n_steps):
    """Liefert n_steps Geschwindigkeitswerte v_1..v_n einer stationaeren Realisierung.

    Annahme (Ornstein-Uhlenbeck-Geschwindigkeit, konstantes dt, exaktes Update):
        v_{n+1} = a v_n + s*sqrt(1-a^2)*xi,   a = exp(-2 mu dt),   xi ~ N(0,1)
    -> <v^2> = s^2 und C_v(t) = s^2 exp(-2 mu t), wie in der Aufgabe.
    Start aus der stationaeren Verteilung N(0, s^2), damit kein Einschwingen
    die kurzen Zeitreihen verfaelscht.

    Wenn dein Algorithmus aus Task 4 anders aussieht: nur diese Funktion ersetzen.
    Sie muss ein 1D-numpy-Array der Laenge n_steps zurueckgeben.
    """
    a = np.exp(-2.0 * MU * DT)
    b = S * np.sqrt(1.0 - a * a)
    v = np.empty(n_steps)
    v[0] = rng.normal(0.0, S)
    for i in range(1, n_steps):
        v[i] = a * v[i - 1] + b * rng.normal()
    return v


# ----------------------------------------------------------------------------
# Autokorrelation exakt nach der Definition der Aufgabe
#   C_v(j dt) = 1/(N-j) * sum_{k=1}^{N-j} v_k v_{k+j}
# ----------------------------------------------------------------------------
def autocorr(v):
    n = len(v)
    return np.array([np.dot(v[: n - j], v[j:]) / (n - j) for j in range(n)])


def C_expected(t):
    return S**2 * np.exp(-2.0 * MU * t)


# ----------------------------------------------------------------------------
# Film-Writer: mp4 (ffmpeg) falls vorhanden, sonst gif (Pillow)
# ----------------------------------------------------------------------------
def make_writer():
    if animation.writers.is_available("ffmpeg"):
        w = animation.FFMpegWriter(
            fps=FPS, codec="libx264", bitrate=2500,
            extra_args=["-pix_fmt", "yuv420p"],   # QuickTime/macOS-kompatibel
        )
        return w, MOVIE_BASENAME + ".mp4"
    print("Hinweis: ffmpeg nicht gefunden -> speichere GIF. "
          "(Fuer mp4: conda install -c conda-forge ffmpeg)")
    return animation.PillowWriter(fps=FPS), MOVIE_BASENAME + ".gif"


# ----------------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------------
def main():
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.subplots_adjust(bottom=0.22, left=0.12, right=0.96, top=0.92)

    t_fine = np.linspace(0, T[-1], 400)
    ax.plot(t_fine, C_expected(t_fine), color="tab:blue", lw=2.5,
            label=r"erwartet: $s^2 e^{-2\mu t}$")
    (line,) = ax.plot(T, np.zeros_like(T), "-o", color="k", ms=6, lw=1,
                      label="gemessen (gemittelt)")
    ax.axhline(0, color="gray", lw=0.6)
    ax.set_xlim(0, T_MAX)
    ax.set_ylim(-0.4, 1.2)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$C_v(t)$")
    ax.set_title(r"Gemittelte Geschwindigkeits-Autokorrelation")
    ax.legend(loc="upper right")
    frame_txt = ax.text(0.97, 0.62, "", transform=ax.transAxes,
                        ha="right", va="top", fontsize=13)

    btn_ax = fig.add_axes([0.40, 0.04, 0.20, 0.09])
    btn = Button(btn_ax, "STOP", color="#f4b6b6", hovercolor="#e57373")
    state = {"stop": False}

    def on_stop(_event):
        state["stop"] = True

    btn.on_clicked(on_stop)
    fig.canvas.mpl_connect("close_event", lambda _e: state.update(stop=True))

    writer, movie_name = make_writer()
    writer.setup(fig, movie_name, dpi=120)

    plt.show(block=False)

    c_sum = np.zeros(N_STEPS)
    m = 0
    while not state["stop"]:
        m += 1
        c_sum += autocorr(generate_velocities(N_STEPS))
        c_avg = c_sum / m

        line.set_ydata(c_avg)
        frame_txt.set_text(f"Frame {m}")

        # Button nicht im Film zeigen
        btn_ax.set_visible(False)
        writer.grab_frame()
        btn_ax.set_visible(True)

        fig.canvas.draw_idle()
        plt.pause(0.001)             # GUI-Events (STOP-Klick) abarbeiten

    # --- Aufraeumen: Daten + Film speichern, dann beenden --------------------
    c_final = c_sum / max(m, 1)
    np.savetxt(CSV_NAME, np.column_stack([T, c_final]), delimiter=",",
               header="t,Cv", comments="")
    writer.finish()
    print(f"{m} Realisierungen -> {CSV_NAME} und {movie_name} gespeichert.")
    plt.close("all")
    sys.exit(0)


if __name__ == "__main__":
    main()
