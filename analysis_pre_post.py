import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_category(filename):
    """
    Determines the category (Tiktok or Video) based on the filename.

    Args:
    - filename (str): The name of the file.

    Returns:
    - str: 'Tiktok' for odd numbers, 'Video' for even numbers.
    """
    number_part = int(filename.split('_')[0])
    return 'Tiktok' if number_part % 2 != 0 else 'Video'

def get_exposure(filename):
    """
    Determines the exposure type (Pre or Post) based on the filename.

    Args:
    - filename (str): The name of the file.

    Returns:
    - str: 'Pre' or 'Post' based on the filename.
    """
    return filename.split('_')[1].capitalize()

# Initialize a list to store data and a dictionary to track unique subjects
data = []
subject_files = {'Tiktok': set(), 'Video': set()}

data_dir = 'data'
# Iterate over each file in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        category = get_category(filename)
        exposure = get_exposure(filename)
        subject_id = filename.split('_')[0]
        subject_files[category].add(subject_id)

        with open(os.path.join(data_dir, filename), 'r') as file:
            content = file.read().strip()
            if content:
                forward, backward, combined = [int(x) for x in content.split(',')]
                data.append({'Category': category, 'Exposure': exposure,
                             'Forward': forward, 'Backward': backward, 'Combined': combined})

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Set the style for seaborn plots
sns.set_style('whitegrid')
palette = sns.color_palette("turbo", len(df['Category'].unique()))

# Plot the data for each score type
for score_type in ['Forward', 'Backward', 'Combined']:
    plt.figure(figsize=(10, 6))
    ax = sns.violinplot(x='Category', y=score_type, hue='Exposure', data=df, palette=palette,
                        inner=None, linewidth=0, saturation=0.4)

    # Adding individual data points
    sns.stripplot(x='Category', y=score_type, hue='Exposure', data=df, color='black',
                  dodge=True, jitter=True, alpha=0.7, ax=ax)

    # Adding box plot overlay
    sns.boxplot(x='Category', y=score_type, hue='Exposure', data=df, palette=palette, width=0.3,
                boxprops={'zorder': 2}, ax=ax)

    # Set plot title
    ax.set_title(f'{score_type} Score by Category and Exposure')

    # Calculate and add counts of test subjects below the x-axis
    for i, category in enumerate(df['Category'].unique()):
        count = len(subject_files[category])
        ax.text(i, ax.get_ylim()[-2], f'n = {count} test subjects', horizontalalignment='center', size='medium', color='black', weight='semibold')

    # Adjust legend to show only Exposure types
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2], title='Exposure', bbox_to_anchor=(1, 1), loc='upper left')

    # Display the plot
    plt.show()
