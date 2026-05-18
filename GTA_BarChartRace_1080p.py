import pandas as pd
import numpy as np
import bar_chart_race as bcr
import matplotlib.pyplot as plt

print("දත්ත සකස් කරමින් පවතී...")
print("Unit: Ten-Thousands (×10,000 copies)")

# --- Helper: smooth growth curve ---
def smooth_growth(start, end, n):
    t = np.linspace(-3, 3, n)
    s = 1 / (1 + np.exp(-t))
    return start + (end - start) * s

# --- Milestone data (Millions) ---
# Values are based on commonly reported publisher milestones.
milestones_millions = {
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
        ("2014-05-01", 33.0),
        ("2018-05-01", 95.0),
        ("2020-05-01", 130.0),
        ("2022-08-01", 170.0),
        ("2023-08-01", 185.0),
        ("2024-11-01", 205.0),
        ("2025-11-01", 215.0),
        ("2026-05-01", 215.0),
    ],
}

# --- Convert Millions -> Ten-Thousands (×10,000 copies) ---
# 1 Million copies = 100 x Ten-Thousands
milestones = {
    game: [(date, int(round(value_m * 100))) for date, value_m in points]
    for game, points in milestones_millions.items()
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
    steps_per_period=50,
    period_length=period_length,
    title="GTA Series Sales Evolution  |  Copies Sold (Ten-Thousands, ×10,000)",
    title_size=24,
    cmap=["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"],
    tick_label_size=14,
    bar_label_size=16,
    period_fmt="%Y %b",
    period_label={"x": 0.95, "y": 0.15, "ha": "right", "va": "center",
                  "size": 45, "weight": "bold", "color": "#1F2937"},
    bar_kwargs={"alpha": 0.95, "lw": 1, "ec": "#1F2937"}
)

print("✅ වැඩේ හරි! 'GTA_Evolution_1080p.mp4' නමින් Video එක Save වෙලා.")
