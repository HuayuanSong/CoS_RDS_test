import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to determine if the filename corresponds to Tiktok or Video
def get_category(filename):
    number_part = int(filename.split('_')[0])
    return 'Tiktok' if number_part % 2 != 0 else 'Video'

# Function to determine if the filename corresponds to Pre or Post exposure
def get_exposure(filename):
    return filename.split('_')[1].capitalize()

# Initialize a DataFrame to hold the data
data = []

# Directory where data files are stored
data_dir = 'data'

# Iterate over files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        category = get_category(filename)
        exposure = get_exposure(filename)
        # Read the contents of the file
        with open(os.path.join(data_dir, filename), 'r') as file:
            content = file.read().strip()
            if content:  # Check if content is not empty
                # Split the string by commas and convert each to an integer
                forward, backward, combined = [int(x) for x in content.split(',')]
                # Append the numbers to the data list
                data.append({'Category': category, 'Exposure': exposure,
                             'Forward': forward, 'Backward': backward, 'Combined': combined})

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Set seaborn style
sns.set_style('whitegrid')

# Define a custom palette
palette = sns.color_palette("turbo", len(df['Category'].unique()))

# Plot for each score type
for score_type in ['Forward', 'Backward', 'Combined']:
    plt.figure(figsize=(10, 6))

    # Create the violin plot
    ax = sns.violinplot(x='Category', y=score_type, hue='Exposure', data=df, palette=palette,
                        inner=None, linewidth=0, saturation=0.4)

    # Overlay the box plot
    sns.boxplot(x='Category', y=score_type, hue='Exposure', data=df, palette=palette, width=0.3,
                boxprops={'zorder': 2}, ax=ax)

    # Set the title for the plot
    plt.title(f'{score_type} Score by Category and Exposure')

    # Show the plot
    plt.show()
