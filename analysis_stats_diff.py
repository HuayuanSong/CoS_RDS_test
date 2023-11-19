import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

def get_category(filename):
    """Determines the category based on the filename."""
    number_part = int(filename.split('_')[0])
    return 'Tiktok' if number_part % 2 != 0 else 'Video'

def get_exposure(filename):
    """Determines the exposure type based on the filename."""
    return filename.split('_')[1].capitalize()

# Initialize dictionaries to hold the pre and post data separately
pre_data = {'Tiktok': [], 'Video': []}
post_data = {'Tiktok': [], 'Video': []}

data_dir = 'data'

# Reading data files and categorizing them
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        category = get_category(filename)
        exposure = get_exposure(filename)
        with open(os.path.join(data_dir, filename), 'r') as file:
            content = file.read().strip()
            if content:
                forward, backward, combined = [int(x) for x in content.split(',')]
                if exposure == 'Pre':
                    pre_data[category].append({'Forward': forward, 'Backward': backward, 'Combined': combined})
                else:
                    post_data[category].append({'Forward': forward, 'Backward': backward, 'Combined': combined})

# Calculating differences between Post and Pre scores
diff_data = []
for category in ['Tiktok', 'Video']:
    for pre, post in zip(pre_data[category], post_data[category]):
        diff_data.append({
            'Category': category,
            'Forward Difference': post['Forward'] - pre['Forward'],
            'Backward Difference': post['Backward'] - pre['Backward'],
            'Combined Difference': post['Combined'] - pre['Combined']
        })

df_diff = pd.DataFrame(diff_data)

sns.set_style('whitegrid')
palette = sns.color_palette("turbo", len(df_diff['Category'].unique()))

def perform_mannwhitneyu(df, category1, category2, score_type):
    """Performs Mann-Whitney U test and returns p-value."""
    group1 = df[df['Category'] == category1][score_type]
    group2 = df[df['Category'] == category2][score_type]
    stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
    return p_value

def annotate_p_value(ax, p_value, x1, x2, y, h):
    """Annotates the plot with the p-value."""
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='black')
    ax.text((x1+x2)*0.5, y+h, f'p={p_value:.3f}', ha='center', va='bottom', color='black')

# Plotting the violin plots with annotated p-values
for diff_type in ['Forward Difference', 'Backward Difference', 'Combined Difference']:
    plt.figure(figsize=(10, 6))
    ax = sns.violinplot(x='Category', y=diff_type, data=df_diff, palette=palette, inner=None, linewidth=0, saturation=0.4)
    sns.stripplot(x='Category', y=diff_type, data=df_diff, color='black', size=4, jitter=True, alpha=0.7)
    sns.boxplot(x='Category', y=diff_type, data=df_diff, palette=palette, width=0.3, boxprops={'zorder': 2}, ax=ax)
    plt.title(f'{diff_type} by Category')

    p_value = perform_mannwhitneyu(df_diff, 'Tiktok', 'Video', diff_type)
    annotate_p_value(ax, p_value, 0, 1, df_diff[diff_type].max(), 0.05 * df_diff[diff_type].max())

    # Annotating the number of test subjects
    counts = df_diff['Category'].value_counts()
    for i, category in enumerate(df_diff['Category'].unique()):
        count_text = f'n = {int(counts[category])} test subjects'
        ax.text(i, ax.get_ylim()[-1], count_text, ha='center', va='top', color='black', fontweight='semibold')

    plt.show()
