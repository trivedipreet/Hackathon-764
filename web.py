import streamlit as st
import time

def main():
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

    # Check if the user has clicked "Get Started"
    if not st.session_state.started:
        show_get_started_popup()
    else:
        show_home_page()

def show_get_started_popup():
    greetings = ["Hello", "नमस्ते", "નમસ્તે", "வணக்கம்", "ಹಲೋ", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "ନମସ୍କାର"]

    greeting_placeholder = st.empty()  # Placeholder to display greetings

    # Create "Get Started" button with a unique key
    get_started_button = st.button("Get Started", key="get_started_button")

    # Infinite loop to create a continuous loop of greetings
    while not st.session_state.started:  # Exit the loop when the button is clicked
        for greeting in greetings:
            if st.session_state.started:
                break  # Exit the loop if "Get Started" button is clicked
            greeting_placeholder.markdown(f"<h1 class='center greeting-container' style='font-size: 60px;'>{greeting}</h1>", unsafe_allow_html=True)
            time.sleep(1)  # Faster transition between greetings
            greeting_placeholder.empty()  # Clear the previous greeting before displaying the next

    # When "Get Started" button is clicked, show the register page
    show_register_page()

def show_home_page():
    st.subheader("Home Page")
    st.write("Welcome to the Home Page!")
    
    # Show buttons for Sign Up and Sign In with unique keys
    if st.button("Sign Up", key="sign_up_button"):
        show_register_page()
    if st.button("Sign In", key="sign_in_button"):
        show_login_page()

def show_register_page():
    st.subheader("Register Page")
    st.write("This is the Registration Page.")
    
    # Add the registration form here
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        # Show a spinner while processing the registration
        with st.spinner("Processing..."):
            # Validate and process the registration form here
            time.sleep(2)  # Simulate processing time (remove this line in actual implementation)
            st.success("Registration Successful!")

if __name__ == "__main__":
    main()
