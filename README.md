KnoCoBot

KnoCoBot is a smart tutor chatbot designed to assist users in both English and Tamil. It offers vernacular support, video rendering, text-to-speech, resource links, and YouTube video links. This repository contains the code and resources needed to set up and run KnoCoBot.

Table of Contents

Features

Getting Started

Prerequisites

Installation

Usage

Testing

Future Scope

Contributing

License

Features
Multilingual support: English and Tamil
Text-to-speech for both languages
Video rendering with relevant YouTube links
Resource links for further reading
Optional multiple-choice questions (MCQs) for concept reinforcement
User authentication and session management
History tracking for questions and answers
PDF download of answers and resources

Getting Started
Prerequisites
Python 3.7+
Streamlit
SQLite
Google Cloud API key for Gemini API
deep_translator library for translation
gTTS library for text-to-speech
youtubesearchpython library for YouTube video search
beautifulsoup4 and requests for web scraping
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/asvitha1625/knocobot.git
cd knocobot
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory and add your Google Cloud API key:

makefile
Copy code
GEMINI_API_KEY=your_google_cloud_api_key
Set up the SQLite databases:

bash
Copy code
python setup_db.py
Usage
Run the Streamlit application:

bash
Copy code
streamlit run app.py
Open your web browser and navigate to http://localhost:8501.

Sign up or log in to start using KnoCoBot.

Select your preferred language and start asking questions.

Testing
To run the test cases, follow the test script provided in the tests directory. Ensure all functionalities are working as expected.

Future Scope
Expansion to More Languages: Adding support for additional languages to cater to a wider audience.

Important Information: This will involve integrating more translation APIs and enhancing the chatbot's NLP capabilities to handle multiple languages seamlessly.
Image-based Question Input: Allowing users to submit questions via images.

Important Information: This feature will utilize OCR (Optical Character Recognition) to extract text from images and process the query. This will make the chatbot more accessible and user-friendly, especially for younger students or those with disabilities.
Personalized Learning Paths: Creating customized learning paths based on the user's questions and progress.

Important Information: This will involve tracking user interactions, understanding their learning needs, and suggesting topics or resources. This personalized approach will enhance the learning experience and ensure users get the most relevant information.
Contributing
We welcome contributions from the community! Please read our Contributing Guide to learn how you can help.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
