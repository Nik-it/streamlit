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

    # Input fields for username and password
    username = st.text_input("Enter Email (Username)")
    password = st.text_input("Enter Customer ID (Password)", type="password")

    # Upload file through Streamlit
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Check if a file is uploaded
    if uploaded_file is not None:
        database = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
    else:
        st.warning("Please upload a CSV file.")

    # Login button
    if st.button("Login") and uploaded_file is not None:
        if authenticate(username, password, database):
            welcome_page(username, password, database)
            feedback_page(username)
        else:
            st.error("Invalid Credentials. Please try again.")

if __name__ == "__main__":
    main()
