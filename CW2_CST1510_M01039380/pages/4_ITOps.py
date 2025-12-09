import streamlit as st
import pandas as pd
import os
import altair as alt

# ------------------------
# File path
# ------------------------
DATA_DIR = "DATA"
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, "it_tickets.csv")

# ------------------------
# Load CSV or create empty DataFrame
# ------------------------
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=[
        "ticket_id", "ticket_title", "assigned_to", "priority", "status",
        "description", "created_by"
    ])

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
st.title("🖥️ IT Operations Dashboard")

# ------------------------
# LOGIN & ROLE CHECK
# ------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first on the Home page.")
    st.stop()  # stop the page if not logged in

if st.session_state.role != "itops":
    st.error("Access denied. You are not authorized for this dashboard.")
    st.stop()  # stop the page if role is not itops

# ------------------------
# Add new ticket
# ------------------------
st.subheader("Add New Ticket")
with st.form("add_ticket_form"):
    ticket_title = st.text_input("Ticket Title")
    assigned_to = st.text_input("Assigned To")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    description = st.text_area("Description")
    submitted = st.form_submit_button("Add Ticket")

if submitted:
    new_ticket = {
        "ticket_id": len(df) + 1,
        "ticket_title": ticket_title,
        "assigned_to": assigned_to,
        "priority": priority,
        "status": status,
        "description": description,
        "created_by": st.session_state.get("username", "User")
    }
    df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    st.success(f"Ticket #{new_ticket['ticket_id']} added and saved to CSV!")

# ------------------------
# Show all tickets
# ------------------------
st.subheader("All Tickets")
st.dataframe(df)

# ------------------------
# Update / Delete ticket
# ------------------------
st.subheader("Update / Delete Ticket")
ticket_id_input = st.number_input("Ticket ID", min_value=1, step=1)
new_status = st.selectbox("New Status", ["Open", "In Progress", "Closed"], key="update_ticket_status")
new_priority = st.selectbox("New Priority", ["Low", "Medium", "High"], key="update_ticket_priority")

if st.button("Update Ticket"):
    idx = df.index[df["ticket_id"] == ticket_id_input].tolist()
    if idx:
        df.at[idx[0], "status"] = new_status
        df.at[idx[0], "priority"] = new_priority
        df.to_csv(FILE_PATH, index=False)
        st.success(f"Ticket #{ticket_id_input} updated in CSV!")
    else:
        st.error("Ticket not found.")

if st.button("Delete Ticket"):
    idx = df.index[df["ticket_id"] == ticket_id_input].tolist()
    if idx:
        df = df.drop(idx[0]).reset_index(drop=True)
        df.to_csv(FILE_PATH, index=False)
        st.success(f"Ticket #{ticket_id_input} deleted from CSV!")
    else:
        st.error("Ticket not found.")

# ------------------------
# Analytics Charts
# ------------------------
st.subheader("📊 Ticket Analytics")

chart_status = alt.Chart(df).mark_bar(color="orange").encode(
    x=alt.X("status:N", title="Status"),
    y=alt.Y("count():Q", title="Number of Tickets"),
    tooltip=["status", "count()"]
).properties(title="Tickets by Status", width=600)
st.altair_chart(chart_status, use_container_width=True)

chart_priority = alt.Chart(df).mark_bar(color="green").encode(
    x=alt.X("priority:N", title="Priority"),
    y=alt.Y("count():Q", title="Number of Tickets"),
    tooltip=["priority", "count()"]
).properties(title="Tickets by Priority", width=600)
st.altair_chart(chart_priority, use_container_width=True)
