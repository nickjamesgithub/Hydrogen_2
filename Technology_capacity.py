import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Utilities import dendrogram_plot_test

# Import data
data = pd.read_csv("/Users/tassjames/Desktop/Hydrogen_cleaned_vf.csv")

# Clean data & take care of N/A
data["Capacity"] = data["Capacity"].fillna(0)
data = data[data['Year'].notna()]
data = data[data['Status'].notna()]
data = data.loc[data["Year"] >= 2000]

# Sorted data with temporal ordering
sorted_data = data.sort_values("Year")

# Features
features = ["Refining", "Ammonia", "Methanol", "Iron&Steel", "Other Ind",
            "Mobility", "Power", "Grid inj.", "CHP", "Domestic heat", "Biofuels", "Synfuels",
            "CH4 grid inj.", "CH4 mobility"]

# Loop over the features
feature_list = []
for i in range(len(features)):

    # Slice feature
    data_slice = sorted_data[[features[i], "Year"]]
    year_slice = data_slice["Year"].values
    feature_slice = data_slice[features[i]].values
    feature_slice_cumsum = np.cumsum(feature_slice)
    total = np.sum(feature_slice)

    # Compute CDF for each feature
    feature_slice_normalized = (feature_slice_cumsum/total)
    feature_list.append(feature_slice_normalized)

    # Plot CDF for each feature
    plt.plot(year_slice, feature_slice_normalized)
    plt.title(features[i])
    plt.xlabel("Time")
    plt.ylabel("Density")
    plt.savefig("Normalized_CDF_"+features[i])
    plt.show()

# Loop over features, normalize trajectories and compute distances
distance_list = []
for j in range(len(feature_list)):
    for k in range(len(feature_list)):
        # Slice CDFs
        trajectory_j = feature_list[j]
        trajectory_k = feature_list[k]
        # Compute distance between two CDFs
        dist = np.sum(np.abs(trajectory_j-trajectory_k))
        distance_list.append(dist)

# Reshape
distance_array = np.reshape(distance_list, (len(feature_list),len(feature_list)))

# Plot distance between trajectories
plt.matshow(distance_array)
plt.savefig("Distance_matrix_CDFs")
plt.show()

# Plot dendrogram
dendrogram_plot_test(distance_array, "_L1_", "_CDF_", features)

# Unique technology features
technology_features = sorted_data["Technology"].unique()

# Loop over the features
capacity_list = []
for i in range(len(technology_features)):

    # Slice feature
    data_slice = sorted_data.loc[sorted_data["Technology"]==technology_features[i]][["Year", "Capacity"]]
    year_slice = data_slice["Year"].values
    capacity_slice = data_slice["Capacity"].values
    capacity_cumsum = np.cumsum(capacity_slice)
    total = np.sum(capacity_slice)

    # Compute CDF for each feature
    capacity_slice_normalized = (capacity_cumsum/total)
    capacity_list.append(capacity_slice_normalized)

    # Plot CDF for each feature
    plt.plot(year_slice, capacity_slice_normalized)
    plt.title(technology_features[i])
    plt.xlabel("Date")
    plt.ylabel("Capacity")
    plt.savefig("Capacity_"+technology_features[i])
    plt.show()

