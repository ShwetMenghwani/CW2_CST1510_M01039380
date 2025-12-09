import streamlit as st
import pandas as pd
from app.data.db import connect_database
from app.data.dataset import insert_dataset, get_all_datasets, update_dataset, delete_dataset
import altair as alt
from datetime import date

DATA_DIR = "DATA"

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="Data Science Dashboard", layout="wide")
st.title("📊 Data Science Dashboard")

# ------------------------
# Login & role check
# ------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first on the Home page.")
    st.stop()

if st.session_state.role != "datasci":
    st.error("Access denied. You are not authorized for this dashboard.")
    st.stop()

# ------------------------
# CSV export function
# ------------------------
def export_datasets_to_csv(filename="datasets_metadata.csv"):
    """Export all datasets to CSV."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    df.to_csv(f"{DATA_DIR}/{filename}", index=False)
    print(f"Exported {len(df)} datasets to {filename}")

# ------------------------
# Database connection
# ------------------------
conn = connect_database()

# ------------------------
# Add new dataset
# ------------------------
st.subheader("Add New Dataset")
with st.form("add_dataset_form"):
    dataset_name = st.text_input("Dataset Name")
    category = st.text_input("Category")
    source = st.text_input("Source")
    last_updated = st.date_input("Last Updated", value=date.today())
    record_count = st.number_input("Record Count", min_value=0, step=1)
    file_size_mb = st.number_input("File Size (MB)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Dataset")
    if submitted:
        dataset_id = insert_dataset(
            conn,
            dataset_name,
            category,
            source,
            last_updated.strftime("%Y-%m-%d"),
            record_count,
            file_size_mb
        )
        st.success(f"Dataset #{dataset_id} added successfully!")
        export_datasets_to_csv()  # <-- CSV updated automatically

# ------------------------
# Show all datasets
# ------------------------
st.subheader("All Datasets")
df = get_all_datasets(conn)
st.dataframe(df)

# ------------------------
# Update or Delete dataset
# ------------------------
st.subheader("Update / Delete Dataset")
dataset_id_input = st.number_input("Dataset ID", min_value=1, step=1)
new_name = st.text_input("New Dataset Name (optional)")
new_category = st.text_input("New Category (optional)")

if st.button("Update Dataset"):
    rows = update_dataset(
        conn,
        dataset_id_input,
        dataset_name=new_name if new_name else None,
        category=new_category if new_category else None
    )
    if rows > 0:
        st.success(f"Dataset #{dataset_id_input} updated successfully!")
        export_datasets_to_csv()  # <-- CSV updated automatically
    else:
        st.error("Dataset not found or no fields to update.")

if st.button("Delete Dataset"):
    rows = delete_dataset(conn, dataset_id_input)
    if rows > 0:
        st.success(f"Dataset #{dataset_id_input} deleted.")
        export_datasets_to_csv()  # <-- CSV updated automatically
    else:
        st.error("Dataset not found.")

# ------------------------
# Analytics Charts
# ------------------------
st.subheader("📊 Dataset Analytics")

# Reload data to include recent changes
df = get_all_datasets(conn)

# 1. Total records per category
if not df.empty:
    chart_records = alt.Chart(df).mark_bar().encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('record_count:Q', title='Total Records'),
        tooltip=['dataset_name', 'record_count']
    ).properties(
        title="Total Records per Category",
        width=600
    )
    st.altair_chart(chart_records, use_container_width=True)

    # 2. File size distribution
    chart_size = alt.Chart(df).mark_bar(color='green').encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('file_size_mb:Q', title='File Size (MB)'),
        tooltip=['dataset_name', 'file_size_mb']
    ).properties(
        title="Dataset File Size by Category",
        width=600
    )
    st.altair_chart(chart_size, use_container_width=True)
else:
    st.info("No datasets available to display charts.")

# ------------------------
# Close connection
# ------------------------
conn.close()
