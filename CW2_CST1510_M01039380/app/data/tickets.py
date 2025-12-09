import pandas as pd
from app.data.db import connect_database

DATA_DIR = "DATA"

def insert_ticket(conn, ticket_id, priority, status, category, subject, description, assigned_to):
    """Insert a new IT ticket."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO it_tickets (ticket_id, priority, status, category, subject, description, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (ticket_id, priority, status, category, subject, description, assigned_to)
    )
    conn.commit()
    return ticket_id

def get_all_tickets(conn):
    """Retrieve all tickets as a DataFrame."""
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    return df

def update_ticket_status(conn, ticket_id, new_status):
    """Update the status of a ticket."""
    cursor = conn.cursor()
    cursor.execute("UPDATE it_tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """Delete a ticket."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    return cursor.rowcount

def export_tickets_to_csv(filename="it_tickets.csv"):
    """Export all tickets to CSV."""
    conn = connect_database()
    df = get_all_tickets(conn)
    conn.close()
    df.to_csv(f"{DATA_DIR}/{filename}", index=False)
    print(f"Exported {len(df)} tickets to {filename}")

