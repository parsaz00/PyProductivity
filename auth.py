import sqlite3
import bcrypt

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
        return True, "Login successful"
    else:
        return False, "Invalid username or password"
    

if __name__ == "__main__":
    # Test registration
    print(register_user("testuser", "password123", "test@example.com"))
    
    # Test login
    print(login_user("testuser", "password123"))
    print(login_user("testuser", "wrongpassword"))