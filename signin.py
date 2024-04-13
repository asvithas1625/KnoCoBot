import streamlit as st
import sqlite3
import re
from chat import education_tutor
from total import total_education_tutor
from gtts import gTTS
import os

# Function to create the users table
def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
                )""")
    conn.commit()
    conn.close()

# Function to create the history table for English
def create_english_history_table():
    conn = sqlite3.connect("english_history.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                username TEXT,
                question TEXT,
                answer TEXT
                )""")
    conn.commit()
    conn.close()

# Function to create the history table for Tamil
def create_tamil_history_table():
    conn = sqlite3.connect("tamil_history.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                username TEXT,
                question TEXT,
                answer TEXT
                )""")
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Function to check if email is valid
def is_valid_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

# Function to fetch user data from the database
def get_user_data(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def main():
    ##st.image("pencil.jpg")
    #st.info("hi")
    create_users_table()
    create_english_history_table()  # Create history table for English
    create_tamil_history_table()    # Create history table for Tamil

    # User choice: sign in or sign up
    choice = st.session_state.get("choice", "Sign In")

    if choice == "Sign In":
        #st.title("KnoCoBot ")
        #st.markdown("<h1 style='font-family: 'Julius Sans One'>-Your smart tutor chatbot</h1>", unsafe_allow_html=True)
        st.image("Knocobot.png")
        st.title("LOGIN")
        # Input fields for username and passwordS
        username = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Sign-in button
        if st.button("Login"):
            if is_valid_email(username):
                # Check if the user is registered
                user_data = get_user_data(username)
                if user_data:
                    stored_password = user_data[2]  # Password is stored at index 2
                    if password == stored_password:
                        st.success("Sign-in successful!")
                        st.session_state.choice = "Language Selection"  # Move to language selection page
                        st.session_state.username = username  # Store username in session state
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("User is not registered. Please sign up.")
            else:
                st.error("Invalid email format. Please enter a valid email.")
        
        # Signup button
        if st.button("Sign Up"):
            st.session_state.choice = "Sign Up"

    elif choice == "Sign Up":
        st.title("Sign Up Page")
        # Input fields for username and password
        new_username = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        # Sign-up button
        if st.button("Sign Up"):
            if is_valid_email(new_username):
                if not get_user_data(new_username):
                    register_user(new_username, new_password)
                    st.success("Registration successful! You can now sign in with your new credentials.")
                    st.session_state.choice = "Sign In"  # Move back to sign-in page
                else:
                    st.error("User is already registered. Please sign in.")
            else:
                st.error("Invalid email format. Please enter a valid email.")
        
        # Sign in button after sign up
        if st.button("Sign In"):
            st.session_state.choice = "Sign In"

    elif choice == "Language Selection":
        st.title("Language Selection")
        # Radio button for language selection
        selected_language = st.radio("Select Language:", options=["English", "Tamil"])
        if st.button("Submit"):
            st.session_state.choice = "Chat"  # Move to chat page
            st.session_state.language = selected_language

    elif choice == "Chat":
        # Set title and question input text based on selected language
        if st.session_state.language == "English":
            st.markdown("<h1 style='font-family: 'Julius Sans One'>KnoCoBot , here to help you!</h1>", unsafe_allow_html=True)
            question_placeholder = "Enter your question...."
            question_label = "Question:"
        else:
            st.title('நோகோபாட் இதோ உங்களுக்கு உதவ')
            question_placeholder = "உங்கள் கேள்வி..."
            question_label = "கேள்வி:"

       

        # Adding logo image and text "Knocobot"
        st.sidebar.image("logo1.png", width=80, use_column_width=False)
        st.sidebar.markdown("<div class='knocobot-text' style='font-family: 'Julius Sans One'><b>Knocobot</b></div>", unsafe_allow_html=True)


        st.sidebar.write("Current User:", st.session_state.username)  # Display username in sidebar
        # Logout button
        if st.sidebar.button("Logout", key="logout"):
            st.session_state.choice = "Sign In"  # Move back to sign-in page
            st.session_state.username = None  # Clear the stored username

        # Fetch user's preferred language
        user_language = st.session_state.language

        # Determine which history database to use based on the selected language
        history_db = "english_history.db" if user_language == "English" else "tamil_history.db"

        # Display history below "Logged in as" section
        display_history(st.session_state.username, history_db)

        # User input: question
        #question = st.text_input(question_placeholder, '')
        question=st.chat_input(question_placeholder)



        if question:
            st.write(question)
            if question:
                # Display "Thinking..." until the answer is displayed
                with st.spinner("Thinking..." if user_language == "English" else "யோசிக்கிறேன்......"):
                    # Fetch answer based on selected language
                    if user_language == "English":
                        answer, link, links, resource_link, pdf_answer = education_tutor(question)
                        # Text-to-speech for English Knocobot
                        tts = gTTS(answer, lang="en")
                        tts.save("answer1.mp3")
                        st.audio("answer1.mp3", format="audio/mp3")
                        if pdf_answer:
                            st.write(f'The Answer from pdf is {pdf_answer}')
                    else:
                        answer, link, links, resource_link = total_education_tutor(question)
                    
                    if answer:
                        # Replace "Answer: " with "பதில்: " for Tamil language
                        answer_prefix = "பதில்: " if user_language == "Tamil" else "Answer: "
                        st.write(f'{answer_prefix}{answer}')
                        if link:
                            st.write(f'Relevant Video Link: {link} and {links}')
                            # Render YouTube video
                            st.write(f'resource link {resource_link}')
                            st.video(link)
                        
                        # Add question to history
                        add_to_history(st.session_state.username, question, answer, history_db)

                    else:
                        st.write('Unable to get the answer.')

# Add rest of the functions here...
def add_to_history(username, question, answer, history_db):
    conn = sqlite3.connect(history_db)
    c = conn.cursor()
    c.execute("INSERT INTO history (username, question, answer) VALUES (?, ?, ?)", (username, question, answer))
    conn.commit()
    conn.close()

def display_history(username, history_db):
    conn = sqlite3.connect(history_db)
    c = conn.cursor()
    c.execute("SELECT username, question, answer FROM history WHERE username = ?", (username,))  # Select only records for the logged-in user
    history = c.fetchall()
    conn.close()

    st.sidebar.write("Question History:")
    for i, (username, question, answer) in enumerate(history, start=1):
        truncated_question = ' '.join(question.split()[:30]) + '...' if len(question.split()) > 30 else question
        clicked = st.sidebar.button(f"{i}. {truncated_question}")
        if clicked:
            st.session_state[f"answer_visible_{i}"] = not st.session_state.get(f"answer_visible_{i}", False)

        if st.session_state.get(f"answer_visible_{i}", False):
            st.sidebar.write(f"   Answer: {answer}")

if __name__ == '__main__':
    main()
