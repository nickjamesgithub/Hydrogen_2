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

