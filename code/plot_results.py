import json
import re
import numpy as np # type: ignore
import pandas as pd # type: ignore

import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

file_title = 'diff-config-grenoble'

# Load data from JSON files
with open('../data/'+file_title+'-results-mul-runs-split.json', 'r') as file:
    data = json.load(file)

#with open('../data/naive-approach-diff-results.json', 'r') as file:
    #naive_data = json.load(file)

with open('../data/'+file_title+'-merged-results-mul-runs-split.json', 'r') as file:
    merged_data = json.load(file)

# Prepare data for plotting
mse_data = []
merged_mse_data = []
naive_mse_data = []

#node_ids = ["95", "101", "102", "103", "104", "105", "106", "108", "109", "110"]
#node_ids = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
node_ids = ["m3-123", "m3-133", "m3-143", "m3-150", "m3-153", "m3-159", "m3-163", "m3-166"]


# Loop through each node_id and feature
for node_id, features in data.items():
    for feature, values in features.items():
        mse_list = values['0.8']['mse']
        #mse_list = values['mse']
        for mse in mse_list:
            mse_data.append({'Node ID': node_id, 'Feature': feature, 'MSE': mse})

"""
# Loop through each node_id and feature
for node_id, features in naive_data.items():
    for feature, values in features.items():
        mse_list = values['mse']
        for mse in mse_list:
            naive_mse_data.append({'Node ID': node_id, 'Feature': feature, 'MSE': mse})
"""

# Loop through each node_id and feature
for node_id, features in merged_data.items():
    for feature, values in features.items():
        mse_list = values['0.8']['mse']
        #mse_list = values['mse']
        for mse in mse_list:
            merged_mse_data.append({'Node ID': node_id, 'Feature': feature, 'MSE': mse})

"""
print(merged_data.items())
# Loop through each node_id and feature
for feature, values in merged_data.items():
    mse_list = values['mse']
    for mse in mse_list:
        for node_id in node_ids:
            merged_mse_data.append({'Node ID': node_id, 'Feature': feature, 'MSE': mse})
"""

print(merged_mse_data)

# Convert to DataFrame
mse_df = pd.DataFrame(mse_data)
merged_mse_df = pd.DataFrame(merged_mse_data)
#naive_mse_df = pd.DataFrame(naive_mse_data)

# Add a column to distinguish between the two datasets
mse_df['Model'] = 'Original'
merged_mse_df['Model'] = 'Merged'
#naive_mse_df['Model'] = 'Naive'

# Combine the two DataFrames
combined_df = pd.concat([mse_df, merged_mse_df])

# Create subplots for each feature
features = ['mean']
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, feature in enumerate(features):
    # Create boxplots with hue based on the 'Source' column
    #sns.boxplot(x='Node ID', y='MSE', hue='Model', data=combined_df[combined_df['Feature'] == feature], ax=axes[i])
    # Plot the point
    sns.barplot(x='Node ID', y='MSE', hue='Model', data=combined_df[combined_df['Feature'] == feature], ax=axes[i])
    axes[i].set_title(f'Distribution of MSE for {feature.capitalize()}')
    axes[i].grid(True)

# Adjust layout
plt.tight_layout()
#plt.savefig("../figures/results-models-diff-stbg.pdf", format="pdf", bbox_inches="tight")
plt.show()