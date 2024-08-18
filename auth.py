import sqlite3
import bcrypt
from session_management import create_session, delete_session

def register_user(username, password, email):
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
    # Check if username already exists 
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "Username already exists"
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert new user
    cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                   (username, hashed, email))
    conn.commit()
    conn.close()
    return True, "User registered successfully"

def login_user(username, password):
    conn = sqlite3.connect('productivity.db')
    cursor = conn.cursor()
    
     # Fetch user
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        session_id = create_session(user[0])  # user[0] is the user_id
        return True, "Login successful", session_id
    else:
        return False, "Invalid username or password", None

def logout_user(session_id):
    delete_session(session_id)
    return True, "Logged out successfully"
    

if __name__ == "__main__":
    # Test registration
    print(register_user("testuser1", "password123", "test@example12.com"))
    
    # Test login
    success, message, session_id = login_user("testuser1", "password123")
    print(f"Login: {success}, {message}, Session ID: {session_id}")
    
    # Test logout
    if session_id:
        print(logout_user(session_id))
    
    # Test login with wrong password
    print(login_user("testuser1", "wrongpassword"))