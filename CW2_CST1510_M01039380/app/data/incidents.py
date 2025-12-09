import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """Insert a new cyber incident."""
    cursor = conn.cursor()
    sql = """
    INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def get_all_incidents(conn):
    """Retrieve all incidents as DataFrame."""
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    return df

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

# Analytical queries
def get_incidents_by_type_count(conn):
    query = "SELECT incident_type, COUNT(*) as count FROM cyber_incidents GROUP BY incident_type ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    query = "SELECT status, COUNT(*) as count FROM cyber_incidents WHERE severity='High' GROUP BY status ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    query = "SELECT incident_type, COUNT(*) as count FROM cyber_incidents GROUP BY incident_type HAVING COUNT(*) > ? ORDER BY count DESC"
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df
