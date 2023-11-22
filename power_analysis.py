import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import TTestIndPower
from scipy.stats import norm
import math
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="statsmodels")

def calculate_cohens_d(group1, group2):
    # Calculates mean differences for each group
    mean_diff_group1 = np.mean(group1)
    mean_diff_group2 = np.mean(group2)

    # Calculates pooled standard deviation
    pooled_sd = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)

    # Calculates Cohen's d
    cohen_d = (mean_diff_group1 - mean_diff_group2) / pooled_sd

    return cohen_d

def calculate_effect_size(sample_size, alpha, beta):
    # Calculate critical values
    z_alpha_over_2 = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(1 - beta)

    # Calculate effect size
    effect_size = (2 * (z_alpha_over_2 + z_beta)) / (sample_size**0.5)

    return effect_size

def calculate_sample_size_ttest(effect_size, alpha, power):
    analysis = TTestIndPower()
    sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, ratio=1.0, alternative='two-sided')
    return round(sample_size)

def calculate_sample_size_manual(alpha, beta, effect_size):
    # Calculates critical values
    z_alpha_over_2 = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(1 - beta)

    # Calculates required sample size
    #sample_size = (2 * (z_alpha_over_2 + z_beta)**2 * sigma**2) / effect_size**2
    sample_size = (2 * (z_alpha_over_2 + z_beta)**2) / effect_size**2
    # we can't have 0.1 particiåant so we want the next bigger number

    return math.ceil(sample_size), z_alpha_over_2, z_beta

# CSV file into a DataFrame
df_diff = pd.read_csv('df_diff.csv')

# Assuming df_diff is the DataFrame with the 'Combined Difference' and 'Category' columns
video_group = np.array(df_diff.loc[df_diff['Category'] == 'Video', 'Combined Difference'])
tiktok_group = np.array(df_diff.loc[df_diff['Category'] == 'TikTok', 'Combined Difference'])

# Calculates standard deviations for pilot data
sigma_video = np.std(video_group, ddof=1)
sigma_tiktok = np.std(tiktok_group, ddof=1)

# Calculates pooled standard deviation
pooled_sd = np.sqrt((sigma_video**2 + sigma_tiktok**2) / 2)

# Displays the arrays
print("Video Group:", video_group)
print("TikTok Group:", tiktok_group)

# Calculates Cohen's d
effect_size = calculate_cohens_d(video_group, tiktok_group)

# Sets alpha and desired power
sample_size_lit = 106
simple_size_our_data = 25
alpha = 0.05
power = 0.8
beta = 0.2

# Calculates required sample size
sample_size_builtin = calculate_sample_size_ttest(effect_size, alpha, power)


# Calculate required sample size
sample_size_manual, z_alpha_over_2, z_beta  = calculate_sample_size_manual(alpha, beta, effect_size)

# Calculate effect size
calculated_effect_size = calculate_effect_size(sample_size_lit, alpha, beta)
calculated_effect_size_our_sample = calculate_effect_size(simple_size_our_data, alpha, beta)

# Print the result
print(f"Cohen's d from our analysis: {effect_size}")
print(f"Builtin ttest function: Required sample size per group: {sample_size_builtin}")
print(f"Manual function: Required sample size per group: {sample_size_manual}")
print(f"Calculated Effect Size from similar literature: {calculated_effect_size}")
print(f"Effect Size from our sample size: {calculated_effect_size_our_sample}")

print(f"Zalpha: {z_alpha_over_2}")
print(f"z_beta: {z_beta}")

