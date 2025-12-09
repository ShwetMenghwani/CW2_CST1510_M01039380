from app.data.db import connect_database
import pandas as pd
from pathlib import Path

DATA_DIR = Path("DATA")
USERS_FILE = DATA_DIR / "users.txt"

conn = connect_database()
df = pd.read_sql_query("SELECT username, password_hash, role FROM users", conn)
conn.close()

with open(USERS_FILE, 'w') as f:
    for _, row in df.iterrows():
        f.write(f"{row['username']},{row['password_hash']},{row['role']}\n")

print(f"Synced {len(df)} users to users.txt")
