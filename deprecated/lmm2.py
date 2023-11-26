import os
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Define a mapping from 'TestType' to numeric values
test_type_mapping = {'pre': 0, 'post': 1}

# Load your data from the 'data' folder
data_folder = 'data'
data_files = os.listdir(data_folder)
data = []

# Iterate through the data files and read the contents
for file in data_files:
    if file.endswith(".txt"):
        # Extract participant ID, test type, and scores from the file name
        file_name = os.path.splitext(file)[0]  # Remove the file extension
        participant_id, test_type = file_name.split('_')[:2]
        with open(os.path.join(data_folder, file), 'r') as f:
            scores = [int(score) for score in f.read().strip().split(',')]
            combined_score = scores[-1]
        data.append([participant_id, test_type, combined_score])

# Create a DataFrame from the collected data
df = pd.DataFrame(data, columns=['ParticipantID', 'TestType', 'CombinedScore'])

# Replace 'TestType' values with numeric values
df['TestTypeNumeric'] = df['TestType'].map(test_type_mapping)

# Create a formula for the LMM using 'TestTypeNumeric'
formula = 'CombinedScore ~ TestTypeNumeric + (1|ParticipantID)'

# Fit the Linear Mixed Model
lmm = smf.mixedlm(formula, df, groups=df['ParticipantID'])
result = lmm.fit()

# Print the summary of the LMM results
print(result.summary())
