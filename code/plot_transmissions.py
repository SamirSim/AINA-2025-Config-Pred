import re
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from collections import defaultdict # type: ignore
import time
import json
import numpy as np # type: ignore

# Initialize a dictionary to store transmission counts for each node
transmission_counts = {}
file_title = 'same-config'
filename = '../data/'+file_title+'.txt'

# Read the logs from the file
with open(filename, 'r') as file:
    logs = file.read()

# Regular expressions to capture the necessary fields
config_re = r"m3-(\d+);The configuration has been changed to: CSMA_MIN_BE=(\d+), CSMA_MAX_BE=(\d+), CSMA_MAX_BACKOFF=(\d+), FRAME_RETRIES=(\d+)"
trans_count_re = r"m3-(\d+);csma: rexmit ok (\d+)"

# Patterns to capture timestamp, node ID, and the data for transmissions and config changes
transmission_pattern = r'(\d+\.\d+);m3-(\d+);csma: rexmit ok (\d+)'
config_pattern = r'(\d+\.\d+);m3-(\d+);The configuration has been changed to: (.*)'

# Dictionary to store transmission counts per node and configuration
node_transmission_counts = defaultdict(lambda: defaultdict(list))
transmission_timeline = defaultdict(list)

# Current configuration per node
current_config = {}

# Parsing the log data
for line in logs.splitlines():
    # Check for configuration change
    config_match = re.search(config_re, line)
    if config_match:
        node = config_match.group(1)
        csma_min_be = int(config_match.group(2))
        csma_max_be = int(config_match.group(3))
        csma_max_backoff = int(config_match.group(4))
        frame_retries = int(config_match.group(5))
        
        # Store the current configuration for the node
        current_config[node] = (csma_min_be, csma_max_be, csma_max_backoff, frame_retries)
        
        # Record the time of configuration change for the node
        timestamp = float(line.split(";")[0])
        transmission_timeline[node].append((timestamp, current_config[node]))

    # Check for transmission count
    trans_match = re.search(trans_count_re, line)
    if trans_match:
        node = trans_match.group(1)
        transmission_count = int(trans_match.group(2))
        
        # Get the current configuration for the node
        if node in current_config:
            config = current_config[node]
            # Append the transmission count to the respective configuration's list
            node_transmission_counts[node][config].append(transmission_count)
            
            # Record the timestamp and transmission count for plotting
            timestamp = float(line.split(";")[0])
            transmission_timeline[node].append((timestamp, transmission_count))


# Create a figure
num_nodes = len(("95", "101", "102", "103", "104", "105", "106", "108", "109"))
plt.figure(figsize=(10, 2 * num_nodes))  # Adjust the figure height based on the number of nodes

for i, node_id in enumerate(("95", "101", "102", "103", "104", "105", "106", "108", "109")):
    # Extract timestamps and transmission counts for the node
    timestamps = []
    transmissions = []
    config_changes = []
    
    for entry in transmission_timeline[node_id]:
        timestamp, value = entry
        timestamps.append(timestamp)
        if isinstance(value, tuple):  # Configuration change
            config_changes.append((timestamp, value))
        else:
            transmissions.append(value)
    
    # Generate for each configuration the succession of transmission counts
    config_transmissions = defaultdict(list)
    for timestamp, value in transmission_timeline[node_id]:
        if isinstance(value, tuple):
            config = value
        else:
            config_transmissions[config].append(value)

    # Create a subplot for the current node
    plt.subplot(num_nodes, 1, i + 1)  # (rows, cols, panel number)
    
    # Plot transmissions over time for the current node
    plt.plot(timestamps[:len(transmissions)], transmissions, label=f"Node {node_id}", marker='o')
    
    # Plot configuration changes as vertical lines
    for config_change in config_changes:
        ts, config = config_change
        plt.axvline(x=ts, color='r', linestyle='--', alpha=0.5)  # Adjust alpha for visibility
    
    # Customize each subplot
    plt.xlabel('Time (s)')
    plt.ylabel('Transmission Count')
    plt.title(f'Evolution of Transmissions for Node {node_id}')
    plt.grid(True)

# Adjust layout for better spacing
plt.tight_layout()
plt.show()