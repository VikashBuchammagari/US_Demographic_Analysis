import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
import matplotlib.pyplot as plt
import seaborn as sns

default_age_group = (25, 35)
default_state = '1'
default_year = 2023

# PostgreSQL Connection



PGHOST= st.secrets["PGHOST"]
PGDATABASE=st.secrets["PGDATABASE"]
PGUSER=st.secrets["PGUSER"]
PGPASSWORD=st.secrets["PGPASSWORD"]

conn_str = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}?sslmode=require'

pg_engine = create_engine(conn_str)

marital_statuses = {
    "Married - spouse present": 1,
    "Married - spouse absent": 2,
    "Widowed": 3,
    "Divorced": 4,
    "Separated": 5,
    "Never married": 6
}


@st.cache_data(max_entries=20, persist=True)
def load_data():


    demography_data = pd.read_sql_table('census_data', pg_engine, chunksize=100000)
    df = pd.concat(demography_data, ignore_index=True)
    return df

df = load_data()
df.rename({'STATE': 'state'}, axis=1, inplace=True)
# Selection boxes for age group, state, and year

default_age_group = (25, 35)
default_state = '1'
default_year = 2023
state_fips = {     "Alabama": "01",     "Alaska": "02",     "Arizona": "04",     "Arkansas": "05",     "California": "06",     
              "Colorado": "08",     "Connecticut": "09",     "Delaware": "10",     "Florida": "12",     "Georgia": "13",     
              "Hawaii": "15",     "Idaho": "16",     "Illinois": "17",     "Indiana": "18",     "Iowa": "19",     
              "Kansas": "20",     "Kentucky": "21",     "Louisiana": "22",     "Maine": "23",     "Maryland": "24",     "Massachusetts": "25",     
              "Michigan": "26",     "Minnesota": "27",     "Mississippi": "28",     "Missouri": "29",     "Montana": "30",     "Nebraska": "31",   
                  "Nevada": "32",     "New Hampshire": "33",     "New Jersey": "34",     "New Mexico": "35",     "New York": "36",     "North Carolina": "37",    
                    "North Dakota": "38",     "Ohio": "39",     "Oklahoma": "40",     "Oregon": "41",     "Pennsylvania": "42",     "Rhode Island": "44",    
                      "South Carolina": "45",     "South Dakota": "46",     "Tennessee": "47",     "Texas": "48",     "Utah": "49",     "Vermont": "50",     
                      "Virginia": "51",     "Washington": "53",     "West Virginia": "54",     "Wisconsin": "55",     "Wyoming": "56", "Districts of Columbia": "11"}

state_fips_2 = {'01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas', '06': 'California', '08': 'Colorado', '09': 'Connecticut', 
                '10': 'Delaware','11': 'Districts of Columbia', '12': 'Florida', '13': 'Georgia', '15': 'Hawaii', '16': 'Idaho', '17': 'Illinois', '18': 'Indiana', '19': 'Iowa', 
                '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana', '23': 'Maine', '24': 'Maryland', '25': 'Massachusetts', '26': 'Michigan', 
                '27': 'Minnesota', '28': 'Mississippi', '29': 'Missouri', '30': 'Montana', '31': 'Nebraska', '32': 'Nevada', '33': 'New Hampshire', 
                '34': 'New Jersey', '35': 'New Mexico', '36': 'New York', '37': 'North Carolina', '38': 'North Dakota', '39': 'Ohio', '40': 'Oklahoma', 
                '41': 'Oregon', '42': 'Pennsylvania', '44': 'Rhode Island', '45': 'South Carolina', '46': 'South Dakota', '47': 'Tennessee', '48': 'Texas', 
                '49': 'Utah', '50': 'Vermont', '51': 'Virginia', '53': 'Washington', '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming'}



HEFAMINC_dict = {
    "Less than $5,000": "1",
    "$5,000 to $7,499": "2",
    "$7,500 to $9,999": "3",
    "$10,000 to $12,499": "4",
    "$12,500 to $14,999": "5",
    "$15,000 to $19,999": "6",
    "$20,000 to $24,999": "7",
    "$25,000 to $29,999": "8",
    "$30,000 to $34,999": "9",
    "$35,000 to $39,999": "10",
    "$40,000 to $49,999": "11",
    "$50,000 to $59,999": "12",
    "$60,000 to $74,999": "13",
    "$75,000 to $99,999": "14",
    "$100,000 to $149,999": "15",
    "$150,000 or more": "16"
}

PEEDUCA_dict = {'Less than 1st grade': 31,
 '1st, 2nd, 3rd or 4th grade': 32,
 '5th or 6th grade': 33,
 '7th or 8th grade': 34,
 '9th grade': 35,
 '10th grade': 36,
 '11th grade': 37,
 '12th grade no diploma': 38,
 'High school grad-diploma or equiv (GED)': 39,
 'Some college but no degree': 40,
 'Associate degree-occupational/vocational': 41,
 'Associate degree-academic program': 42,
 "Bachelor's degree (ex: BA, AB, BS)": 43,
 "Master's degree (ex: MA, MS, MEng, MEd, MSW)": 44,
 'Professional school deg (ex: MD, DDS, DVM)': 45,
 'Doctorate degree (ex: PhD, EdD)': 46}

#age_group = st.slider('Select Age Group',value=[15,100])

st.title("So, are you wondering, what might be the frequency distribution of people with various marital statuses across an Age range, State, and Year range?\n Well, I was too....Now:")

age_group = st.slider('Select an AGE Range',value=[15,100]) #slider for selecting age range

year_range = st.slider('Select an YEAR Range', value=[2022, 2023], min_value=2010, max_value=2023)

selected_state = st.selectbox("Select a STATE", list(state_fips.keys()),index=26)
print(int(state_fips[selected_state]))


counts = list((df[(df['state'] == int(state_fips[selected_state])) & (df['PRTAGE'] >= age_group[0]) & (df["PRTAGE"] <= age_group[1]) & (df['YEAR'] >= year_range[0])
                  & (df['YEAR'] <= year_range[1]) ])['PEMARITL'].value_counts().sort_index())

#print(counts)

if len(counts) > 6:
    counts = counts[len(counts)-6:]

fig = px.bar(df, x=list(marital_statuses.keys()), y=counts, labels={'y': 'Count', 'x': 'Marital Status'})
st.plotly_chart(fig)

st.title("Frequency Distribution based on Family income over Age, Year range and State")

age_group2 = st.slider('Select an AGE Range:', value=[15, 100]) # Slider for selecting age range
year_range2 = st.slider('Select a YEAR Range:', value=[2022, 2023], min_value=2010, max_value=2023)
selected_state2 = st.selectbox("Select a STATE:", list(state_fips.keys()), index=26)

# Filtering the dataframe based on selected criteria
count_HEFAMINC = list(df[(df['state'] == int(state_fips[selected_state2])) & 
                 (df['PRTAGE'] >=  age_group2[0]) & 
                 (df["PRTAGE"] <=  age_group2[1]) & 
                 (df['YEAR'] >= year_range2[0]) & 
                 (df['YEAR'] <= year_range2[1])]['HEFAMINC'].value_counts().sort_index())



# Plotting the horizontal bar graph
fig = px.bar(x=count_HEFAMINC, y=list(HEFAMINC_dict.keys()), orientation='h', labels={'x': 'Count', 'y': 'Family income'})
st.plotly_chart(fig)


st.title("Gender Distribution over Years")

#year_range3 = st.slider('Select an YEAR Range - ', value=[2022, 2023], min_value=2010, max_value=2023)
# Calculate gender counts
#gender_counts = df[(df['YEAR'] >= year_range3[0]) & 
#                 (df['YEAR'] <= year_range3[1])]["PESEX"].value_counts().sort_index()
#
#print(gender_counts)
#
## Create pie chart
#fig = px.pie(names=['Male', 'Female'], values=gender_counts.values)
#
## Update layout
#fig.update_layout(title='Gender Distribution')
#
## Show the chart
#st.plotly_chart(fig)

def gender_pie_plot(year_range3):
    gender_counts = df[(df['YEAR'] >= year_range3[0]) & 
                 (df['YEAR'] <= year_range3[1])]["PESEX"].value_counts().sort_index()
    print(gender_counts)

    fig = px.pie(names=['Male', 'Female'], values=gender_counts.values)

    # Update layout
    fig.update_layout(title='Gender Distribution')

    # Show the chart
    st.plotly_chart(fig)

year_range3 = st.slider('Select an YEAR Range - ', value=[2022, 2023], min_value=2010, max_value=2023)

gender_pie_plot(year_range3)

st.title("Statewise Heatmap based on Highest Educational Qualification over a rane of Years")
# Plotly heatmap
def plot_heatmap(state_counts):
    fig = px.imshow(state_counts['Count'].values.reshape(-1, 1),
                    labels=dict(y="state"),
                    y=state_counts['state'],
                    color_continuous_scale='YlGnBu')
    fig.update_traces(hovertemplate= "State: %{y} <br> Count: %{z}")
    fig.update_layout(title='Statewise Count',
                      yaxis_title='State',
                      xaxis_title='',
                      xaxis_showticklabels=False,
                      coloraxis_colorbar_title='Count')
    st.plotly_chart(fig)

year_range4 = st.slider('Select an YEAR Range -- ', value=[2022, 2023], min_value=2010, max_value=2023)
selected_edu = st.selectbox("Select a Level of Education:", list(PEEDUCA_dict.keys()), index=13)

state_counts = (df[(df['PEEDUCA'] == PEEDUCA_dict[selected_edu]) & (df['YEAR'] >= year_range4[0]) & 
                 (df['YEAR'] <= year_range4[1]) ].groupby('PEEDUCA')['state'].value_counts(sort=True).reset_index(name='Count'))
state_counts = state_counts[['state','Count']].nlargest(10, columns='Count')
#print(state_counts['state'])
li = []
for x in state_counts['state']:
    if x < 10:
        x = '0'+str(x)
        #print(x)
    if str(x) not in state_fips_2.keys():
        #print(x)
        continue
    #print(x)
    li.append(state_fips_2[str(x)])
#print(li)
#print(li)
state_counts['state'] = li
plot_heatmap(state_counts)
