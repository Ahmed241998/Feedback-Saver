import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timezone, timedelta


# Display Title and Description
st.title("L'Oréal Action Plan")

# Establishing a Google Sheet Connection
conn = st.experimental_connection('gsheets',type=GSheetsConnection)

# Ftech Exisiting Vendors data
existing_data = conn.read(worksheet= 'Operators Data',usecols = list(range(5)) , ttl = 5)
existing_data = existing_data.dropna(how="all")

# List of Machine Names
machine_name = [
    "LSH01",
    "LSH02",
    "LSH06",
    "LSH04",
    "LSH05",
    "Kit1",
    "Kit2",
    "Kit3",
    "Kit4",
    "Tub1",
    "Tub2",
    "Tub3",
    "LJAR",
    "LSH07",
    "LSH09",
    "LSF06",
    "LSF07",
    "LSF09",
    "LSF10",
    "Shampoo Cell"
]
# Onboarding New Vendor Form
with st.form(key="action_plan_form"):
    timezone_offset = 3  # Pacific Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    date = datetime.now(tzinfo)
    name = st.text_input(label="Name")
    machine_name = st.selectbox("Machine", machine_name,index =None,placeholder = "Select Machine")
    problem = st.text_area(label="Problem Details")
    action = st.text_area(label="Action Details")
    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not name or not machine_name :
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            # Create a new row of vendor data
            action_data = pd.DataFrame(
                [
                    {
                        "Date": date,
                        "Name": name,
                        "Machine": machine_name,
                        "Problem": problem,
                        "Action": action,
                    }
                ]
            )
            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, action_data], ignore_index=True)
            conn.update(worksheet='Operators Data',data=updated_df)
            st.success("Action is submitted")

