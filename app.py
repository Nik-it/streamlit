import streamlit as st
import pandas as pd

# Load the database
database_path = '/home/nikit/Downloads/Churn_ModellingEmail.csv'
database = pd.read_csv(database_path)

# Function to authenticate user
def authenticate(username, password):
    for index, row in database.iterrows():
        if row['Email'] == username and row['CustomerId'] == int(password):
            return True
    return False

# Function to display the welcome page
def welcome_page(username, password):
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
def feedback_page(username):
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
            # Save or process the feedback (in this example, just print it)
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"Email: {username}")  # Using the username from the login

            # Display confirmation message
            st.success("Feedback submitted successfully!")

def main():
    st.title("Login System with Streamlit")

    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Input fields for username and password
    username = st.text_input("Enter Email (Username)")
    password = st.text_input("Enter Customer ID (Password)", type="password")

    # Login button
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True

    # Check if the user is authenticated
    if st.session_state.authenticated:
        welcome_page(username, password)
        feedback_page(username)
    else:
        st.error("Invalid Credentials. Please try again.")

if __name__ == "__main__":
    main()