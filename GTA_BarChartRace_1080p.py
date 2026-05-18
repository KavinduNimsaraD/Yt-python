import pandas as pd
import numpy as np
import bar_chart_race as bcr
import matplotlib.pyplot as plt

print("දත්ත සකස් කරමින් පවතී...")

# --- Helper: smooth growth curve ---
def smooth_growth(start, end, n):
    t = np.linspace(-3, 3, n)
    s = 1 / (1 + np.exp(-t))
    return start + (end - start) * s

# --- Milestone data (Millions) ---
milestones = {
    "GTA III": [
        ("2001-10-01", 0),
        ("2008-03-01", 14.5),
        ("2026-05-01", 14.5),
    ],
    "GTA Vice City": [
        ("2002-10-01", 0),
        ("2008-03-01", 17.5),
        ("2026-05-01", 17.5),
    ],
    "GTA San Andreas": [
        ("2004-10-01", 0),
        ("2011-01-01", 27.5),
        ("2026-05-01", 27.5),
    ],
    "GTA IV": [
        ("2008-04-01", 0),
        ("2013-07-01", 25.0),
        ("2026-05-01", 25.0),
    ],
    "GTA V": [
        ("2013-09-01", 0),
        ("2025-11-01", 220.0),
        ("2026-05-01", 220.0),
    ],
}

# --- Build monthly dataframe with smooth growth ---
all_dates = pd.date_range("2001-10-01", "2026-05-01", freq="MS")
df = pd.DataFrame(index=all_dates)

for game, points in milestones.items():
    series = pd.Series(index=all_dates, dtype=float)
    for (d1, v1), (d2, v2) in zip(points[:-1], points[1:]):
        d1 = pd.to_datetime(d1)
        d2 = pd.to_datetime(d2)
        idx = pd.date_range(d1, d2, freq="MS")
        series.loc[idx] = smooth_growth(v1, v2, len(idx))
    df[game] = series

df = df.fillna(0)

# ✅ start from first non-zero to avoid blank frames
nonzero = df.max(axis=1) > 0
df = df.loc[nonzero.idxmax():]

df.index = df.index.strftime("%Y %b")

# --- Style (Full HD) ---
plt.style.use("default")
plt.rcParams["figure.figsize"] = (16, 9)
plt.rcParams["figure.dpi"] = 120
plt.rcParams["figure.facecolor"] = "#F7F8FA"
plt.rcParams["axes.facecolor"] = "#FFFFFF"

# --- Duration ---
target_seconds = 380
period_length = int((target_seconds * 1000) / len(df))

print(f"Estimated video length ≈ {len(df) * period_length / 1000:.1f} seconds")
print("🎬 1080p Full HD Video එක Render වෙමින් පවතී...")

bcr.bar_chart_race(
    df=df,
    filename="GTA_Evolution_1080p.mp4",
    orientation="h",
    sort="desc",
    n_bars=5,
    steps_per_period=30,
    period_length=period_length,
    title="Evolution of GTA Series (Copies Sold in Millions)",
    cmap="Set2",
    tick_label_size=14,
    bar_label_size=16,
    period_label={"x": 0.95, "y": 0.15, "ha": "right", "va": "center",
                  "size": 45, "weight": "bold", "color": "#333333"},
    bar_kwargs={"alpha": 0.9, "lw": 1}
)

print("✅ වැඩේ හරි! 'GTA_Evolution_1080p.mp4' නමින් Video එක Save වෙලා.")