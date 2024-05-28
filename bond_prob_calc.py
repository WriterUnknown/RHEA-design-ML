import pandas as pd

# Importing alloy_comp_data.csv file containing compositional data of all the alloys in the dataset
df = pd.read_csv('alloy_comp_data.csv')  # Reading the CSV file into a DataFrame

# Creating constituent element list
ele_list = ['Al', 'Cr', 'Fe', 'Hf', 'Mo', 'Nb', 'Ni', 'Sc', 'Si', 'Ta', 'Ti', 'V', 'W', 'Zr', 'Co', 'Cu']

# Making a header for the new CSV file
header = ['Alloy']

for x in range(0, 16):
    for y in range(x, 16):
        bond = ele_list[x] + '-' + ele_list[y]
        header.append(bond)

length_header = len(header)

# Number of rows (86 alloys) and columns (length of header)
rows, cols = (86, length_header)
arr = [[0 for _ in range(cols)] for _ in range(rows)]  # Creates a blank 2D list

# Calculating bond probability for each alloy
for row_num in range(0, 86):
    arr[row_num][0] = df.iloc[row_num, 0]  # Set the alloy name
    index = 1  # Initialize index for bonds in arr

    # Calculating den_sum (This will be the same throughout the whole row in the final CSV file)
    den_sum = 0
    
    for i in range(1, 17):
        for j in range(i, 17):
            p = (df.iloc[row_num, i]) * (df.iloc[row_num, j])
            den_sum += p
    
    for a in range(1, 17):
        for b in range(a, 17):
            prod_ab = (df.iloc[row_num, a]) * (df.iloc[row_num, b])
            prob_ab = prod_ab / den_sum
            arr[row_num][index] = prob_ab
            index += 1

# Convert the 2D list to a DataFrame and save it to a CSV file
arr_df = pd.DataFrame(arr, columns=header)
arr_df.to_csv('bond_prob_alloy.csv', index=False)
