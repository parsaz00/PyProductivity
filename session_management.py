import sqlite3
import uuid
from datetime import datetime, timedelta

def create_session(user_id):
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()

    # Create sessions table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        created_at TEXT,
        expires_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Generate a new session ID
    session_id = str(uuid.uuid4())

    # Set session expiration (e.g., 24 hours from now)
    created_at = datetime.now()
    expires_at = created_at + timedelta(hours=24)

    # Insert the new session
    cursor.execute('''
    INSERT INTO sessions (id, user_id, created_at, expires_at)
    VALUES (?, ?, ?, ?)
    ''', (session_id, user_id, created_at.isoformat(), expires_at.isoformat()))

    conn.commit()
    conn.close()

    return session_id

def get_user_from_session(session_id):
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()

    # Get the session
    cursor.execute('SELECT user_id, expires_at FROM sessions WHERE id = ?', (session_id,))
    result = cursor.fetchone()

    if result:
        user_id, expires_at = result
        expires_at = datetime.fromisoformat(expires_at)

        # Check if session is expired
        if datetime.now() > expires_at:
            # Session expired, delete it
            cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
            conn.commit()
            conn.close()
            return None
        else:
            conn.close()
            return user_id
    else:
        conn.close()
        return None

def delete_session(session_id):
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()

# Test the session management
if __name__ == "__main__":
    # Create a session for user with ID 1
    session_id = create_session(1)
    print(f"Created session: {session_id}")

    # Get user from the session
    user_id = get_user_from_session(session_id)
    print(f"User ID from session: {user_id}")

    # Delete the session
    delete_session(session_id)
    print("Session deleted")

    # Try to get user from deleted session
    user_id = get_user_from_session(session_id)
    print(f"User ID from deleted session: {user_id}")