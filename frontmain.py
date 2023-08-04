import streamlit as st
import time
#import gettext
import os
import locale
locale.setlocale(locale.LC_ALL, '')  # Set the default locale
import sqlite3
import hashlib


'''def load_translations(lang):
    localedir = os.path.join(os.path.dirname(__file__), 'locales')
    translation = gettext.translation('messages', localedir=localedir, languages=[lang])
    translation.install()
    return translation'''

# Define a function for handling registration of regular patients
def register_regular_patient():
    # Your code for handling registration of regular patients goes here
    st.subheader("Regular Patient Sign Up")
    st.write("Sign Up as a Regular Patient")

    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up", key="regular_patient_register_button"):
        # Check if any field is empty
        if not user_name or not password or not confirm_password:
            st.error("Please fill in all fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Perform regular patient registration
            # Your code for handling regular patient registration goes here
            st.success("Regular Patient Registration Successful!")

    pass

# Define a function for handling registration of doctors
def register_doctor():
    # Your code for handling registration of doctors goes here
    st.subheader("Doctor Sign Up")
    st.write("Sign Up as a Doctor")

    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up", key="doctor_register_button"):
        # Check if any field is empty
        if not user_name or not password or not confirm_password:
            st.error("Please fill in all fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Perform doctor registration
            # Your code for handling doctor registration goes here
            st.success("Doctor Registration Successful!")

    pass

# Define a function for handling registration of NGOs
def register_ngo():
    # Your code for handling registration of NGOs goes here
    st.subheader("NGO Sign Up")
    st.write("Sign Up as an NGO")

    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up", key="ngo_register_button"):
        # Check if any field is empty
        if not user_name or not password or not confirm_password:
            st.error("Please fill in all fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Perform NGO registration
            # Your code for handling NGO registration goes here
            st.success("NGO Registration Successful!")
    pass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_credentials(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before checking against the database
    hashed_password = hash_password(password)

    # Check if the username and hashed password exist in the database
    query = "SELECT name FROM user WHERE name=? AND password=?"
    cursor.execute(query, (username, hashed_password))
    result = cursor.fetchone()

    conn.close()

    return result


def show_get_started_popup():
    greetings = ["Hello", "नमस्ते", "નમસ્તે", "வணக்கம்", "ಹಲೋ", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ନମସ୍କାର"]

    greeting_placeholder = st.empty()  # Placeholder to display greetings

    # Create "Get Started" button with a unique key
    get_started_button = st.button("Get Started", key="get_started_button")

    if get_started_button:  # Check if the button is clicked
        st.session_state.started = True  # Set the flag to True when the button is clicked
        st.session_state.register_completed = False  # Reset register_completed flag
        st.session_state.login_completed = False  # Reset login_completed flag
        show_tabs()

    # Simulate continuous loop of greetings
    for greeting in greetings:
        if st.session_state.started:
            break  # Exit the loop if "Get Started" button is clicked
        greeting_placeholder.markdown(f"<h1 class='center greeting-container' style='font-size: 60px;'>{greeting}</h1>", unsafe_allow_html=True)
        time.sleep(1)  # Faster transition between greetings
        greeting_placeholder.empty()  # Clear the previous greeting before displaying the next

def show_tabs():
    st.subheader("Welcome!")
    st.write("Create an Account or Log In to Existing Account")

    tabs = ["Sign Up", "Sign In"]
    selected_tab = st.selectbox("Sign Up/Sign In", tabs)

    if selected_tab == "Sign Up":
        show_register_page()
    elif selected_tab == "Sign In":
        show_login_page()
    print("Exiting show tabs")    


# Helper function to insert user data into the database
def insert_user_data(username, password, age, gender, email=''):
    # Connect to the SQLite database
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before inserting into the database
    hashed_password = hash_password(password)

    # Insert user data into the 'user' table
    query = "INSERT INTO user (name, password, age, gender, email) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (username, hashed_password, age, gender, email))

    conn.commit()
    conn.close()



def show_register_page():
    st.subheader("Sign Up")
    st.write("Sign Up if you do not already have an account")

    # Add the registration form here
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    age = st.number_input("Age", min_value=1, max_value=150, value=18)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email (optional)")

    if st.button("Sign Up", key="register_button"):  # Add a unique key to the "Register" button
        # Check if any field is empty
        if not user_name or not password or not confirm_password or not age or not gender:
            st.error("Please fill in all required fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Process the registration form
            insert_user_data(user_name, password, age, gender, email)
            st.success("Registration Successful!")
            st.session_state.register_completed = True

def show_register_options():
    st.subheader("Sign Up")
    st.write("Choose the option that best describes you:")

    register_options = ["Regular Patient", "Doctor", "NGO"]
    selected_option = st.selectbox("Select Role", register_options)

    if selected_option == "Regular Patient":
        register_regular_patient()
    elif selected_option == "Doctor":
        register_doctor()
    elif selected_option == "NGO":
        register_ngo()

def show_login_page():
    # Implement the login page here
    st.subheader("Sign In")
    st.write("Sign In if you already have an account:")
    user_name2 = st.text_input("Username")
    password2 = st.text_input("Password", type="password")

    if st.button("Sign In", key="signin_button"):  # Add a unique key to the "Register" button
        # Check if any field is empty
        if not user_name2 or not password2:
            st.error("Please fill in all fields.")
        else:
            # Check the username and password against the database
            result = check_user_credentials(user_name2, password2)

            if result is not None:
                st.success("Login successful!")
                st.session_state.login_completed = True
                
            else:
                st.error("Invalid username or password.")
                

# if __name__ == '__main__':
#     # The table creation code is executed when importing database_creation.py
#     # No need for additional function calls

#     # Run the Streamlit app
#     show_login_page()


def show_home_tab():
    # Implement the Home tab here

    # Add the hamburger menu with options
    menu_options = ["Dashboard", "Calendar", "History", "Help", "Contact", "Announcements", "Settings", "Log out"]
    selected_option = st.sidebar.radio("Menu", menu_options)

    if selected_option == "Dashboard":
        # Display Dashboard content here
        st.title("Dashboard")
        st.write("This is the Dashboard.")
    elif selected_option == "Calendar":
        # Display Calendar content here
        st.title("Calendar")
        st.write("This is the Calendar.")
    elif selected_option == "History":
        # Display History content here
        st.title("History")
        st.write("This is the History.")
    elif selected_option == "Help":
        # Display Help content here
        st.title("Help")
        st.write("This is the Help page.")
    elif selected_option == "Contact":
        # Display Contact content here
        st.title("Contact")
        st.write("This is the Contact page.")
    elif selected_option == "Announcements":
        # Display Announcements content here
        st.title("Announcements")
        st.write("This is the Announcements page.")
    elif selected_option == "Settings":
        # Display Settings content here
        st.title("Settings")
        st.write("This is the Settings page.")
    elif selected_option == "Log out":
        # Log out and reset the session state
        st.session_state.started = False
        st.session_state.register_completed = False
        st.session_state.login_completed = False
        st.write("You have been logged out. Click 'Get Started' to sign in or sign up again.")


def main():
    '''lang = st.selectbox("Select Language", ["English", "Hindi"])
    if lang == "Hindi":
        _ = load_translations('hi')
    else:
        _ = load_translations('en')'''

    st.markdown(
        """
        <style>
        body {
            background-image: url('./path/to/your/image.jpg'); /* Use the correct relative path here */
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            height: 100vh;
        }
        .greeting-container {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Menstrual Health Tracker")
    

    # Initialize st.session_state.started if not already set
    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        show_get_started_popup()
    elif not st.session_state.register_completed and not st.session_state.login_completed:
        show_tabs()
    if st.session_state.register_completed or st.session_state.login_completed:
        show_home_tab()  # Call show_home_tab() directly here
    #this if was elif if theres a glitch

if __name__ == "__main__":
    main()