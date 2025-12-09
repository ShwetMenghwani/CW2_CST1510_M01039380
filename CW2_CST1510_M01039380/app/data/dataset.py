import pandas as pd
from app.data.db import connect_database
from pathlib import Path

DATA_DIR = Path("DATA")

def export_datasets_to_csv(filename="datasets.csv"):
    """Export all datasets from database to CSV."""
    conn = connect_database()
    df = get_all_datasets(conn)
    conn.close()
    df.to_csv(DATA_DIR / filename, index=False)
    print(f"Exported {len(df)} datasets to {filename}")

from app.data.db import connect_database

# -------------------------
# CRUD for datasets_metadata table
# -------------------------

def insert_dataset(conn, dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert a new dataset."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    """Retrieve all datasets as a DataFrame."""
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    return df

def update_dataset(conn, dataset_id, dataset_name=None, category=None, source=None, last_updated=None, record_count=None, file_size_mb=None):
    """Update dataset metadata by ID."""
    cursor = conn.cursor()
    # Build dynamic update query
    fields = []
    values = []
    if dataset_name:
        fields.append("dataset_name=?")
        values.append(dataset_name)
    if category:
        fields.append("category=?")
        values.append(category)
    if source:
        fields.append("source=?")
        values.append(source)
    if last_updated:
        fields.append("last_updated=?")
        values.append(last_updated)
    if record_count is not None:
        fields.append("record_count=?")
        values.append(record_count)
    if file_size_mb is not None:
        fields.append("file_size_mb=?")
        values.append(file_size_mb)

    if not fields:
        return 0  # nothing to update

    values.append(dataset_id)
    sql = f"UPDATE datasets_metadata SET {', '.join(fields)} WHERE id=?"
    cursor.execute(sql, values)
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """Delete a dataset by ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id=?", (dataset_id,))
    conn.commit()
    return cursor.rowcount

