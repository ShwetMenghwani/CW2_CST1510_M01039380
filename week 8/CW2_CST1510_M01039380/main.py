from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents


def main():
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    # 2. Migrate users
    migrate_users_from_file()

    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 4. Test CRUD
    conn = connect_database()
    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")
    conn.close()

    # 5. Query data
    conn = connect_database()
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")
    conn.close()


if __name__ == "__main__":
    main()
