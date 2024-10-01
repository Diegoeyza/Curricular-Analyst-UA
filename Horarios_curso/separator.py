import pandas as pd
import re

def separator(file,out):
    # Load the CSV file
    df = pd.read_csv(file, sep=';')

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
    df.to_csv(out, sep=';', index=False)

    print(f"Separation complete. The modified schedule is saved as {out}.")

#separator("merged_schedule.csv", "separated_schedule.csv")