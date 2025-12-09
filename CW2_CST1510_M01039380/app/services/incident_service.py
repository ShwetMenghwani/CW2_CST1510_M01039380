import pandas as pd
from app.data.db import connect_database
from app.data.incidents import insert_incident, get_all_incidents

DATA_DIR = "DATA"

# ------------------------
# CSV export / migration
# ------------------------
def export_incidents_to_csv(filename="cyber_incidents.csv"):
    """Export all incidents from the database to CSV."""
    conn = connect_database()
    df = get_all_incidents(conn)
    conn.close()
    df.to_csv(f"{DATA_DIR}/{filename}", index=False)
    print(f"Exported {len(df)} incidents to {filename}")

def migrate_incidents_from_csv(filename="cyber_incidents.csv"):
    """Migrate incidents from a CSV file into the database."""
    path = f"{DATA_DIR}/{filename}"
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    conn = connect_database()
    migrated_count = 0
    for _, row in df.iterrows():
        insert_incident(
            conn,
            row['date'],
            row['incident_type'],
            row['severity'],
            row['status'],
            row['description'],
            row.get('reported_by', None)
        )
        migrated_count += 1
    conn.close()
    print(f"Migrated {migrated_count} incidents from {filename}")

def list_incidents():
    """Return all incidents as a DataFrame."""
    conn = connect_database()
    df = get_all_incidents(conn)
    conn.close()
    return df

# ------------------------
# Missing functions causing the ImportError
# ------------------------
def update_incident_status(conn, incident_id, new_status):
    """Update incident status."""
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """Delete an incident."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount
