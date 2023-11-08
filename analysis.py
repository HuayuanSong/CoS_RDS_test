import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to determine if the filename corresponds to Tiktok or Video
def get_category(filename):
    number_part = int(filename.split('_')[0])
    return 'Tiktok' if number_part % 2 != 0 else 'Video'

# Function to determine if the filename corresponds to Pre or Post exposure
def get_exposure(filename):
    # Standardize to title case to match dictionary keys
    return filename.split('_')[1].capitalize()

# Initialize dictionaries to hold the data
data = {
    'Tiktok': {'Pre': {'Forward': [], 'Backward': [], 'Combined': []},
               'Post': {'Forward': [], 'Backward': [], 'Combined': []}},
    'Video': {'Pre': {'Forward': [], 'Backward': [], 'Combined': []},
              'Post': {'Forward': [], 'Backward': [], 'Combined': []}}
}

# Directory where data files are stored
data_dir = 'data'

# Iterate over files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        category = get_category(filename)
        exposure = get_exposure(filename)
        # Read the contents of the file
        with open(os.path.join(data_dir, filename), 'r') as file:
            content = file.read()
            # Split the string by commas and convert each to an integer
            forward, backward, combined = [int(x) for x in content.split(',')]
            # Append the numbers to the appropriate lists
            data[category][exposure]['Forward'].append(forward)
            data[category][exposure]['Backward'].append(backward)
            data[category][exposure]['Combined'].append(combined)

# Create subplots for each score type
fig, axs = plt.subplots(3, 4, figsize=(20, 15))  # 3 rows for score types, 4 columns for [Tiktok Pre, Tiktok Post, Video Pre, Video Post]

# Titles for the columns
col_titles = ['Tiktok Pre', 'Tiktok Post', 'Video Pre', 'Video Post']

# Titles for the rows
row_titles = ['Forward', 'Backward', 'Combined']

# Set titles for columns
for ax, col in zip(axs[0], col_titles):
    ax.set_title(col)

# Set titles for rows
for ax, row in zip(axs[:, 0], row_titles):
    ax.set_ylabel(row, rotation=0, size='large')

# Plotting the data
for i, score_type in enumerate(row_titles):
    axs[i, 0].boxplot(data['Tiktok']['Pre'][score_type])
    axs[i, 1].boxplot(data['Tiktok']['Post'][score_type])
    axs[i, 2].boxplot(data['Video']['Pre'][score_type])
    axs[i, 3].boxplot(data['Video']['Post'][score_type])

# Add a title to the figure
fig.suptitle('Score Distribution Across Categories and Exposures')

# Adjust layout for readability
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Show the plots
plt.show()
