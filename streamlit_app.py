import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime


# Display Title and Description
st.title("L'Oréal Action Plan")

# Establishing a Google Sheet Connection
conn = st.experimental_connection('gsheets',type=GSheetsConnection)

# Ftech Exisiting Vendors data
existing_data = conn.read(worksheet= 'Data',usecols = list(range(5)) , ttl = 5)
existing_data = existing_data.dropna(how="all")

# List of Machine Names
machine_name = [
    "LSH01",
    "LSH02",
    "LSH06",
    "LSH04",
    "LSH05"
]
# Onboarding New Vendor Form
with st.form(key="action_plan_form"):
    date = datetime.now()
    name = st.text_input(label="Name")
    machine_name = st.selectbox("Machine", machine_name)
    problem = st.text_area(label="Problem Details")
    action = st.text_area(label="Action Details")

    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not name or not machine_name or not action:
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
            conn.update(worksheet='Data',data=updated_df)
!pipreqs ./