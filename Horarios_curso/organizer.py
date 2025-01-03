import pandas as pd


def csv_organizer(file, out):
    # Read the CSV data from the file with UTF-8 encoding
    data = file

    # Specify encoding when reading the CSV file
    df = pd.read_csv(data, sep=';', header=0, encoding='utf-8')

    # Prepare output list
    output_data = []

    # Extract course data
    courses_L=[]
    for index, row in df.iterrows():
        # Get the current time slot using .iloc
        inicio_intervalo = row.iloc[0]
        final_intervalo = row.iloc[1] if index + 1 < len(df) else None  # Check for next row's time

        for day in df.columns[2:]:  # Skip the first two columns which are times
            course = row[day]
            courseL=[]
            if pd.notna(course) and course != "":
                # Split courses by commas and create entries
                splitted=course.split(",")
                for i in range(0,len(splitted)):
                    if (i==0):
                        if (splitted[i][-1]==" "):
                            courseL.append(splitted[i][-2])
                        else:
                            courseL.append(splitted[i][-1])
                    else:
                        courseL.append(splitted[i][0])
                courses = [c.strip() for c in course.split(',')]

                # Extract the base course name (e.g., PROGRAMACION (LAB) SEC)
                base_course_name = " ".join(courses[0].split()[:-1])  # Assuming the last part is the SEC number

                for i in range(len(courses)):
                    # Construct the full course name for each entry
                    full_course_name = f"{base_course_name} {courseL[i]}"
                    # Check if the course should have the next time interval
                    if final_intervalo is None and index + 1 < len(df):
                        next_row = df.iloc[index + 1]
                        next_inicio_intervalo = next_row.iloc[0]
                        # Check if the current course should match the next interval
                        if next_inicio_intervalo != inicio_intervalo:
                            final_intervalo = next_inicio_intervalo
                    
                    output_data.append({
                        "course": full_course_name,
                        "day": day,
                        "interval_start": inicio_intervalo,
                        "interval_end": final_intervalo
                    })

    # Save to CSV using pandas to preserve encoding
    output_file = out
    output_df = pd.DataFrame(output_data)

    # Use utf-8 encoding to handle special characters
    output_df.to_csv(output_file, sep=';', index=False, encoding='utf-8')

    print(f"Data has been saved to {output_file}")

#csv_organizer("first_part.csv", "filled.csv")