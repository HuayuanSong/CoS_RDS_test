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

# Initialize dictionaries to hold the pre and post data separately
pre_data = {'Tiktok': [], 'Video': []}
post_data = {'Tiktok': [], 'Video': []}

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
                # Append the numbers to the appropriate list
                if exposure == 'Pre':
                    pre_data[category].append({'Forward': forward, 'Backward': backward, 'Combined': combined})
                else:  # Exposure is 'Post'
                    post_data[category].append({'Forward': forward, 'Backward': backward, 'Combined': combined})

# Calculate the difference between Post and Pre scores
diff_data = []
for category in ['Tiktok', 'Video']:
    for pre, post in zip(pre_data[category], post_data[category]):
        diff_data.append({
            'Category': category,
            'Forward Difference': post['Forward'] - pre['Forward'],
            'Backward Difference': post['Backward'] - pre['Backward'],
            'Combined Difference': post['Combined'] - pre['Combined']
        })

# Convert the list of dictionaries to a DataFrame
df_diff = pd.DataFrame(diff_data)

# Set seaborn style
sns.set_style('whitegrid')

# Define a custom palette
palette = sns.color_palette("turbo", len(df_diff['Category'].unique()))

# Plot for each score difference type
for diff_type in ['Forward Difference', 'Backward Difference', 'Combined Difference']:
    plt.figure(figsize=(10, 6))

    # Create the violin plot
    ax = sns.violinplot(x='Category', y=diff_type, data=df_diff, palette=palette, inner=None, linewidth=0, saturation=0.4)

    # Overlay the box plot
    sns.boxplot(x='Category', y=diff_type, data=df_diff, palette=palette, width=0.3, boxprops={'zorder': 2}, ax=ax)

    # Set the title for the plot
    plt.title(f'{diff_type} by Category')

    # Show the plot
    plt.show()