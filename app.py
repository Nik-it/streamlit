import streamlit as st
import pandas as pd
import sqlite3

# Function to authenticate user
def authenticate(username, password, database):
    for index, row in database.iterrows():
        if row['Email'] == username and row['CustomerId'] == int(password):
            return True
    return False

# Function to display the welcome page
def welcome_page(username, password, database):
    st.write(f"Welcome, {username}!")

    # Check if there are records for the specified username and password
    user_data = database[(database['Email'] == username) & (database['CustomerId'] == int(password))]
    if not user_data.empty:
        user_details = user_data.iloc[0].to_dict()
        st.write("User Details:")
        for key, value in user_details.items():
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
            save_feedback(username, subject, message)

            # Display confirmation message
            st.success("Feedback submitted successfully!")

# Function to save feedback to the database
def save_feedback(username, subject, message):
    # Connect to SQLite database (create one if not exists)
    conn = sqlite3.connect('feedbacks.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            message TEXT
        )
    ''')

    # Insert feedback into the table
    cursor.execute('''
        INSERT INTO feedbacks (username, subject, message) VALUES (?, ?, ?)
    ''', (username, subject, message))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to show all feedbacks
def show_all_feedbacks():
    st.title("All Feedbacks")

    # Connect to SQLite database
    conn = sqlite3.connect('feedbacks.db')

    # Query all feedbacks from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedbacks')
    feedbacks = cursor.fetchall()

    # Display the feedbacks in a table
    if feedbacks:
        columns = ['ID', 'Username', 'Subject', 'Message']
        feedback_df = pd.DataFrame(feedbacks, columns=columns)
        st.table(feedback_df)
    else:
        st.warning("No feedbacks available.")

    # Close the connection
    conn.close()

def main():
    st.title("Login System with Streamlit")

    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.database = None

    # Input fields for username and password
    username = st.text_input("Enter Email (Username)")
    password = st.text_input("Enter Customer ID (Password)", type="password")

    # Upload file through Streamlit
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Check if a file is uploaded
    if uploaded_file is not None:
        database = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
        st.session_state.database = database

    # Login button
    if st.button("Login") and uploaded_file is not None:
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
        show_all_feedbacks()

if __name__ == "__main__":
    main()
