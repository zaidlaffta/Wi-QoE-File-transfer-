#This code uses throuput/max throuhgput
#it will find basic QoE
import pandas as pd

# Load the CSV
df = pd.read_csv("detailed_iperf3_results.csv")

# Max throughput from the dataset
max_throughput = df["throughput_bps"].max()

# Avoid division by zero
if max_throughput == 0:
    df["QoE_score"] = 0
else:
    df["QoE_score"] = df["throughput_bps"] / max_throughput

# Optionally scale QoE from 0 to 100
df["QoE_score"] = (df["QoE_score"] * 100).round(2)

# Save result to a new CSV
df.to_csv("detailed_iperf3_with_qoe_basic_formula.csv", index=False)
