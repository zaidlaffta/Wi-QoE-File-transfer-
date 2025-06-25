#This code use QoE = A⋅log10(Throughput+1) – B ⋅ Retransmissions − C⋅RTT
#Complex QoE based on application with fine tune when it comes to A, B, C
import pandas as pd
import math

# Load the CSV
df = pd.read_csv("detailed_iperf3_results.csv")

# Print column names to ensure correctness
print("Columns:", df.columns)

# Define QoE calculation function
def calculate_qoe(row):
    A, B, C = 34, 0.5, 0.05
    throughput_bps = row.get("throughput_bps", 0)
    rtt_us = row.get("rtt_us", 0)
    retransmits = row.get("retransmits", 0)

    # Handle possible NaNs
    throughput_bps = throughput_bps if pd.notna(throughput_bps) else 0
    rtt_us = rtt_us if pd.notna(rtt_us) else 0
    retransmits = retransmits if pd.notna(retransmits) else 0

    throughput_mbps = throughput_bps / 1e6
    rtt_ms = rtt_us / 1000

    try:
        qoe = A * math.log10(throughput_mbps + 1) - B * retransmits - C * rtt_ms
    except ValueError:
        qoe = 0

    # Print for debugging (can be removed later)
    print(f"Throughput: {throughput_mbps:.2f} Mbps, RTT: {rtt_ms:.2f} ms, Retransmits: {retransmits}, QoE: {qoe:.2f}")
    return round(qoe, 2)

# Apply QoE calculation
df["QoE_score"] = df.apply(calculate_qoe, axis=1)

# Save to new CSV
df.to_csv("detailed_iperf3_with_qoe_complex_formula.csv", index=False)
