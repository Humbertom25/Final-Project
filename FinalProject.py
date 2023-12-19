import pandas as pd
import streamlit as st
import pydeck as pdk
'''import matplotlib.pyplot as plt
import numpy as np

# Data Loading and Processing
data = pd.read_csv('Homework/boston_building_violations.csv')
data['status_dttm'] = pd.to_datetime(data['status_dttm'], errors='coerce')

# Description Group Mapping
description_group_mapping = {
    'Certificate of Occupancy': 'Occupancy Issues',
    'Maintenance': 'Maintenance Issues',
    'Failure to Obtain Permit': 'Permit Issues',
    'Building or Use of Premise req': 'Premise Use Issues',
    'Unsafe Structures': 'Safety Issues',
    'No use of premises permit': 'Permit Issues',
    'Garages': 'Specific Area Issues',
    'Emergency escape and rescue': 'Safety Issues'
}

# Apply the mapping to the dataset
data['grouped_description'] = data['description'].map(description_group_mapping).fillna('Other Issues')

# Generate color mapping for violation descriptions
unique_descriptions = data['grouped_description'].dropna().unique()
default_color = [200, 30, 0, 160]  # Red color for 'Maintenance Issues'
color_mapping = {desc: [np.random.randint(0, 255) for _ in range(3)] + [160] for desc in unique_descriptions}
color_mapping['Maintenance Issues'] = default_color

# Function to create a color-coded map
def create_detailed_map(filtered_data):
    # Assign colors using apply() to handle list values correctly
    filtered_data['color'] = filtered_data['grouped_description'].apply(lambda x: color_mapping.get(x, default_color))

    # Create a pydeck layer using the color mapping
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=filtered_data,
        get_position='[longitude, latitude]',
        get_color='color',
        get_radius=100,
        pickable=True
    )

    # Define the initial view state of the map
    view_state = pdk.ViewState(latitude=42.3601, longitude=-71.0589, zoom=11)

    # Render the map
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{description}"})
    return r


# Function Definitions
def city_with_most_least_violations(data):
    violation_counts = data['violation_city'].value_counts()
    most_violations_city = violation_counts.idxmax()
    least_violations_city = violation_counts.idxmin()
    most_violations_count = violation_counts.max()
    least_violations_count = violation_counts.min()
    return (most_violations_city, most_violations_count), (least_violations_city, least_violations_count)


def plot_top_bottom_violations(data, n=3):
    violation_counts = data['violation_city'].value_counts()
    top_violations = violation_counts.head(n)
    bottom_violations = violation_counts.tail(n)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Top violations bar chart
    top_violations.plot(kind='bar', ax=ax[0], color='#FF5733')
    ax[0].set_title('Top 3 Cities with Most Violations')
    ax[0].set_ylabel('Number of Violations')

    # Bottom violations bar chart
    bottom_violations.plot(kind='bar', ax=ax[1], color='#FF5733')
    ax[1].set_title('Bottom 3 Cities with Least Violations')
    ax[1].set_ylabel('Number of Violations')

    plt.tight_layout()
    return fig

# Function to Plot Violations by Grouped Description
def plot_selected_city_violations_by_grouped_description(data, selected_cities):
    if not selected_cities:
        return None

    # Initialize a figure for plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    # Find unique grouped descriptions for x-axis labels
    unique_grouped_descriptions = data['grouped_description'].unique()
    num_descriptions = len(unique_grouped_descriptions)

    # Process each selected city
    for i, city in enumerate(selected_cities):
        # Filter and group data for the city
        city_data = data[data['violation_city'] == city]
        grouped_data = city_data.groupby('grouped_description').size().reset_index(name='count')

        # Sort the grouped data by count in descending order
        sorted_grouped_data = grouped_data.sort_values(by='count', ascending=False)

        # Calculate the x positions for the bars
        x_positions = np.arange(num_descriptions) + i * 0.2

        # Plot the bars for this city
        ax.bar(x_positions, sorted_grouped_data['count'], width=0.2, label=city)

    # Set the chart labels and title
    ax.set_xlabel('Grouped Violation Descriptions')
    ax.set_ylabel('Number of Violations')
    ax.set_title('Violation Count by Grouped Description in Selected Cities')
    ax.legend(title='Cities')
    ax.set_xticks(np.arange(num_descriptions) + 0.2 * (len(selected_cities) - 1) / 2)
    ax.set_xticklabels(unique_grouped_descriptions, rotation=45, ha='right')
    plt.tight_layout()
    return fig

def most_common_violation(data):
    return data['description'].value_counts().idxmax()

def count_violation_status(data):
    status_counts = data['status'].value_counts()
    closed_count = status_counts.get('Closed', 0)
    open_count = status_counts.get('Open', 0)
    return closed_count, open_count

def filter_violations(data, year_start, year_end, code='All', cities=None):
    filtered = data[(data['status_dttm'].dt.year >= year_start) & (data['status_dttm'].dt.year <= year_end)]
    if code != 'All':
        filtered = filtered[filtered['code'] == code]
    if cities:
        filtered = filtered[data['violation_city'].isin(cities)]
    return filtered

def total_and_unique_violations(data):
    total_violations = len(data)
    unique_violation_codes = data['code'].nunique()
    return total_violations, unique_violation_codes

st.title('Boston Building Violations Analysis')
st.subheader("By: Humberto Zepeda")
st.image("buildngs.jpg")

# Streamlit UI for Map Visualization
st.subheader("Map of Building Violations")

# Multi-select widget for selecting violation descriptions
alphabetical_descriptions = sorted(data['grouped_description'].dropna().unique())
selected_descriptions = st.multiselect("Filter by Violation Descriptions", alphabetical_descriptions, key="select_descriptions_map")

# Range slider to filter data by year
year_to_filter, year_end_filter = st.slider('Year to filter data for map', 2009, 2023, (2009, 2023))

# Filter data based on the selected year range
filtered_data_for_map = data[(data['status_dttm'].dt.year >= year_to_filter) &
                             (data['status_dttm'].dt.year <= year_end_filter) &
(data['grouped_description'].isin(selected_descriptions) if selected_descriptions else True)]

# Display the color-coded map
detailed_map = create_detailed_map(filtered_data_for_map)
st.pydeck_chart(detailed_map)

# Display the city with the most and least building violations
st.subheader("City with Most and Least Building Violations")
((most_violations_city, most_violations_count),
(least_violations_city, least_violations_count)) = city_with_most_least_violations(data)
st.write(f"City with most violations: {most_violations_city} ({most_violations_count} violations)")
st.write(f"City with least violations: {least_violations_city} ({least_violations_count} violations)")

common_violation = most_common_violation(data)
st.write(f"Most common violation: {common_violation}")

closed_count, open_count = count_violation_status(data)
st.write(f"Number of closed violations: {closed_count}")
st.write(f"Number of open violations: {open_count}")

# Display Bar Charts for Top and Bottom 3 Cities
st.subheader("Cities with Most and Least Building Violations")
fig_top_bottom = plot_top_bottom_violations(data)
st.pyplot(fig_top_bottom)

# Interactive Multi-Select for Cities and Grouped Bar Chart by Grouped Description
st.subheader("Explore Violations in Specific Cities")

# Multi-select widget for selecting cities
alphabetical_cities = sorted(data['violation_city'].dropna().unique())
selected_cities = st.multiselect("Select Cities", alphabetical_cities, key="select_cities_explore")

# Optional Multi-select widget for filtering by violation descriptions within the selected cities
alphabetical_descriptions = sorted(data['grouped_description'].dropna().unique())
selected_descriptions = st.multiselect("Optionally Filter by Violation Descriptions",
                                       alphabetical_descriptions, key="select_descriptions_explore")

# Filter data based on the selected cities, and optionally by selected descriptions
if selected_descriptions:
    filtered_data = data[data['violation_city'].isin(selected_cities)
                         & data['grouped_description'].isin(selected_descriptions)]
else:
    filtered_data = data[data['violation_city'].isin(selected_cities)]

# Plotting the data if any cities are selected
if selected_cities:
    fig_selected_cities = plot_selected_city_violations_by_grouped_description(filtered_data, selected_cities)
    if fig_selected_cities:
        st.pyplot(fig_selected_cities)
else:
    st.write("Please select cities to view the data.")

# Advanced Filtering by Year, Code, and City
st.subheader("Explore Dataset!")
# Year range slider
year_start, year_end = st.slider("Select Year Range", 2009, 2023, (2009, 2023))

# Violation code selection
selected_option = st.selectbox("Select Violation Code", ['All'] + sorted(data['code'].dropna().unique().tolist()))
selected_code = selected_option if selected_option != 'All' else 'All'

# Alphabetically sorted cities for multi-select in Advanced Filtering
alphabetical_cities = sorted(data['violation_city'].dropna().unique())
city_selection = st.multiselect("Select Cities", alphabetical_cities, key="select_cities_database")

# Text input for city search (optional, based on your requirement)
city_input = st.text_input("Enter a City Name")
searched_cities = list(set([city_input] + city_selection)) if city_input else city_selection

# Filter the data based on the selected criteria
filtered_violations = filter_violations(data, year_start, year_end, selected_code, searched_cities)
if filtered_violations.empty:
    st.write(f"No Building Violations in {', '.join(searched_cities)}")
else:
    st.write(filtered_violations)

# Total and Unique Violation Counts
st.subheader("Violation Summary")
total_violations, unique_violation_codes = total_and_unique_violations(data)
st.write(f"Total number of violations: {total_violations}")
st.write(f"Number of unique violation codes: {unique_violation_codes}")
