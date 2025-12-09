import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

DATA_DIR = Path("DATA")

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(filepath=DATA_DIR / 'users.txt'):
    """Migrate users from text file to database."""
    if not Path(filepath).exists():
        return False, f"File not found: {filepath}"

    with open(filepath, 'r') as file:
        users = file.readlines()

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    for line in users:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 2:
            continue
        username, password_hash = parts
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, 'user')
            )
            if cursor.rowcount > 0:
                migrated_count += 1
        except Exception as e:
            print(f"Error migrating user {username}: {e}")

    conn.commit()
    conn.close()
    return True, f"Migrated {migrated_count} users from {filepath}"


from app.data.users import insert_user_safe


def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    success, msg = insert_user_safe(username, password_hash, role)
    return success, msg
