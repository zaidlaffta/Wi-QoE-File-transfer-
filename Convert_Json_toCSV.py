import json
import pandas as pd

# Load raw JSON data
file_path = "result_filetransfer_tcp.json"
with open(file_path) as f:
    raw_data = f.read()

# Split multiple JSON objects
json_objects = []
buffer = ""
brace_count = 0

for char in raw_data:
    buffer += char
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0:
            try:
                json_objects.append(json.loads(buffer))
            except json.JSONDecodeError:
                pass
            buffer = ""

# Extract detailed fields
detailed_data = []
for entry in json_objects:
    try:
        start = entry.get("start", {})
        end = entry.get("end", {})
        stream = end.get("streams", [{}])[0].get("sender", {})

        detailed_data.append({
            "start_time": start.get("timestamp", {}).get("time"),
            "local_host": start.get("connected", [{}])[0].get("local_host"),
            "local_port": start.get("connected", [{}])[0].get("local_port"),
            "remote_host": start.get("connected", [{}])[0].get("remote_host"),
            "remote_port": start.get("connected", [{}])[0].get("remote_port"),
            "protocol": start.get("test_start", {}).get("protocol"),
            "duration": end.get("sum_received", {}).get("seconds"),
            "throughput_bps": end.get("sum_received", {}).get("bits_per_second"),
            "bytes_received": end.get("sum_received", {}).get("bytes"),
            "cpu_utilization_sender": end.get("cpu_utilization_percent", {}).get("host_total"),
            "cpu_utilization_receiver": end.get("cpu_utilization_percent", {}).get("remote_total"),
            "retransmits": stream.get("retransmits"),
            "rtt_us": stream.get("rtt"),
            "rtt_var_us": stream.get("rttvar"),
            "max_rtt_us": stream.get("max_rtt"),
            "min_rtt_us": stream.get("min_rtt"),
            "lost_packets": stream.get("lost_packets"),
            "packets": stream.get("packets")
        })
    except Exception:
        continue

# Save to CSV
print("saving the data to CSV file:")
df = pd.DataFrame(detailed_data)
df.to_csv("detailed_iperf3_results.csv", index=False)
