#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Import modules
import pandas as pd    # To load dataset
import numpy as np     # To round the percentage probability for better viewing

import datetime        # To format date

import streamlit as st # To create streamlit formatting
    
# Configure initial page
st.set_page_config(
        page_title="Smart Agricultural Pest Management (SAPM) Dashboard",
        page_icon="sapm_logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Add title
st.write('''
# Smart Agricultural Pest Management (SAPM) Dashboard
This front-end site will showcase the data recorded from the IoT solution's hardware and if there is any detection of pests within your agricultural area.
''')

# Tabs of different information
tab1, tab2, tab3 = st.tabs([":hourglass: Latest Recorded Data", ":bookmark_tabs: Sensor Records Database", ":chart_with_upwards_trend: Data Dashboard"])

# Tab of most recent recorded sensor data
with tab1:

    st.write('''
    ### Latest Recorded Data
    You can view the most recent recorded data here.
    ''')
        
    # Convert JSON object to pandas DataFrame and reorganise it
    df = pd.read_csv("sensor_data.csv")
    df = df.reindex(columns=['time', 'device_id', 'air_temperature', 'air_humidity', 'soil_moisture', 'soil_temperature', 
                             'soil_ph', 'nitrogen_levels', 'phosphorus_levels', 'potassium_levels', 'motion_detected'])

    # Sort by most recent
    df = df.sort_values(by='time', ascending=False)

    # Key for coloured boxes in expanders
    html_string = '''
      <div style="border: 1px solid #f9f9f9; border-radius: 5px; background-color: #fbfbfb; padding: 15px; margin-bottom: 10px">
          <h5><b>Alerts Regarding Conditions</b></h5>
          <p><b style="color:#e0bf2a">Yellow Boxes:</b> Condition levels are in the <i><b>tolerable</b></i> range.</p>
          <p><b style="color:#d64848">Red Boxes:</b> Condition levels are in the <i><b>abnormal</i></b> range.</p><br>
          <h5><b>Alerts Regarding Pest Detection</b></h5>
          <p><b style="color:#6aa84f">Green Boxes:</b> <i><b>No movement</b></i> was detected by the PIR sensors.</p>
          <p><b style="color:#d64848">Red Boxes:</b> <i><b>Movement</b></i> was detected by the PIR sensors.</p>
      </div>
    '''
    st.markdown(html_string, unsafe_allow_html=True)

    # Displays the top 3 most recent rows in the database
    for i in range(3):

        # Reformatting date timstamp into readable text
        date_string = df['time'].iloc[i]
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = date_object.strftime("%d/%m/%Y %I:%M%p")

        # Creating expander template
        with st.expander(f"Sensor {df['device_id'].iloc[i]} – Date Recorded: {formatted_date} UTC"):
            # Columns to separate info
            col1, col2, col3 = st.columns(3, gap="small")

            # Column with recorded data
            with col1:
                st.write('''
                #### Data Recorded
                ''')
                st.write(f'''
                **Air Temperature:** {df['air_temperature'].iloc[i]}°C

                **Air Humidity:** {df['air_humidity'].iloc[i]}%

                **Soil Moisture:** {df['soil_moisture'].iloc[i]}%

                **Soil Temperature:** {df['soil_temperature'].iloc[i]}°C

                **Soil pH:** {df['soil_ph'].iloc[i]}

                **Nitrogen (N) Levels:** {df['nitrogen_levels'].iloc[i]} mg/kg

                **Phosphorus (P) Levels:** {df['phosphorus_levels'].iloc[i]} mg/kg

                **Potassium (K) Levels:** {df['potassium_levels'].iloc[i]} mg/kg

                **Motion Detected:** {df['motion_detected'].iloc[i]}
                ''')

            # Column with environmental conditions that fall outside optimal levels
            with col2:
                # Check if an environmental condition is in abnormal levels
                def check_abnormal(condition_name, condition_value, condition_unit, optimal_min, optimal_max, tolerable_min, tolerable_max):
                    if condition_value < tolerable_min or condition_value > tolerable_max:
                        if condition_unit == 'mg/kg':
                            st.error(f'''
                                **{condition_name}:** {condition_value} {condition_unit} falls outside the healthy range ({optimal_min}-{optimal_max}{condition_unit}).
                        ''')
                        else:
                            st.error(f'''
                            **{condition_name}:** {condition_value}{condition_unit} falls outside the healthy range ({optimal_min}-{optimal_max}{condition_unit}).
                            ''')

                # Check if an environmental condition is in tolerable levels  
                def check_tolerable(condition_name, condition_value, condition_unit, optimal_min, optimal_max, tolerable_min, tolerable_max):
                    if condition_value < optimal_min or condition_value > optimal_max:
                        if condition_value >= tolerable_min and condition_value <= tolerable_max:
                            if condition_unit == 'mg/kg':
                                    st.warning(f'''
                                        **{condition_name}:** {condition_value} {condition_unit} falls outside the healthy range ({optimal_min}-{optimal_max}{condition_unit}).
                                ''')
                            else:
                                st.warning(f'''
                                **{condition_name}:** {condition_value}{condition_unit} falls outside the healthy range ({optimal_min}-{optimal_max}{condition_unit}).
                                ''')

                st.write("#### Alerts Regarding Conditions")

                # Call functions for every environmental condition
                check_tolerable('Air Temperature', df['air_temperature'].iloc[i], '°C', 21, 25, 4, 35)
                check_tolerable('Air Humidity', df['air_humidity'].iloc[i], '%', 40, 70, 20, 85)
                check_tolerable('Soil Moisture', df['soil_moisture'].iloc[i], '%', 50, 70, 15, 80)
                check_tolerable('Soil Temperature', df['soil_temperature'].iloc[i], '°C', 12, 25, 4, 30)
                check_tolerable('Soil pH', df['soil_ph'].iloc[i], '', 6.0, 7.0, 5.5, 8.0)
                check_tolerable('Nitrogen Levels', df['nitrogen_levels'].iloc[i], 'mg/kg', 20, 40, 20, 40)
                check_tolerable('Phosphorus Levels', df['phosphorus_levels'].iloc[i], 'mg/kg', 10, 20, 10, 20)
                check_tolerable('Potassium Levels', df['potassium_levels'].iloc[i], 'mg/kg', 150, 300, 150, 300)

                check_abnormal('Air Temperature', df['air_temperature'].iloc[i], '°C', 21, 25, 4, 35)
                check_abnormal('Air Humidity', df['air_humidity'].iloc[i], '%', 40, 70, 20, 85)
                check_abnormal('Soil Moisture', df['soil_moisture'].iloc[i], '%', 50, 70, 15, 80)
                check_abnormal('Soil Temperature', df['soil_temperature'].iloc[i], '°C', 12, 25, 4, 30)
                check_abnormal('Soil pH', df['soil_ph'].iloc[i], '', 6.0, 7.0, 5.5, 8.0)
                check_abnormal('Nitrogen Levels', df['nitrogen_levels'].iloc[i], 'mg/kg', 20, 40, 20, 40)
                check_abnormal('Phosphorus Levels', df['phosphorus_levels'].iloc[i], 'mg/kg', 10, 20, 10, 20)
                check_abnormal('Potassium Levels', df['potassium_levels'].iloc[i], 'mg/kg', 150, 300, 150, 300)

                st.write('''
                These conditions demand your prompt attention to avert potential losses in crop yield and the onset of pest infestations. Corrective measures must be taken soon to address this issue.
                ''')

            # Column to display if motion was detected    
            with col3:
                st.write(f'''
                #### Alerts Regarding Pest Detection
                ''')

                if df['motion_detected'].iloc[i] == 0:
                    st.success('''
                    No movement has been detected by the Passive Infrared (PIR) sensors on your premises. Likelihood of a current pest infestation is minimal.
                    ''')
                else:
                    st.error('''
                    Movement has been detected by the Passive Infrared (PIR) sensors on your premises. Please refer to the notification titled 'Detection of Pest Infestation' for more information.
                    ''')                  

# Tab of database and dictionary
with tab2:
    st.write('''
    ### Sensor Records Database
    You can view all recorded data from the IoT sensors and additional hardware in this data table.
    ''')

    # Convert JSON object to pandas DataFrame, reorganise and display it
    df = pd.read_csv("sensor_data.csv")
    df = df.reindex(columns=['time', 'device_id', 'air_temperature', 'air_humidity', 'soil_moisture', 'soil_temperature', 
                             'soil_ph', 'nitrogen_levels', 'phosphorus_levels', 'potassium_levels', 'motion_detected'])
    st.dataframe(df)

    # Store dictionary information inside an expander to reduce space
    with st.expander(":blue_book: Data Dictionary"):
        st.markdown('''
        **time:** The time the data was recorded as an ISO 8601 timestamp, for example "2023-11-28T06:16:46.777Z".

        - **2023-11-28:** The year, month and day respectively.

        - **T:** A separator that indicates the start of the time portion.

        - **06:16:46.777:** The hours, minutes, seconds and milliseconds respectively.

        - **Z:** It indicates that the time is in Coordinated Universal Time (UTC). If this was a different time zone, it would be represented as a positive or negative offset from UTC.

        **device_id**: The sensor's/hardware's serial ID. 

        **air_temperature:** Current temperature of the surrounding air in degrees Celcius.

        - **:green[Optimal Range:]** 21-25°C

        - **:orange[Tolerable Range:]** 4-35°C

        **air_humidity:** The humidity of the surrounding air as a percentage.

        - **:green[Optimal Range:]** 40-70%

        - **:orange[Tolerable Range:]** 20-85%

        **soil_moisture:** The water content of the surrounding soil as a percentage of the total soil volume.

        - **:green[Optimal Range:]** 50-70%

        - **:orange[Tolerable Range:]** 15-80%

        **soil_temperature:** Current temperature of the surrounding soil in degrees Celcius.

        - **:green[Optimal Range:]** 12-25°C

        - **:orange[Tolerable Range:]** 4-30°C

        **soil_ph:** The acidity or alkalinity of the surrounding soil.

        - **:green[Optimal Range:]** 6.0-7.0

        - **:orange[Tolerable Range:]** 5.5-8.0

        **nitrogen_levels:** The total concentration of nitrogen (N) measured in milligrams per kilogram soil.

        - **:green[Optimal Range:]** 20-40 mg/kg

        - **:orange[Tolerable Range:]** 20-40 mg/kg

        **phosphorus_levels:** The total concentration of phosphorus (P) measured in milligrams per kilogram soil.

        - **:green[Optimal Range:]** 10-20 mg/kg

        - **:orange[Tolerable Range:]** 10-20 mg/kg

        **potassium_levels:** The total concentration of potassium (K) measured in milligrams per kilogram soil.

        - **:green[Optimal Range:]** 150-300 mg/kg

        - **:orange[Tolerable Range:]** 150-300 mg/kg

        **motion_detected:** The detection of movement by the passive infrared (PIR) sensors.

        - **0:** No movement.

        - **1:** Movement detected.
        ''')

# Tab for analytics and graphs
with tab3:
    st.write('''
    ### Data Analytics Dashboard
    You can view graphs and perform processing and analytics here in this dashboard.
    ''')

    # Convert JSON object to pandas DataFrame and reorganise it
    df = pd.read_csv("sensor_data.csv")
    df = df.reindex(columns=['time', 'device_id', 'air_temperature', 'air_humidity', 'soil_moisture', 'soil_temperature', 
                             'soil_ph', 'nitrogen_levels', 'phosphorus_levels', 'potassium_levels', 'motion_detected'])

    # Set columns to showcase more graphs in limited space
    col1, col2 = st.columns(2, gap="small")

    # Graphs and charts
    with col1:
        st.write('''
        #### Air Temperature over Time
        ''')
        st.line_chart(df[['time', 'air_temperature']].set_index('time'))

        st.write('''
        #### Comparison between Air and Soil Temperatures
        ''')
        st.area_chart(df[['air_temperature','soil_temperature']])

    with col2:
        st.write('''
        #### Soil Moisture over Time
        ''')
        st.bar_chart(df[['time', 'soil_moisture']].set_index('time'))

        st.write('''
        #### Nutrient Concentration Levels over Time
        ''')
        st.bar_chart(df[['nitrogen_levels', 'phosphorus_levels', 'potassium_levels']].set_index(df['time']))           

# # In[ ]:
