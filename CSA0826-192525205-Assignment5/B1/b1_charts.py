"""B1.4: the four charts designed in A3.1, drawn from the SQLite database. One hue, thin marks, labelled axes."""
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, MUTED, BLUE, GRID = "#222222", "#666666", "#2E5597", "#DDDDDD"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})
con = sqlite3.connect("air_quality.db")
df = pd.read_sql("SELECT s.name AS station, r.date, r.hour, r.pm25, r.temp_c FROM readings r JOIN stations s USING (station_id)", con)
df["date"] = pd.to_datetime(df["date"])

# 1. line chart - trend of PM2.5 over the month (city daily mean)
daily = df.groupby("date")["pm25"].mean()
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.plot(daily.index, daily.values, color=BLUE, linewidth=2)
ax.set_title("City-wide daily mean PM2.5, October 2026"); ax.set_xlabel("Date"); ax.set_ylabel("PM2.5 (µg/m³)")
fig.autofmt_xdate(); fig.tight_layout(); fig.savefig("chart1_trend_line.png", dpi=150); plt.close(fig)
dd = daily.index.day.to_numpy(); x = dd - dd.mean(); slope = ((x * (daily.values - daily.values.mean())).sum() / (x ** 2).sum())
print(f"chart 1: daily mean from {daily.min():.1f} (on {daily.idxmin().date()}) to {daily.max():.1f} (on {daily.idxmax().date()}); linear trend {slope:+.2f} µg/m³ per day, "
      f"month mean {daily.mean():.1f}")

# 2. box plot - comparison of stations (spread, not only the mean)
order = df.groupby("station")["pm25"].median().sort_values(ascending=False).index
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.boxplot([df.loc[df.station == s, "pm25"].dropna() for s in order], orientation="horizontal", tick_labels=list(order), patch_artist=True, showfliers=True,
           boxprops=dict(facecolor="#C9D6EE", edgecolor=BLUE), medianprops=dict(color=BLUE, linewidth=2), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
           flierprops=dict(marker="o", markersize=2.5, markeredgecolor=MUTED, alpha=.6))
ax.invert_yaxis(); ax.set_title("PM2.5 by station, October 2026 (hourly readings)"); ax.set_xlabel("PM2.5 (µg/m³)"); ax.set_ylabel("Station")
fig.tight_layout(); fig.savefig("chart2_stations_box.png", dpi=150); plt.close(fig)
med = df.groupby("station")["pm25"].median().sort_values(ascending=False)
print(f"chart 2: highest median {med.index[0]} {med.iloc[0]:.1f}, lowest {med.index[-1]} {med.iloc[-1]:.1f}; ratio {med.iloc[0]/med.iloc[-1]:.1f}x; "
      f"stations with median above 60: {', '.join(med[med > 60].index)}")

# 3. scatter - temperature versus PM2.5 (hourly, one station so the baseline is comparable)
one = df[df.station == "Adyar"].dropna(subset=["pm25", "temp_c"])
corr_all = df.dropna(subset=["pm25", "temp_c"])[["pm25", "temp_c"]].corr().iloc[0, 1]
fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.scatter(one["temp_c"], one["pm25"], s=9, color=BLUE, alpha=.45, linewidths=0)
ax.set_title("Temperature and PM2.5 at Adyar (hourly)"); ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("PM2.5 (µg/m³)")
fig.tight_layout(); fig.savefig("chart3_temp_scatter.png", dpi=150); plt.close(fig)
print(f"chart 3: Adyar correlation r = {one['pm25'].corr(one['temp_c']):.2f} (n={len(one)}); all stations pooled r = {corr_all:.2f}")

# 4. bar chart - hours with the worst air (city mean per hour)
byh = df.groupby("hour")["pm25"].mean()
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(byh.index, byh.values, color=BLUE, width=0.7)
ax.set_xticks(range(0, 24)); ax.set_title("Mean PM2.5 by hour of day, all stations"); ax.set_xlabel("Hour of day (0-23)"); ax.set_ylabel("PM2.5 (µg/m³)")
fig.tight_layout(); fig.savefig("chart4_hours_bar.png", dpi=150); plt.close(fig)
top3 = byh.sort_values(ascending=False).head(3)
print(f"chart 4: worst hours {', '.join(f'{h:02d}:00 ({v:.1f})' for h, v in top3.items())}; best hour {byh.idxmin():02d}:00 ({byh.min():.1f}); evening peak / afternoon low = {byh.max()/byh.min():.2f}")
