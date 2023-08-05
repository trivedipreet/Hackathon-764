from __future__ import annotations
import streamlit as st
import time
#import gettext
import os
import locale
import datetime
import sqlite3
import hashlib
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd

import random



#global user_role
user_role = None

'''def load_translations(lang):
    #localedir = os.path.join(os.path.dirname(__file__), 'locales')
    # Get the absolute path of the current script
    #script_path = os.path.abspath(__file__)
    # Construct the absolute path of the 'locales' directory based on the script path
    localedir = os.path.join(os.path.dirname(script_path), 'locales')

    translation = gettext.translation('messages', localedir=localedir, languages=[lang])
    translation.install()
    return translation'''



def get_data_from_db():
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    query = "SELECT District FROM regionInfo"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to retrieve towns based on the selected district
def get_towns(selected_district):
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    query = f"SELECT Name FROM regionInfo WHERE District='{selected_district}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['Name'].unique()

def generate_appointment_letter(selected_district1, selected_district2,selected_district3, date_of_visit):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 20)

    c.drawString(100, 750, "Confirmation Letter")
    c.drawString(100, 700, f"District Preference 1: {selected_district1}")
    c.drawString(100, 680, f"District Preference 2: {selected_district2}")
    c.drawString(100, 660, f"District Preference 3: {selected_district3}")
    c.drawString(100, 640, f"Date of Visit: {date_of_visit}")

    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_calendar(year, month):
    # Get the first day of the month
    first_day = datetime.date(year, month, 1)

    # Get the weekday of the first day (0 = Monday, 6 = Sunday)
    first_weekday = first_day.weekday()

    # Get the number of days in the month
    num_days = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 28 if year % 4 != 0 else 29

    # Create an empty calendar
    calendar = [["" for _ in range(7)] for _ in range(6)]

    # Fill in the calendar with the dates
    day = 1
    for i in range(6):
        for j in range(7):
            if i == 0 and j < first_weekday:
                continue
            if day <= num_days:
                calendar[i][j] = day
                day += 1

    return calendar

# Define a function for handling registration of regular patients
def register_regular_patient():
    # Your code for handling registration of regular patients goes here
    st.subheader("Regular Patient Sign Up")
    st.write("Sign Up as a Regular Patient")

    user_name_reg = st.text_input("Username", key="user_name_input1")
    password_reg = st.text_input("Password", key="password_input1", type="password")
    confirm_password_reg = st.text_input("Confirm Password", type="password",key="confirm_password_input1")

    if st.button("Sign Up", key="regular_patient_register_button"):
        # Check if any field is empty
        if not user_name_reg or not password_reg or not confirm_password_reg:
            st.error("Please fill in all fields.")
        # Check if the password and confirm password match
        elif password_reg != confirm_password_reg:
            st.error("Passwords do not match!")
        else:
            # Perform regular patient registration
            # Your code for handling regular patient registration goes here
            st.success("Regular Patient Registration Successful! Click again to continue")

    pass


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def show_get_started_popup():
    greetings = ["Hello", "नमस्ते", "નમસ્તે", "வணக்கம்", "ಹಲೋ", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ନମସ୍କାର"]

    greeting_placeholder = st.empty()  # Placeholder to display greetings

    # Create "Get Started" button with a unique key
    get_started_button = st.button("Get Started", key="get_started_button")

    if get_started_button:  # Check if the button is clicked
        st.session_state.started = True  # Set the flag to True when the button is clicked
        st.session_state.register_completed = False  # Reset register_completed flag
        st.session_state.login_completed = False  # Reset login_completed flag
        st.session_state.ngo_register_completed = False
        st.session_state.doctor_register_completed = False
        st.session_state.doctor_login_completed = False
        st.session_state.ngo_login_completed = False

        show_tabs()

    # Simulate continuous loop of greetings
    for greeting in greetings:
        if st.session_state.started:
            break  # Exit the loop if "Get Started" button is clicked
        greeting_placeholder.markdown(f"<h1 class='center greeting-container' style='font-size: 60px;'>{greeting}</h1>", unsafe_allow_html=True)
        time.sleep(1)  # Faster transition between greetings
        greeting_placeholder.empty()  # Clear the previous greeting before displaying the next

def show_tabs():
    #global user_role
    st.subheader("Welcome!")
    st.write("Create an Account or Log In to Existing Account")

    # Add a selection box for choosing the user role (doctor, NGO, or user)
    user_role = st.selectbox("Select User Role", ["User", "Doctor", "NGO" ],key="select2")

    tabs = ["Sign Up", "Sign In"]
    selected_tab = st.selectbox("Sign Up/Sign In", tabs)

    if selected_tab == "Sign Up":
        # Show the registration page based on the selected role
        if user_role == "Doctor":
            show_doctor_register_page()
        elif user_role == "NGO":
            show_ngo_register_page()
        else:
            show_user_register_page()
    elif selected_tab == "Sign In":
        # Show the login page based on the selected role
        if user_role == "Doctor":
            show_doctor_login_page()
        elif user_role == "NGO":
            show_ngo_login_page()
        else:
            show_user_login_page()
    
    st.session_state.user_role = user_role.lower()
    return user_role

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
    if result:
        # Extract the 'id' from the fetched row and store it in a variable
        id = result[0] 
        st.session_state.id = id # Assuming the 'id' column is the first one in the table
        return id
    else:
        return None

# Helper function to insert user data into the database
def insert_user_data(username, password, age, gender, contact=''):
    # Connect to the SQLite database
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before inserting into the database
    hashed_password = hash_password(password)
    uid = "U"+str(random.randint(1000,9999))

    # Insert user data into the 'user' table
    query = "INSERT INTO user (id, name, password, age, gender, contact) VALUES (? ,?, ?, ?, ?, ?)"
    cursor.execute(query, (uid, username, hashed_password, age, gender, contact))

    st.session_state.id = id

    conn.commit()
    conn.close()

def get_data_from_db():
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    query = "SELECT District FROM regionInfo"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to retrieve towns based on the selected district
def get_towns(selected_district):
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    query = f"SELECT Name FROM regionInfo WHERE District='{selected_district}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['Name'].unique()

def Button():
    st.title("")
    
    # Retrieve data from the database and store it in a DataFrame
    df = get_data_from_db()

    # Get unique districts from the DataFrame
    unique_districts = df['District'].unique()

    # Select the district using a dropdown
    selected_district = st.selectbox('Select a district', unique_districts)

    # Get the towns based on the selected district
    towns = get_towns(selected_district)

    # Select the town using a second dropdown
    selected_town = st.selectbox('Select a town', towns)

    # Display the selected district and town
    # st.write("Selected District:", selected_district)
    # st.write("Selected Town:", selected_town)
    return selected_town


def show_user_register_page():
    st.subheader("Sign Up")
    st.write("Sign Up if you do not already have an account")

    # Add the registration form here
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    
    
    age = st.number_input("Age", min_value=1, max_value=150, value=18)
    gender = st.selectbox("Gender", ["Female", "Other", "Male"])
    region = Button()
    contact = st.number_input("Contact Number", step=1, format="%d")

    if st.button("Sign Up", key="register_button"):  # Add a unique key to the "Register" button
        # Check if any field is empty
        if not user_name or not password or not confirm_password or not age or not gender:
            st.error("Please fill in all required fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Process the registration form
            insert_user_data(user_name, password, age, gender, contact)
            st.success("Registration Successful! Click again to continue")
            st.session_state.register_completed = True


def show_user_login_page():
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
                st.success("Login successful! Click again to continue")
                st.session_state.login_completed = True
                
            else:
                st.error("Invalid username or password.")

def insert_doctor_data(user_name, password, qualification, reg_no, age, gender, contact):
    # Connect to the SQLite database
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before inserting into the database
    hashed_password = hash_password(password)
    did = "D"+str(random.randint(1000,9999))

    # Insert user data into the 'doctor' table
    query = "INSERT INTO doctor (id, name, password, qualification, reg_no, age, gender, contact) VALUES (?, ?, ?, ?, ? ,? ,? ,?)"
    cursor.execute(query, (did, user_name, hashed_password, qualification, reg_no, age, gender, contact))
  

    
    
    st.session_state.id = did
    print(st.session_state.id," in doctor register")
    conn.commit()
    conn.close()

def show_doctor_register_page():
    st.subheader("Sign Up")
    st.write("Sign Up if you do not already have an account")

    # Add the registration form here
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    qualification = st.text_input("Qualification")
    df = get_data_from_db()

    unique_districts = df['District'].unique()

    # Select the district using a dropdown
    selected_district1 = st.selectbox('Region 1', unique_districts)
    selected_district2 = st.selectbox('Region 2', unique_districts)
    selected_district3 = st.selectbox('Region 3', unique_districts)

    #AARYA ADD REGION HERE

    age = st.number_input("Age", min_value=1, max_value=150, value=18)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.number_input("Contact Number", step=1, format="%d")
    reg_no = st.number_input("Registration Number", step=1, format="%d")

    if st.button("Sign Up", key="register_button"):  # Add a unique key to the "Register" button
        # Check if any field is empty
        if not user_name or not password or not confirm_password or not qualification or not reg_no or not age or not gender:
            st.error("Please fill in all required fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Process the registration form
            insert_doctor_data(user_name, password, qualification, reg_no, age, gender, contact)
            st.success("Registration Successful! Click again to continue")
            st.session_state.doctor_register_completed = True
            st.session_state.register_completed = True

def check_doctor_credentials(username, password):
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before checking against the database
    hashed_password = hash_password(password)

    # Check if the username and hashed password exist in the database
    query = "SELECT * FROM doctor WHERE name=? AND password=?"
    cursor.execute(query, (username, hashed_password))
    result = cursor.fetchone()

    conn.close()

    if result:
        # Extract the 'id' from the fetched row and store it in a variable
        doctor_id = result[0] 
        st.session_state.id = doctor_id # Assuming the 'id' column is the first one in the table
        return doctor_id
    else:
        return None

# Function to display the doctor login page
def show_doctor_login_page():
    st.subheader("Doctor Sign In")
    st.write("Sign In if you are a registered doctor:")
    doctor_id = st.text_input("Doctor ID")
    password = st.text_input("Password", type="password")

    if st.button("Sign In", key="doctor_signin_button"):
        if not doctor_id or not password:
            st.error("Please fill in all fields.")
        else:
            result = check_doctor_credentials(doctor_id, password)

            if result is not None:
                st.success("Login successful! Click again to continue")
                st.session_state.login_completed = True
                st.session_state.doctor_login_completed = True
                # Add other doctor-specific functionalities here
            else:
                st.error("Invalid Doctor ID or password.")


def insert_ngo_data(user_name, password, reg_no, contact):
    # Connect to the SQLite database
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before inserting into the database
    hashed_password = hash_password(password)
    nid = "N"+str(random.randint(1000,9999))

    # Insert user data into the 'user' table
    query = "INSERT INTO ngo (id, name, password, reg_no, contact) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (nid, user_name, hashed_password, reg_no, contact))
    
    st.session_state.id = nid
    conn.commit()
    conn.close()

def show_ngo_register_page():
    st.subheader("Sign Up")
    st.write("Sign Up if you do not already have an account")

    # Add the registration form here
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    df = get_data_from_db()

    unique_districts = df['District'].unique()

    # Select the district using a dropdown
    selected_district1 = st.selectbox('Region 1', unique_districts)
    selected_district2 = st.selectbox('Region 2', unique_districts)
    selected_district3 = st.selectbox('Region 3', unique_districts)

    #AARYA ADD REGION HERE

    reg_no = st.number_input("Registration Number", step=1, format="%d")
    
    contact = st.number_input("Contact Number", step=1, format="%d")

    if st.button("Sign Up", key="register_button"):  # Add a unique key to the "Register" button
        # Check if any field is empty
        if not user_name or not password or not confirm_password or not reg_no or not contact:
            st.error("Please fill in all required fields.")
        # Check if the password and confirm password match
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Process the registration form
            insert_ngo_data(user_name, password, reg_no, contact)
            st.success("Registration Successful! Click again to continue")
            st.session_state.register_completed = True
            st.session_state.ngo_register_completed = True

def check_ngo_credentials(username, password):
    conn = sqlite3.connect('Backend/PeriodTracker.db')
    cursor = conn.cursor()

    # Hash the password before checking against the database
    hashed_password = hash_password(password)

    # Check if the username and hashed password exist in the database
    query = "SELECT * FROM ngo WHERE name=? AND password=?"
    cursor.execute(query, (username, hashed_password))
    result = cursor.fetchone()

    conn.close()

    if result:
        # Extract the 'id' from the fetched row and store it in a variable
        id = result[0] 
        st.session_state.id = id # Assuming the 'id' column is the first one in the table
        return id
    else:
        return None

# Function to display the NGO login page
def show_ngo_login_page():
    st.subheader("NGO Sign In")
    st.write("Sign In if you are a registered NGO:")
    ngo_id = st.text_input("NGO ID")
    password = st.text_input("Password", type="password")

    if st.button("Sign In", key="ngo_signin_button"):
        if not ngo_id or not password:
            st.error("Please fill in all fields.")
        else:
            result = check_ngo_credentials(ngo_id, password)

            if result is not None:
                st.success("Login successful! Click again to continue")
                st.session_state.login_completed = True
                st.session_state.ngo_login_completed = True
                # Add other NGO-specific functionalities here
            else:
                st.error("Invalid NGO ID or password.")


def show_user_tab():
    # Implement the Home tab here

    # Add the hamburger menu with options
    menu_options = ["Dashboard", "Calendar", "Download Report", "Contact", "Announcements", "Log out"]
    selected_option = st.sidebar.radio("Menu", menu_options)
    if 'start_date' not in st.session_state:
        st.session_state.start_date = datetime.date.today()
    if 'end_date' not in st.session_state:
        st.session_state.end_date = datetime.date.today()
    
    if selected_option == "Dashboard":
        # Display Dashboard content here
        st.title("Dashboard")
        st.write("welcome ",st.session_state.id)
        st.title("Your Period is expected to arrive in X days.")
        st.write("This is your Dashboard.")
        
        # Drop-down for Symptoms
        st.subheader("Symptoms")
        selected_symptoms = st.multiselect(
            "Select Symptoms",
            ["Abdominal Pain", "Back Pain", "Bloating", "Fatigue", "Headache", "Mood Swings", "Nausea", "Other"],
        )

        # Checkboxes for Pregnancy and Lactation
        st.subheader("Factors")
        is_pregnant = st.checkbox("Pregnant")
        if is_pregnant:
            preg_start_date = st.date_input("Pregnancy Start Date", datetime.date.today())
            preg_end_date = st.date_input("Pregnancy End Date", datetime.date.today())
            if preg_end_date == datetime.date.today():
                preg_end_date = "NOT YET"

        is_lactating = st.checkbox("Lactating")
        if is_lactating:
            lact_start_date = st.date_input("Lactation Start Date", datetime.date.today())
            lact_end_date = st.date_input("Lactation End Date", datetime.date.today())
            if lact_end_date == datetime.date.today():
                lact_end_date = "NOT YET"

        is_contra = st.checkbox("Contraceptive")
        if is_contra:
            cont_start_date = st.date_input("Contraceptive Start Date", datetime.date.today())
            cont_end_date = st.date_input("Contraceptive End Date", datetime.date.today())
            if cont_end_date == datetime.date.today():
                cont_end_date = "NOT YET"

    elif selected_option == "Calendar":
        st.title("Calendar")
        st.write("This is the Calendar.")
        
        start_date = st.date_input("Start Date", st.session_state.start_date)
        end_date = st.date_input("End Date", st.session_state.end_date)

        # Update session state variables when dates are changed
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date

        today = datetime.date.today()
        current_year, current_month = today.year, today.month
        
        # Get the selected year and month from the user
        selected_year = st.selectbox("Select Year", list(range(1960, 2101)), index=current_year - 1900)
        selected_month = st.selectbox("Select Month", [datetime.date(2000, m, 1).strftime("%B") for m in range(1, 13)], index=current_month - 1)

        # Convert month name to numeric value
        selected_month_number = datetime.datetime.strptime(selected_month, "%B").month

        # Generate the calendar for the selected year and month
        calendar = generate_calendar(selected_year, selected_month_number)

        # Generate HTML for the calendar
        calendar_html = "<div class='calendar'>"
        calendar_html += "<div class='month'>" + selected_month + " " + str(selected_year) + "</div>"
        calendar_html += "<div class='day'>Mon</div>"
        calendar_html += "<div class='day'>Tue</div>"
        calendar_html += "<div class='day'>Wed</div>"
        calendar_html += "<div class='day'>Thu</div>"
        calendar_html += "<div class='day'>Fri</div>"
        calendar_html += "<div class='day'>Sat</div>"
        calendar_html += "<div class='day'>Sun</div>"

        # Convert start and end dates to strings for comparison
        fertile_cycle_start = end_date + datetime.timedelta(days=15)
        fertile_cycle_end = fertile_cycle_start + datetime.timedelta(days=4)

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        fertile_cycle_start_str = fertile_cycle_start.strftime("%Y-%m-%d")
        fertile_cycle_end_str = fertile_cycle_end.strftime("%Y-%m-%d")


        for week in calendar:
            for day in week:
                if day == "":
                    calendar_html += "<div class='empty'></div>"
                else:
                    date_str = f"{selected_year}-{selected_month_number:02d}-{day:02d}"
                    is_start_date = date_str == start_date_str
                    is_end_date = date_str == end_date_str
                    if start_date_str <= date_str <= end_date_str:
                        if fertile_cycle_start_str <= date_str <= fertile_cycle_end_str:
                            calendar_html += f"<div class='date fertile'>{day}</div>"
                            continue
                    # Check if the current date is between the start and end dates
                    is_between_dates = start_date <= datetime.date(selected_year, selected_month_number, day) <= end_date

                    classes = "date"
                    if is_start_date:
                        classes += " start"
                    if is_end_date:
                        classes += " end"
                    if is_between_dates:
                        classes += " between"

                    calendar_html += f"<div class='{classes}' onclick='selectDate(this)'>{day}</div>"
                

        calendar_html += "</div>"


        # CSS code to style the calendar
        calendar_css = """
        .calendar {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
        }

        .month {
            grid-column: 1 / -1;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .day {
            padding: 10px;
            text-align: center;
            background-color: #f0f0f0;
        }

        .date {
            padding: 10px;
            text-align: center;
            background-color: #e0e0e0;
            cursor: pointer;
        }

        .date.selected {
            border: 2px solid #2196F3;
        }

        .date.start {
            background-color: red;
        }

        .date.end {
            background-color: red;
        }

        .date.not-yet {
            background-color: red;
        }
        .date.between {
            background-color: red;
        }

        .fertile {
            background-color: blue;
        }
        .empty {
            padding: 10px;
        }
        """

        # JavaScript code to handle date selection
        calendar_js = """
        <script>
        var startDate = null;
        var endDate = null;

        function selectDate(element) {
            if (startDate === null) {
                startDate = element.textContent;
                element.classList.add("selected");
                element.classList.add("start");
            } else if (endDate === null && element.textContent !== startDate) {
                endDate = element.textContent;
                element.classList.add("selected");
                element.classList.add("end");
            } else if (element.textContent === startDate) {
                startDate = null;
                element.classList.remove("selected");
                element.classList.remove("start");
            } else if (element.textContent === endDate) {
                endDate = null;
                element.classList.remove("selected");
                element.classList.remove("end");
            } else if (element.textContent !== startDate && element.textContent !== endDate) {
                var dates = document.querySelectorAll(".date");
                for (var i = 0; i < dates.length; i++) {
                    dates[i].classList.remove("selected");
                    dates[i].classList.remove("start");
                    dates[i].classList.remove("end");
                }
                startDate = element.textContent;
                element.classList.add("selected");
                element.classList.add("start");
            }
        }

        function selectNotYet() {
            startDate = "NOT YET";
            endDate = "NOT YET";
            var dates = document.querySelectorAll(".date");
            for (var i = 0; i < dates.length; i++) {
                dates[i].classList.remove("selected");
                dates[i].classList.remove("start");
                dates[i].classList.remove("end");
            }
        }
        </script>
        """

        # Legend for "Possible Period Day" in red font and "Fertile Cycle Day" in blue font
        legend_html = """
        <div style='color: red; font-weight: bold; margin-top: 10px;'>Possible Period Day</div>
        <div style='color: blue; font-weight: bold;'>Fertile Cycle Day</div>
        """

        # Combine all the HTML and render the calendar with the legend
        calendar_html_with_legend = calendar_html + legend_html

        print("Calendar HTML:", calendar_html_with_legend)

        # Render the calendar using st.markdown
        st.markdown(f"<style>{calendar_css}</style>", unsafe_allow_html=True)
        st.markdown(calendar_html, unsafe_allow_html=True)
        st.markdown(calendar_js, unsafe_allow_html=True)
    
        
    elif selected_option == "Download Report":
        # Display History content here
        st.title(("Download Report"))
        st.write("You can Download report here.")
    
    elif selected_option == "Contact":
        # Display Contact content here
        #st.title("Contact your Nearest Doctor: ")
        st.title("Helpline Numbers: ")
        st.write("Maharashtra Women Helpline: 022-26111103, 1298 , 103")
        st.title("Contact for site help: ")
        st.write("rujutabudke@gmail.com")
        st.write("aaryakkw@gmail.com")
        st.write("trivedipreet@gmail.com")
        st.write("nazrera21.comp@coeptech.ac.in")
        st.write("joshits21.comp@coep.ac.in")
        st.write("shreyabhatkhande@gmail.com")
    elif selected_option == "Announcements":
        # Display Announcements content here
        st.title("Announcements")
        st.write("This is the Announcements page.")
    elif selected_option == "Log out":
        logout_button = st.button("Log out")
        if logout_button:
            # Log out and reset the session state
            st.session_state.started = False
            st.session_state.register_completed = False
            st.session_state.login_completed = False
            st.write("You have been logged out. Click again to confirm Log Out")


def insert_doctor_regions(region1, region2, region3, doctor_id):
    """
    Insert the three regions into the 'doctor' table for the specified doctor.

    Parameters:
        region1 (str): The first region preference.
        region2 (str): The second region preference.
        region3 (str): The third region preference.
        doctor_id (str): The ID of the doctor for whom the regions are being inserted.

    Returns:
        bool: True if the insertion is successful, False otherwise.
    """
    try:
        # Connect to the database (or create if not exists)
        conn = sqlite3.connect('Backend/PeriodTracker.db')
        cur = conn.cursor()

        # Define the SQL query for updating the regions in the doctor table
        update_query = """UPDATE doctor
                          SET region = ?, region2 = ?, region3 = ?
                          WHERE id = ?"""

        # Execute the query with the provided data
        cur.execute(update_query, (region1, region2, region3, doctor_id))

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        return True

    except Exception as e:
        print("Error occurred:", e)
        return False



def show_doctor_tab():
    print(st.session_state.id," in doctor tab")
    st.title("Doctor Viewer")
    # Add doctor-specific functionalities here
    
    menu_options = ["Dashboard","Contact Us", "Log out"]
    selected_option = st.sidebar.radio("Menu", menu_options)
    if selected_option == "Dashboard":
        st.title("Plan a Visit:")
        
        st.write("**Select Region of Visit:**")
        df = get_data_from_db()

        # Get unique districts from the DataFrame
        unique_districts = df['District'].unique()

        # Select the district using a dropdown
        selected_district1 = st.selectbox('**Preference 1**', unique_districts)
        selected_district2 = st.selectbox('**Preference 2**', unique_districts)
        selected_district3 = st.selectbox('**Preference 3**', unique_districts)
        if 'start_date' not in st.session_state:
            st.session_state.start_date = datetime.date.today()
        start_date = st.date_input("**Select Date of Visit:**", st.session_state.start_date)
        # Update session state variables when dates are changed
        st.session_state.start_date = start_date
        st.write("**Selected Districts:**", selected_district1,", ", selected_district2,", ",selected_district3)
        st.write("**Please select a region from the suggested set of regions**")
        ### add region

        if st.button("Confirm"):
            if start_date:
                pdf_bytes = generate_appointment_letter(selected_district1, selected_district2, selected_district3,start_date)
                st.success("Confirmation Letter generated successfully!")
                st.download_button(label="View PDF", data=pdf_bytes, file_name="Appointment_Letter.pdf", mime="application/pdf")
           
            
            
            # Call the function to insert the selected regions into the doctor table
            
            if insert_doctor_regions(selected_district1, selected_district2, selected_district3, st.session_state.id):
                st.success("Regions inserted successfully!")
            else:
                st.warning("Failed to insert regions.")
        else:
            st.warning("Please select a valid date of visit.")

    elif selected_option=='Contact Us':
        st.title("Contact for site help: ")
        st.write("rujutabudke@gmail.com")
        st.write("aaryakkw@gmail.com")
        st.write("trivedipreet@gmail.com")
        st.write("nazrera21.comp@coeptech.ac.in")
        st.write("joshits21.comp@coep.ac.in")
        st.write("shreyabhatkhande@gmail.com")

    elif selected_option=="Log Out":
        logout_button2 = st.button("Log out")
        if logout_button2:
            # Log out and reset the session state
            st.session_state.started = False
            st.session_state.register_completed = False
            st.session_state.login_completed = False
            st.session_state.doctor_login_completed = False
            st.session_state.doctor_register_completed = False
            st.write("You have been logged out. Click again to confirm Log Out")



def insert_ngo_regions(region1, region2, region3, ngo_id):
    """
    Insert the three regions into the 'doctor' table for the specified doctor.

    Parameters:
        region1 (str): The first region preference.
        region2 (str): The second region preference.
        region3 (str): The third region preference.
        doctor_id (str): The ID of the doctor for whom the regions are being inserted.

    Returns:
        bool: True if the insertion is successful, False otherwise.
    """
    try:
        # Connect to the database (or create if not exists)
        conn = sqlite3.connect('Backend/PeriodTracker.db')
        cur = conn.cursor()

        # Define the SQL query for updating the regions in the doctor table
        update_query = """UPDATE ngo
                          SET region = ?, region2 = ?, region3 = ?
                          WHERE id = ?"""

        # Execute the query with the provided data
        cur.execute(update_query, (region1, region2, region3, ngo_id))

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        return True

    except Exception as e:
        print("Error occurred:", e)
        return False



    

def show_ngo_tab():
    st.title("NGO Viewer")
    st.write("welcome ",st.session_state.id)
    menu_options = ["Dashboard","Contact Us", "Log out"]
    selected_option = st.sidebar.radio("Menu", menu_options)
    if selected_option == "Dashboard":
        st.title("Plan a Visit:")
        
        st.write("**Select Region of Visit:**")
        df = get_data_from_db()

        # Get unique districts from the DataFrame
        unique_districts = df['District'].unique()

        # Select the district using a dropdown
        selected_district1 = st.selectbox('**Preference 1**', unique_districts)
        selected_district2 = st.selectbox('**Preference 2**', unique_districts)
        selected_district3 = st.selectbox('**Preference 3**', unique_districts)
        if 'start_date' not in st.session_state:
            st.session_state.start_date = datetime.date.today()
        start_date = st.date_input("**Select Date of Visit:**", st.session_state.start_date)
        # Update session state variables when dates are changed
        st.session_state.start_date = start_date
        st.write("**Selected Districts:**", selected_district1,", ", selected_district2,", ",selected_district3)

        if st.button("Confirm"):
            if start_date:
                pdf_bytes = generate_appointment_letter(selected_district1, selected_district2, selected_district3,start_date)
                st.success("Confirmation Letter generated successfully!")
                st.download_button(label="View PDF", data=pdf_bytes, file_name="Appointment_Letter.pdf", mime="application/pdf")
            if insert_ngo_regions(selected_district1, selected_district2, selected_district3, st.session_state.id):
                st.success("Regions inserted successfully!")
            else:
                st.warning("Failed to insert regions.")
        else:
            st.warning("Please select a valid date of visit.")

    elif selected_option=='Contact Us':
        st.title("Contact for site help: ")
        st.write("rujutabudke@gmail.com")
        st.write("aaryakkw@gmail.com")
        st.write("trivedipreet@gmail.com")
        st.write("nazrera21.comp@coeptech.ac.in")
        st.write("joshits21.comp@coep.ac.in")
        st.write("shreyabhatkhande@gmail.com")

    elif selected_option=="Log Out":
        logout_button3 = st.button("Log out")
        if logout_button3:
            # Log out and reset the session state
            st.session_state.started = False
            #st.session_state.register_completed = False
            #st.session_state.login_completed = False
            st.session_state.ngo_login_completed = False
            st.session_state.ngo_register_completed = False
            st.write("You have been logged out. Click again to confirm Log Out")




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
            height: 50vh;
        }
        .greeting-container {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    #st.title("Menstrual Health Tracker")

    # Remove the global user_role variable from here, as it's now being managed in session_state
    # user_role = None  # Remove this line

    # Initialize st.session_state.started if not already set
    if 'started' not in st.session_state:
        st.session_state.started = False

    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

    # Check if the user is not started, show the Get Started popup
    if not st.session_state.started:
        show_get_started_popup()
    else:
        # Check if the registration or login is not completed, show the tabs
        if not st.session_state.register_completed and not st.session_state.login_completed:
            show_tabs()

        # Check if registration or login is completed and user_role is set, show the respective dashboard
        if (st.session_state.register_completed or st.session_state.login_completed) and st.session_state.user_role:
            
            if st.session_state.user_role == "user":
                
                show_user_tab()
            elif st.session_state.user_role == "doctor" and (st.session_state.doctor_login_completed or st.session_state.doctor_register_completed) :  # Check doctor_login_completed
                
                show_doctor_tab()
            elif st.session_state.user_role == "ngo" and (st.session_state.ngo_login_completed or st.session_state.ngo_register_completed) :  # Check ngo_login_completed
                show_ngo_tab()
            else:
                st.error("Invalid user type.")

if __name__ == "__main__":
    main()
