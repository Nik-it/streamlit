import streamlit as st
import pandas as pd

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
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.database = None

    # Input fields for username and password
    username = st.text_input("Enter Email (Username)")
    password = st.text_input("Enter Customer ID (Password)", type="password")

    # Upload file through Streamlit
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], key='csv_uploader')

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Use st.cache to load the CSV file only once
        @st.cache_data
        def load_database():
            return pd.read_csv(uploaded_file)

        st.session_state.database = load_database()
        st.success("CSV file uploaded successfully!")

    # Login button
    if st.button("Login") and st.session_state.database is not None:
        if authenticate(username, password, st.session_state.database):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.password = password
            welcome_page(username, password, st.session_state.database)
            feedback_page(username, st.session_state.database)
        else:
            st.error("Invalid Credentials. Please try again.")

if __name__ == "__main__":
    main()
