import pandas as pd
import glob
import os
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

# Step 1: Read and Organize Data
data_folder = 'data'  # Replace with your data folder path
files = glob.glob(os.path.join(data_folder, '*.txt'))

# Initialize an empty DataFrame
df = pd.DataFrame(columns=['ParticipantID', 'VideoType', 'TestType', 'CombinedScore'])

for file in files:
    # Extract participant ID, test type, and video type from filename
    filename = os.path.basename(file)
    participant_id, test_type = filename.split('_')[0], filename.split('_')[1]
    participant_id = int(participant_id)
    
    # Determine VideoType based on ParticipantID
    video_type = 'TikTok' if participant_id % 2 != 0 else 'Video'
    
    # Determine TestType (pre or post) based on filename
    test_phase = 'pre' if 'pre' in test_type else 'post'

    # Read scores from file
    with open(file, 'r') as f:
        combined_score = int(f.read().strip().split(',')[-1])  # Get the last number which is the combined score

    # Append to DataFrame
    df = df.append({
        'ParticipantID': participant_id,
        'VideoType': video_type,
        'TestType': test_phase,
        'CombinedScore': combined_score
    }, ignore_index=True)

# Ensure that the 'ParticipantID', 'VideoType', and 'TestType' are treated as categorical variables
df['ParticipantID'] = df['ParticipantID'].astype('category')
df['VideoType'] = df['VideoType'].astype('category')

# Convert 'TestType' to a 'category' dtype
df['TestType'] = df['TestType'].astype('category')

# Convert 'TestType' to numeric values
df['TestTypeNumeric'] = df['TestType'].cat.codes

# Ensure that 'CombinedScore' is of numeric data type
df['CombinedScore'] = pd.to_numeric(df['CombinedScore'], errors='coerce')

# Remove rows with missing values in 'CombinedScore'
df = df.dropna(subset=['CombinedScore'])

# Step 2: Performing Linear Mixed Model
# Create dummy variables for VideoType (0 for TikTok, 1 for Video)
df['VideoTypeDummy'] = (df['VideoType'] == 'Video').astype(int)

# Fit the model
X = df[['VideoTypeDummy', 'CombinedScore']]
X = sm.add_constant(X)
y = df['TestTypeNumeric']

# Fit an OLS model
ols_model = OLS(y, X).fit()

# Print the summary
print(ols_model.summary())
