import pandas as pd
import os
import numpy as np

downloads_path = os.path.expanduser("~/Downloads/thesis")
file_path = os.path.join(downloads_path, "repo_new.csv")

df = pd.read_csv(file_path)

essential_columns = {'Automation Files', 'Closed PRs (30 days)', 'Closed Issues (30 days)'}
if not essential_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns: {essential_columns - set(df.columns)}")
df['Bot PR Closure Rate (%)'] = np.where(
    (df['Automation Files'] > 0) & (df['Closed PRs (30 days)'] > 0),
    40,  # Not useful now
    0
)
df['Bot Issue Closure Rate (%)'] = np.where(
    (df['Automation Files'] > 0) & (df['Closed Issues (30 days)'] > 0),
    50,  # Not useful now
    0
)

df['Bot Activity Score'] = df['Automation Files'] + \
    np.where(df['Automation Files'] > 0, 
             (df['Closed PRs (30 days)'] + df['Closed Issues (30 days)']) * 0.3, #Not useful
             0)

print(df[['Automation Files', 'Closed PRs (30 days)', 'Closed Issues (30 days)', 'Bot PR Closure Rate (%)', 'Bot Issue Closure Rate (%)', 'Bot Activity Score']].head())

output_file = os.path.join(downloads_path, "repo_bots.csv")
df.to_csv(output_file, index=False)
print(f"Updated file saved as: {output_file}")
