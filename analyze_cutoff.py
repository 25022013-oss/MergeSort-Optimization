import os
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "results/cutoff_results.csv"
FIG_DIR = "results/figures"
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
df["n"] = df["n"].astype(int)
df["cutoff"] = df["cutoff"].astype(int)
df["avg_time_ms"] = df["avg_time_ms"].astype(float)

# 1. Tìm cutoff tốt nhất cho từng (type, n)
best_per_group = (
    df.sort_values("avg_time_ms")
    .groupby(["type", "n"], as_index=False)
    .first()
)
print("=== BEST CUTOFF BY (TYPE, N) ===")
print(best_per_group[["type", "n", "cutoff", "avg_time_ms"]].to_string(index=False))

# 2. So sánh với baseline cutoff = 0 (MergeSort thuần)
baseline = df[df["cutoff"] == 0][["type", "n", "avg_time_ms"]].rename(
    columns={"avg_time_ms": "baseline_ms"}
)
merged = best_per_group.merge(baseline, on=["type", "n"], how="left")
merged["speedup_pct"] = (
    (merged["baseline_ms"] - merged["avg_time_ms"]) / merged["baseline_ms"] * 100.0
)
print("\n=== SPEEDUP VS CUTOFF = 0 ===")
print(
    merged[["type", "n", "cutoff", "baseline_ms", "avg_time_ms", "speedup_pct"]].to_string(
        index=False
    )
)

# 3. Trung bình thời gian theo từng cutoff trên toàn bộ bộ test
mean_by_cutoff = (
    df.groupby("cutoff", as_index=False)["avg_time_ms"]
    .mean()
    .sort_values("avg_time_ms")
)
print("\n=== MEAN TIME ACROSS ALL TESTS BY CUTOFF ===")
print(mean_by_cutoff.to_string(index=False))

# 4. Vẽ biểu đồ: avg_time_ms theo cutoff cho từng loại dữ liệu (tách theo N)
types = df["type"].unique()
sizes = sorted(df["n"].unique())

for dtype in types:
    sub_type = df[df["type"] == dtype]
    plt.figure(figsize=(8, 5))
    for n_val in sizes:
        sub_n = sub_type[sub_type["n"] == n_val].sort_values("cutoff")
        plt.plot(sub_n["cutoff"], sub_n["avg_time_ms"], marker="o", label=f"N = {n_val:,}")
    plt.title(f"Execution Time vs. Cutoff ({dtype})")
    plt.xlabel("Cutoff Threshold")
    plt.ylabel("Average Time (ms)")
    plt.xticks(sorted(df["cutoff"].unique()))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    out_img = os.path.join(FIG_DIR, f"cutoff_{dtype}.png")
    plt.savefig(out_img, dpi=200)
    plt.close()

# 5. Vẽ biểu đồ tổng hợp: thời gian trung bình theo cutoff (chia theo type)
plt.figure(figsize=(8, 5))
for dtype in types:
    agg = (
        df[df["type"] == dtype]
        .groupby("cutoff", as_index=False)["avg_time_ms"]
        .mean()
        .sort_values("cutoff")
    )
    plt.plot(agg["cutoff"], agg["avg_time_ms"], marker="s", label=dtype)
plt.title("Mean Execution Time vs. Cutoff by Data Distribution")
plt.xlabel("Cutoff Threshold")
plt.ylabel("Mean Time (ms)")
plt.xticks(sorted(df["cutoff"].unique()))
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
summary_img = os.path.join(FIG_DIR, "cutoff_mean_by_type.png")
plt.savefig(summary_img, dpi=200)
plt.close()

print(f"\nSaved figures to {FIG_DIR}/")