import streamlit as st
import sqlite3
import hashlib

# Function to create and connect to the SQLite database
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Function to create the user table
def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """
    conn.execute(query)
    conn.commit()

# Function to insert a new user into the database
def insert_user(conn, username, password, role):
    query = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
    conn.execute(query, (username, password, role))
    conn.commit()

# Function to check if the entered credentials are valid
def authenticate_user(conn, username, password):
    query = "SELECT password, role FROM users WHERE username = ?"
    cursor = conn.execute(query, (username,))
    row = cursor.fetchone()

    if row is None:
        return None, None

    hashed_password, role = row
    if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
        return role
    else:
        return None


def main():
    st.title("Login Page")

    # Create or connect to the database
    conn = create_connection()
    create_table(conn)

    # User input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate_user(conn, username, password)
        if role is not None:
            st.success(f"Logged in as {username} with role: {role}")
            # Here you can redirect the user to the appropriate dashboard based on the role
        else:
            st.error("Invalid credentials")

if __name__ == "__main__":
    main()
