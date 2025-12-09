import streamlit as st
from app.data.db import connect_database
from app.services.incident_service import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident,
    export_incidents_to_csv
)
import altair as alt
import pandas as pd

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("🛡️ Cybersecurity Dashboard")

# ------------------------
# Check login and role
# ------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first on the Home page.")
    st.stop()

if st.session_state.role != "cyber":
    st.error("Access denied. You are not authorized for this dashboard.")
    st.stop()

# ------------------------
# Database connection
# ------------------------
conn = connect_database()

# ------------------------
# Add new incident
# ------------------------
st.subheader("Add New Incident")
with st.form("add_incident_form"):
    date = st.date_input("Date")
    incident_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    description = st.text_area("Description")
    submitted = st.form_submit_button("Add Incident")

if submitted:
    incident_id = insert_incident(
        conn,
        date.strftime("%Y-%m-%d"),
        incident_type,
        severity,
        status,
        description,
        reported_by=st.session_state.username
    )
    st.success(f"Incident #{incident_id} added successfully!")
    export_incidents_to_csv()

# ------------------------
# Show all incidents
# ------------------------
st.subheader("All Incidents")
df = get_all_incidents(conn)
st.dataframe(df)

# ------------------------
# Update / Delete incident
# ------------------------
st.subheader("Update / Delete Incident")
incident_id_input = st.number_input("Incident ID", min_value=1, step=1)
new_status = st.selectbox("New Status", ["Open", "In Progress", "Closed"], key="update_status")

if st.button("Update Status"):
    rows = update_incident_status(conn, incident_id_input, new_status)
    if rows > 0:
        st.success(f"Incident #{incident_id_input} status updated to {new_status}")
        export_incidents_to_csv()
    else:
        st.error("Incident not found.")

if st.button("Delete Incident"):
    rows = delete_incident(conn, incident_id_input)
    if rows > 0:
        st.success(f"Incident #{incident_id_input} deleted.")
        export_incidents_to_csv()
    else:
        st.error("Incident not found.")

# ------------------------
# Analytics Charts
# ------------------------
st.subheader("📊 Incident Analytics")

# Fetch incidents again for charts
df_charts = get_all_incidents(conn)

# 1. Number of incidents by type
chart_type = alt.Chart(df_charts).mark_bar().encode(
    x=alt.X('incident_type:N', title='Incident Type'),
    y=alt.Y('count():Q', title='Number of Incidents'),
    tooltip=['incident_type', 'count()']
).properties(
    title="Number of Incidents by Type",
    width=600
)
st.altair_chart(chart_type, use_container_width=True)

# 2. High severity incidents by status
df_high = df_charts[df_charts['severity'] == 'High']
chart_high = alt.Chart(df_high).mark_bar(color='red').encode(
    x=alt.X('status:N', title='Status'),
    y=alt.Y('count():Q', title='High Severity Incidents'),
    tooltip=['status', 'count()']
).properties(
    title="High Severity Incidents by Status",
    width=600
)
st.altair_chart(chart_high, use_container_width=True)

# ------------------------
# Close connection
# ------------------------
conn.close()

