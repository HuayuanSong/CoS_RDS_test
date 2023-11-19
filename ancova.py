import pandas as pd
import glob
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Step 1: Read and Organize Data
data_folder = 'data'  # Replace with your data folder path
files = glob.glob(os.path.join(data_folder, '*.txt'))

# Initialize an empty DataFrame
df = pd.DataFrame(columns=['ParticipantID', 'VideoType', 'TestType', 'ForwardScore', 'BackwardScore', 'CombinedScore'])

for file in files:
    # Extract filename details
    filename = os.path.basename(file)
    parts = filename.split('_')
    
    # Ensure the filename is split into expected parts
    if len(parts) != 3:
        print(f"Unexpected filename format: {filename}")
        continue

    participant_id, test_type, _ = parts
    participant_id = int(participant_id)
    test_type = test_type  # 'pre' or 'post'

    # Determine VideoType based on ParticipantID
    video_type = 'TikTok' if participant_id % 2 != 0 else 'Video'

    # Read scores from file
    with open(file, 'r') as f:
        scores = f.read().strip().split(',')
        forward_score, backward_score, combined_score = map(int, scores)

    # Append to DataFrame
    df = df.append({
        'ParticipantID': participant_id,
        'VideoType': video_type,
        'TestType': test_type,
        'ForwardScore': forward_score,
        'BackwardScore': backward_score,
        'CombinedScore': combined_score
    }, ignore_index=True)

# Print the DataFrame structure before pivoting
print("DataFrame before pivoting:")
print(df.head())
print(df['TestType'].value_counts())

# Pivot DataFrame to have pre and post scores in separate columns
df_pivot = df.pivot_table(index=['ParticipantID', 'VideoType'],
                          columns='TestType', 
                          values='CombinedScore').reset_index()

# Print the DataFrame structure after pivoting
print("DataFrame after pivoting:")
print(df_pivot.head())

# Check the structure and rename columns accordingly
if len(df_pivot.columns) == 4:
    df_pivot.columns = ['ParticipantID', 'VideoType', 'PreTestScore', 'PostTestScore']
else:
    print("Unexpected DataFrame structure after pivoting. Please check the data and pivot table.")
    exit()

# Step 2: Performing ANCOVA
model = ols('PostTestScore ~ C(VideoType) + PreTestScore', data=df_pivot).fit()
ancova_results = sm.stats.anova_lm(model, typ=2)  # typ=2 for ANCOVA

# Output the results
print(ancova_results)
