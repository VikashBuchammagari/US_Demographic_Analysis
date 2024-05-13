import requests
import pandas as pd
import calendar
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import os
import logging

"""
BELOW CODE USES CENSUS API TO COLLECT CURRENT POPULATION SURVEY (CPS) DATA FROM YEAR 2010 TO 2023.
NOTE: THIS CODE TAKES LONG TIME TO RUN ---- RUN THIS CODE ONLY ONCE------------------------------.

DATA COLLECTED:

PRTAGE: Age of the person
PEMARITL: Marital status
PEEDUCA: Highest level of education completed
HEFAMINC: Household total family income
PESEX: Sex of the person
STATE: FIPS State Code
YEAR: Year of Data
MONTH: Months of Data

"""

# Years to collect data for
years = list(range(2010, 2024))

# Create an empty list to store all data
all_data = []

for year in years:
    # Create an empty list to store data for the year
    year_data = []
    base_url = f"https://api.census.gov/data/{year}/cps/basic/"
    #base_url = "https://api.census.gov/data/"
    api_key = os.environ.get('census_api_key') #REPLACE IT WITH WITH API KEY
    get_params = f"get=PRTAGE,PEMARITL,PEEDUCA,HEFAMINC,PESEX&for=state:*&key={api_key}"


    print(f"Collecting {year}'s Data:")
    # Loop through each month
    for month in range(1, 13):
        month_name = calendar.month_abbr[month].lower()
        # Generate URL for each month and year
        url = f"{base_url}{month_name}?{get_params}"  # using jan, feb, mar format
        print(url)
        # Make request to API
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Collecting {year}-{month_name} 's Data:")
            # Convert response to JSON
            data = response.json()

            # Add year and month columns to the data
            for row in data[1:]:
                row.append(month_name)  # add month
                row.append(year)   # add year
                year_data.append(row)

    # Append year's data to all_data
    all_data.extend(year_data)
    print(f'Done {year}\'s Data')


# Create DataFrame for all years
columns = data[0] + ['MONTH', 'YEAR']
all_df = pd.DataFrame(all_data, columns=columns)

# Define CSV filename for all data
filename = "census_data_all.csv"

# Save DataFrame to CSV for all years
all_df.to_csv(filename, index=False)

print(f"All data saved as {filename}")

"""
BELOW CODE IS TO PUSH THE COLLECTED DATA INTO A CLOUD DATABASE. RUN THIS CODE ONLY ONCE.

"""


# PostgreSQL Connection Details
# REPLACE THE BELOW DETAILS WITH YOUR CREDENTIALS

PGHOST = os.environ.get('PGHOST')
PGDATABASE = os.environ.get('PGDATABASE')
PGUSER = os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')

# Set up metadata
metadata = MetaData()

# Define table structure
census_table = Table(
    'census_data',
    metadata,
    Column('PRTAGE', Integer),
    Column('PEMARITL', Integer),
    Column('PEEDUCA', Integer),
    Column('HEFAMINC', Integer),
    Column('PESEX', Integer),
    Column('STATE', Integer),
    Column('MONTH', String),
    Column('YEAR', Integer)
)

# PostgreSQL Connection
conn_str = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require'

engine = create_engine(conn_str)


# Create the table
metadata.create_all(engine)

# Insert data into the table
all_df.to_sql('census_data', engine, if_exists='append', index=False, chunksize=100000)

print("Data loaded into PostgreSQL database.")

