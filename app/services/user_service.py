import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    # ... migration logic ...
    # 1. Check if the file exists
    if not Path(filepath).exists():
        return False, f"File not found: {filepath}"
    
    # 2. Open and read the file
    with open(filepath, 'r') as file:
        users = file.readlines()
    
    # 3. Connect to the database and prepare to insert users
    conn = connect_database()
    cursor = conn.cursor()
    
    migrated_count = 0  # Keep track of how many users we successfully migrated

    # 4. Process each line in the file (representing a user)
    for line in users:
        line = line.strip()  # Remove any extra spaces or newline characters
        if not line:
            continue  # Skip empty lines
        
        # 5. Split each line by a comma (assuming the format is: username,password_hash)
        parts = line.split(',')
        if len(parts) != 2:
            continue  # Skip lines that don't have the correct format
        
        username, password_hash = parts
        
        # 6. Insert the user into the database (using INSERT OR IGNORE to avoid duplicates)
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, 'user')  # Default role is 'user'
            )
            if cursor.rowcount > 0:  # Increment count if the user was successfully inserted
                migrated_count += 1
        except Exception as e:
            print(f"Error migrating user {username}: {e}")
    
    # 7. Commit changes and close the database connection
    conn.commit()
    conn.close()
    
    # 8. Return the result
    return True, f"Migrated {migrated_count} users from {filepath}"