import pandas as pd
from datetime import datetime, timedelta

def merger(file, out):
    # Load the CSV file
    df = pd.read_csv(file, sep=';')

    # Convert the time columns to datetime objects
    if df['interval_start'][0][-3:] == ":00":
        for i in range(len(df["interval_start"])):
            # Use .loc to avoid chained assignment warning
            df.loc[i, 'interval_start'] = df['interval_start'][i][:-3]
            df.loc[i, 'interval_end'] = df['interval_end'][i][:-3]

    # Convert the interval_start and interval_end columns to datetime.time objects
    df['interval_start'] = pd.to_datetime(df['interval_start'], format='%H:%M').dt.time
    df['interval_end'] = pd.to_datetime(df['interval_end'], format='%H:%M').dt.time

    # Prepare a list to hold merged rows
    merged_rows = []

    # Group by course and day
    grouped = df.groupby(['course', 'day'])

    for (course, day), group in grouped:
        # Sort the group by interval_start
        group = group.sort_values(by='interval_start')
        
        # Initialize variables to track the merged interval
        current_start = None
        current_end = None
        
        for index, row in group.iterrows():
            start_time = datetime.combine(datetime.today(), row['interval_start'])
            end_time = datetime.combine(datetime.today(), row['interval_end'])
            
            if current_start is None:
                # Set the current interval to the first row
                current_start = start_time
                current_end = end_time
            else:
                # Check if the current end + 10 minutes matches the next start
                if current_end + timedelta(minutes=10) >= start_time:
                    # Merge intervals
                    current_end = max(current_end, end_time)
                else:
                    # Store the merged row
                    merged_rows.append({
                        'course': course,
                        'day': day,
                        'interval_start': current_start.time(),
                        'interval_end': current_end.time()
                    })
                    # Start a new interval
                    current_start = start_time
                    current_end = end_time

        # Add the last merged interval
        if current_start is not None and current_end is not None:
            merged_rows.append({
                'course': course,
                'day': day,
                'interval_start': current_start.time(),
                'interval_end': current_end.time()
            })

    # Create a DataFrame from the merged rows
    merged_df = pd.DataFrame(merged_rows)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(out, sep=';', index=False)

    print(f"Merging complete. The merged schedule is saved as {out}.")

# Example usage
# merger("filled.csv", "merged_schedule.csv")
