import streamlit as st
import pandas as pd
import mysql.connector

# Function to authenticate user
def authenticate(username, password, database):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE Email = %s AND CustomerId = %s"
    cursor.execute(query, (username, int(password)))
    result = cursor.fetchone()
    return result is not None

# Function to display the welcome page
def welcome_page(username, password, database):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE Email = %s AND CustomerId = %s"
    cursor.execute(query, (username, int(password)))
    user_data = cursor.fetchone()

    st.write(f"Welcome, {username}!")

    if user_data:
        st.write("User Details:")
        for key, value in user_data.items():
            st.write(f"- {key}: {value}")
    else:
        st.warning("User details not found.")

# Function to display the feedback page
def feedback_page(username, database):
    st.title("Feedback System")

    # Get user input
    subject = st.text_input("Subject:")
    message = st.text_area("Message:")

    # Displaying the username (email) from the login
    st.write(f"Email: {username}")

    if st.button("Submit Feedback"):
        # Validate input
        if not subject or not message:
            st.warning("Please fill out all fields.")
        else:
            # Save feedback to the database
            save_feedback(username, subject, message, database)

            # Display confirmation message
            st.success("Feedback submitted successfully!")

def save_feedback(username, subject, message, database):
    cursor = database.cursor()
    query = "INSERT INTO feedbacks (Email, Subject, Message) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, subject, message))
    database.commit()

def show_all_feedbacks(database):
    st.title("All Feedbacks")

    # Retrieve all feedbacks from the database
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM feedbacks"
    cursor.execute(query)
    all_feedbacks = cursor.fetchall()

    # Display all feedbacks
    for feedback in all_feedbacks:
        st.write(f"Username: {feedback['Email']}, Subject: {feedback['Subject']}, Message: {feedback['Message']}")
        st.markdown("---")

def main():
    st.title("Login System with Streamlit")

    # Connect to MySQL database
    database_config = {
        'host': 'localhost',
        'user': 'id21808370_nikitmht',
        'password': 'n00bNikit!',
        'database': 'id21808370_feedback'
    }

    try:
        database = mysql.connector.connect(**database_config)
        st.session_state.database = database
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        st.stop()

    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.password = ""

    # Input fields for username and password
    username = st.text_input("Enter Email (Username)")
    password = st.text_input("Enter Customer ID (Password)", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password, st.session_state.database):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.password = password
            welcome_page(username, password, st.session_state.database)
        else:
            st.error("Invalid Credentials. Please try again.")

    # Check if the user is authenticated before displaying the feedback page
    if st.session_state.authenticated:
        feedback_page(username, st.session_state.database)

    # Show All Feedbacks button
    if st.button("Show All Feedbacks"):
        show_all_feedbacks(st.session_state.database)

if __name__ == "__main__":
    main()
