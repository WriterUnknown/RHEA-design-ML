import pandas as pd
import numpy as np
from mendeleev import element

# Import the alloy composition data
df = pd.read_csv('alloy_comp_data.csv')

# List of elements considered in the alloys
ele_list = ['Al', 'Cr', 'Fe', 'Hf', 'Mo', 'Nb', 'Ni', 'Sc', 'Si', 'Ta', 'Ti', 'V', 'W', 'Zr', 'Co', 'Cu']

# List of properties to calculate
properties = ['atomic_weight', 'atomic_volume', 'atomic_number', 'electron_affinity']

# Function to retrieve property values, handling electronegativities separately
def get_property_value(ele, property_name):
    if property_name == 'en_pauling':
        return element(ele).electronegativity('pauling')
    elif property_name == 'en_mulliken':
        return element(ele).electronegativity('mulliken')
    else:
        return getattr(element(ele), property_name)

# Function to calculate average properties of an alloy
def calculate_avg_property(property_name):
    alloy_data = df.iloc[:, 1:].values  # Exclude the alloy name from calculations
    element_objs = np.array([get_property_value(ele, property_name) for ele in ele_list])
    property_values = element_objs * alloy_data
    return np.sum(property_values, axis=1) / np.sum(alloy_data, axis=1)

# Calculating average properties for each alloy
avg_properties = {}
for property_name in properties:
    avg_properties[f'avg_{property_name}'] = calculate_avg_property(property_name)

# Calculating average Mulliken and Pauling electronegativities
avg_properties['avg_en_mulliken'] = calculate_avg_property('en_mulliken')
avg_properties['avg_en_pauling'] = calculate_avg_property('en_pauling')

# Function to calculate the minimum and maximum values based on the element with the minimum and maximum composition in each alloy
def calculate_extreme_property(property_name, extreme_func):
    extreme_values = []
    alloy_data = df.iloc[:, 1:].values  # Exclude the alloy name from calculations
    for row in alloy_data:
        extreme_index = extreme_func(row)  # Get the index of the element with the extreme composition
        extreme_element = ele_list[extreme_index]  # Get the element symbol
        extreme_value = get_property_value(extreme_element, property_name)  # Get the property value of the element
        extreme_values.append(extreme_value)
    return extreme_values

# Adding the minimum and maximum properties to the avg_properties dictionary
properties_to_extreme = ['atomic_number', 'atomic_weight', 'atomic_volume', 'electron_affinity', 'en_mulliken', 'en_pauling']
for property_name in properties_to_extreme:
    avg_properties[f'min_{property_name}'] = calculate_extreme_property(property_name, np.argmin)
    avg_properties[f'max_{property_name}'] = calculate_extreme_property(property_name, np.argmax)

# Creating DataFrame for average properties
arr = pd.DataFrame(avg_properties)
arr.insert(0, 'Alloy', df.iloc[:, 0])  # Inserting alloy names as the first column

# Rename columns to have average, min, and max properties side by side for each property
ordered_columns = ['Alloy']
for property_name in properties:
    avg_name = f'avg_{property_name}'
    min_name = f'min_{property_name}'
    max_name = f'max_{property_name}'
    ordered_columns.extend([avg_name, min_name, max_name])
ordered_columns.extend(['avg_en_mulliken', 'min_en_mulliken', 'max_en_mulliken', 'avg_en_pauling', 'min_en_pauling', 'max_en_pauling'])

arr = arr[ordered_columns]

# Ensure all arrays have the same length
assert all(len(arr[col]) == len(arr['Alloy']) for col in arr.columns), "All columns must be the same length"

# Save the DataFrame to a CSV file
arr.to_csv('alloy_prop_data.csv', index=False)
