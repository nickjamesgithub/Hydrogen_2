import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance

# Import data
data = pd.read_csv("/Users/tassjames/Desktop/Hydrogen_cleaned_vf.csv")

# Clean data & take care of N/A
data["Capacity"] = data["Capacity"].fillna(0)
data = data[data['Year'].notna()]
data = data[data['Status'].notna()]
data = data.loc[data["Year"] >= 2000]

# Sorted data with temporal ordering
sorted_data = data.sort_values("Year")

# Sort Types of Technology (Green, etc.)
dic3={"Other Electrolysis":"Green","PEM":"Green","ALK":"Green","SOEC":"Green"}
sorted_data["Technology"].replace(dic3,inplace=True)

# Generate Unique continents and unique Technology
continent_unique = sorted_data["Continent"].unique()
continent_unique.sort()
technology_unique = sorted_data["Technology"].unique()
technology_unique.sort()

# Slice Technology that is just green
green_slice = sorted_data.loc[sorted_data["Technology"]=="Green"]
fossil_slice = sorted_data.loc[sorted_data["Technology"]=="Fossil"]

# Loop over Green plants
green_year_unique = green_slice["Year"].unique()
fossil_year_unique = fossil_slice["Year"].unique()

# Green Capacity values
green_capacity_list = []
for i in range(len(green_year_unique)):
    green_capacity_vals = green_slice.loc[green_slice["Year"]==green_year_unique[i]]["Capacity"].values
    green_capacity_list.append(green_capacity_vals)

# Fossil Capacity values
fossil_capacity_list = []
for i in range(len(fossil_year_unique)):
    fossil_capacity_vals = fossil_slice.loc[fossil_slice["Year"]==fossil_year_unique[i]]["Capacity"].values
    fossil_capacity_list.append(fossil_capacity_vals)

# Compute distance between distributions and learn linear operator
alpha_grid = np.linspace(-10,500,100) # 100
beta_grid = np.linspace(-5,50,100) # 100

# Store Green optimal values for alpha & beta
green_optimal_alpha_list = []
green_optimal_beta_list = []
green_grid_length_list = []

for j in range(0,len(green_capacity_list)-1):
    # Print Current iteration t
    print("T_current", green_year_unique[j])
    # Print Capacity at t and t+1
    green_capacity_t = green_capacity_list[j]
    green_capacity_t1 = green_capacity_list[j+1]

    # Store values in list
    distance_list = []
    alpha_list = []
    beta_list = []

    for a in range(len(alpha_grid)):
        for b in range(len(beta_grid)):
            # Compute linear transformation
            alpha_ = alpha_grid[a]
            beta_ = beta_grid[b]
            dist_transformed_capacity = alpha_ + beta_ * green_capacity_t

            # Compute wasserstein distance
            w_dist = wasserstein_distance(dist_transformed_capacity, green_capacity_t1)

            # Append to lists
            distance_list.append(w_dist)
            alpha_list.append(alpha_)
            beta_list.append(beta_)

            print("Capacity iteration", green_year_unique[j])
            print("Beta iteration", b)
            print("Alpha iteration", a)

    # Compute the minimal distance
    min_dist_star = np.argmin(distance_list)
    alpha_opt = alpha_list[min_dist_star]
    beta_opt = beta_list[min_dist_star]

    # Append to optimal list
    green_optimal_alpha_list.append(alpha_opt)
    green_optimal_beta_list.append(beta_opt)

# Convert alpha and beta (operator parameters) to dataframes and concatentate
green_optimal_alpha_df = pd.DataFrame(green_optimal_alpha_list)
green_optimal_beta_df = pd.DataFrame(green_optimal_beta_list)
concat = pd.concat([green_optimal_alpha_df, green_optimal_beta_df], axis=1)
concat.to_csv("/Users/tassjames/Desktop/green_linear_operator_parameters.csv")

# Store Fossil optimal values for alpha & beta
fossil_optimal_alpha_list = []
fossil_optimal_beta_list = []
fossil_grid_length_list = []

for j in range(0,len(fossil_capacity_list)-1):
    # Print Current iteration t
    print("T_current", fossil_year_unique[j])
    # Print Capacity at t and t+1
    fossil_capacity_t = fossil_capacity_list[j]
    fossil_capacity_t1 = fossil_capacity_list[j+1]

    # Store values in list
    distance_list = []
    alpha_list = []
    beta_list = []

    for a in range(len(alpha_grid)):
        for b in range(len(beta_grid)):
            # Compute linear transformation
            alpha_ = alpha_grid[a]
            beta_ = beta_grid[b]
            dist_transformed_capacity = alpha_ + beta_ * fossil_capacity_t

            # Compute wasserstein distance
            w_dist = wasserstein_distance(dist_transformed_capacity, fossil_capacity_t1)

            # Append to lists
            distance_list.append(w_dist)
            alpha_list.append(alpha_)
            beta_list.append(beta_)

            print("Capacity iteration", fossil_year_unique[j])
            print("Beta iteration", b)
            print("Alpha iteration", a)

    # Compute the minimal distance
    min_dist_star = np.argmin(distance_list)
    alpha_opt = alpha_list[min_dist_star]
    beta_opt = beta_list[min_dist_star]

    # Append to optimal list
    fossil_optimal_alpha_list.append(alpha_opt)
    fossil_optimal_beta_list.append(beta_opt)

# Convert alpha and beta (operator parameters) to dataframes and concatentate
fossil_optimal_alpha_df = pd.DataFrame(fossil_optimal_alpha_list)
fossil_optimal_beta_df = pd.DataFrame(fossil_optimal_beta_list)
concat = pd.concat([fossil_optimal_alpha_df, fossil_optimal_beta_df], axis=1)
concat.to_csv("/Users/tassjames/Desktop/fossil_linear_operator_parameters.csv")