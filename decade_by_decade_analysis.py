import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

experiment = "Technology" # "Chemical", "Technology"

# Import data
data = pd.read_csv("/Users/tassjames/Desktop/Hydrogen_cleaned_vf.csv")

# Clean data & take care of N/A
data["Capacity"] = data["Capacity"].fillna(0)
data = data[data['Year'].notna()]
data = data[data['Status'].notna()]
data = data.loc[data["Year"] >= 2000]

# Sorted data with temporal ordering
sorted_data = data.sort_values("Year")
dic3={"Other Electrolysis":"Green","PEM":"Green","ALK":"Green","SOEC":"Green"}
sorted_data["Technology"].replace(dic3,inplace=True)

# Generate Unique continents and unique Technology
continent_unique = sorted_data["Continent"].unique()
continent_unique.sort()
technology_unique = sorted_data["Technology"].unique()
technology_unique.sort()

# Loop over both and slice continent/technology distribution
names_list = []
data_list = []
distribution_list = []
for i in range(len(continent_unique)):
    for j in range(len(technology_unique)):

        # Slice Continent and Technology
        df_slice = sorted_data.loc[(sorted_data["Continent"]==continent_unique[i]) &
                                   (sorted_data["Technology"]==technology_unique[j])]
        dist_element = continent_unique[i] + " " + technology_unique[j]
        names_list.append(dist_element)
        print(dist_element)

        # DF distributional use cases
        df_dist = df_slice[["Refining", "Ammonia", "Methanol", "Iron&Steel", "Other Ind", "Mobility",
                            "Power", "Grid inj.", "CHP", "Domestic heat", "Biofuels", "Synfuels",
                            "CH4 grid inj.", "CH4 mobility"]]
        df_dist_totals = df_dist.sum(axis=0).values

        # Append distributional components to list
        data_list.append(df_dist)
        distribution_list.append(df_dist_totals)

# Generate barplot
norm_distribution_list = []
for i in range(len(distribution_list)):
    norm_distribution = np.nan_to_num(distribution_list[i]/np.sum(distribution_list[i]))
    print("check", np.sum(norm_distribution))
    norm_distribution_list.append(norm_distribution)

# Convert to dataframes and merge
fig, ax=plt.subplots()
for j in range(len(norm_distribution_list)):
    ax.bar(names_list, norm_distribution_list[j])
    ax.set_xticklabels([''] + names_list, fontsize=6, rotation=90)
plt.legend(["Refining", "Ammonia", "Methanol", "Iron&Steel", "Other Ind", "Mobility",
                            "Power", "Grid inj.", "CHP", "Domestic heat", "Biofuels", "Synfuels",
                            "CH4 grid inj.", "CH4 mobility"])
plt.xlabel("Region / use")
plt.ylabel("Density")
plt.savefig("Stacked_bar_plot")
plt.show()

# Generate distance matrix and then cluster
dist_matrix_list = []
for i in range(len(distribution_list)):
    for j in range(len(distribution_list)):
        dist_i = np.nan_to_num(distribution_list[i]/np.nan_to_num(np.sum(distribution_list[i])))
        dist_j = np.nan_to_num(distribution_list[j]/np.nan_to_num(np.sum(distribution_list[j])))
        # Compute L^1 norm distance
        dist = np.sum(np.abs(dist_i - dist_j)) * 0.5
        dist_matrix_list.append(dist)

# Reshaped
dist_matrix_reshaped = np.reshape(dist_matrix_list, (len(distribution_list), len(distribution_list)))

# Plot figure
fig, ax = plt.subplots()
cax = ax.matshow(dist_matrix_reshaped)
fig.colorbar(cax)
ax.xaxis.set_major_locator(plt.MaxNLocator(17))
ax.yaxis.set_major_locator(plt.MaxNLocator(17))
ax.set_xticklabels(['']+names_list, fontsize=6, rotation=45)
ax.set_yticklabels(['']+names_list, rotation=0, fontsize=6)
plt.savefig("Distribution_distance_hydrogen")
plt.show()
