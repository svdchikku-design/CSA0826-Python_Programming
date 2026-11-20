"""Venn diagrams of the three results (matplotlib patches)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def base(ax, title):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=10)
    ax.add_patch(Rectangle((0.2, 0.2), 9.6, 5.4, fill=False, lw=1.2))
    ax.text(0.4, 5.25, "all students (10)", fontsize=7)

def circles():
    return Circle((3.9, 2.9), 1.9, fill=False, lw=1.5, ec="#1f4e9a"), Circle((6.1, 2.9), 1.9, fill=False, lw=1.5, ec="#b34700")

def labels(ax):
    ax.text(2.6, 3.4, "AI only\n001, 007", ha="center", fontsize=7); ax.text(7.4, 3.4, "IoT only\n002, 010", ha="center", fontsize=7)
    ax.text(5.0, 3.1, "both\n004, 009", ha="center", fontsize=7); ax.text(5.0, 0.9, "neither: 003, 005, 006, 008", ha="center", fontsize=7)
    ax.text(2.4, 4.9, "AI", color="#1f4e9a", fontsize=9, weight="bold"); ax.text(7.6, 4.9, "IoT", color="#b34700", fontsize=9, weight="bold")

fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
SH = "#7fb069"
# 1. intersection A & B
ax = axes[0]; base(ax, "clash: AI ∩ IoT  (A & B)")
a, b = circles(); fill = Circle((3.9, 2.9), 1.9, fc=SH, ec="none"); ax.add_patch(fill); fill.set_clip_path(Circle((6.1, 2.9), 1.9, transform=ax.transData))
ax.add_patch(a); ax.add_patch(b); labels(ax)
# 2. symmetric difference A ^ B
ax = axes[1]; base(ax, "exactly one: AI △ IoT  (A ^ B)")
ax.add_patch(Circle((3.9, 2.9), 1.9, fc=SH, ec="none")); ax.add_patch(Circle((6.1, 2.9), 1.9, fc=SH, ec="none"))
ov = Circle((3.9, 2.9), 1.9, fc="white", ec="none"); ax.add_patch(ov); ov.set_clip_path(Circle((6.1, 2.9), 1.9, transform=ax.transData))
a, b = circles(); ax.add_patch(a); ax.add_patch(b); labels(ax)
# 3. neither U - (A | B)
ax = axes[2]; base(ax, "neither: U − (AI ∪ IoT)")
ax.add_patch(Rectangle((0.2, 0.2), 9.6, 5.4, fc=SH, ec="none"))
ax.add_patch(Circle((3.9, 2.9), 1.9, fc="white", ec="none")); ax.add_patch(Circle((6.1, 2.9), 1.9, fc="white", ec="none"))
a, b = circles(); ax.add_patch(a); ax.add_patch(b); labels(ax)
fig.tight_layout(); fig.savefig("venn.png", dpi=140)
print("saved venn.png")
