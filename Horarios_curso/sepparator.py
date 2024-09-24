import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('merged_schedule.csv', sep=';')

# Function to separate the course column into name, type, and section
def separate_course(course):
    match = re.match(r'^(.*?) \((.*?)\) SEC (\d+)$', course)
    if match:
        return match.groups()  # Return the three groups as a tuple
    return course, None, None  # Return original course and None for others if it doesn't match

# Apply the separation function to the course column
df[['name', 'type', 'section']] = df['course'].apply(separate_course).apply(pd.Series)

# Drop the original course column
df = df.drop(columns=['course'])

# Save the modified DataFrame to a new CSV file
df.to_csv('separated_schedule.csv', sep=';', index=False)

print("Separation complete. The modified schedule is saved as 'separated_schedule.csv'.")
