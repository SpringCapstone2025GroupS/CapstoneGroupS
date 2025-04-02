'''
This Script Calls the Airport db, and creates a holistic Airport List in the form of a CSV.

It catches the rows that malformed and saved them in a separate csv file called bad_airports_data.csv
'''

import pandas as pd
import requests

# URL of the airport.dat file
url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

# Define column names manually
columns = [
    "Airport ID", "Name", "City", "Country", "IATA", "ICAO",
    "Latitude", "Longitude", "Altitude", "Timezone", "DST",
    "Tz Database Timezone", "Type", "Source"
]

# Download the raw data from the URL
response = requests.get(url)
raw_data = response.text

# Split raw data into individual lines
lines = raw_data.split("\n")

# Lists to store valid and bad rows
valid_rows = []
bad_rows = []

# Process each line manually
for line in lines:
    # Split the line by comma -> to check if the length of the lines are matching with the columns list length
    split_line = line.split(",")
    print (line)

    # Ensure the line has the correct number of columns
    if len(split_line) == len(columns):
        valid_rows.append(split_line)  # Append raw values
    else:
        bad_rows.append(line)  # Store "bad" row, ones with length not matching the len(columns)

# Convert valid rows into a DataFrame
df = pd.DataFrame(valid_rows, columns=columns)

# Strip extra spaces and remove quotes
df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(include=['object']).apply(
    lambda x: x.str.replace(r'^"+|"+$', '', regex=True)
)

# Convert numeric columns properly
df["Airport ID"] = pd.to_numeric(df["Airport ID"], errors='coerce') # -> errors = 'coerce', if the data entry cannot be casted to a numeric value it returns it as a NaN entry.
df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')
df["Altitude"] = pd.to_numeric(df["Altitude"], errors='coerce')

print(df.dtypes)

# Convert bad rows to a DataFrame
bad_df = pd.DataFrame({"Bad Rows": bad_rows})

# Print verification
print(f"Total Lines Read: {len(lines)}")
print(f"Total valid rows: {df.shape[0]}")
print(f"Total bad rows: {bad_df.shape[0]}")

# Save valid data to CSV
csv_filename = "airports_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Valid CSV file saved as {csv_filename}")

# Save bad rows to a separate CSV
bad_csv_filename = "bad_airports_data.csv"
bad_df.to_csv(bad_csv_filename, index=False)
print(f"Bad rows saved as {bad_csv_filename}")
