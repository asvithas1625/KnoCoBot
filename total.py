import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator

from dotenv import load_dotenv

load_dotenv()
import os

# Your Google Cloud API key for the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_api_endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

def extract_links(soup):
    links = []
    for gdiv in soup.select('.g, .fP1Qef'):
        link = gdiv.select_one('a')
        if link:
            href = link.get('href')
            url = extract_href(href)
            if url:
                links.append(url)
                if len(links) >= 10:  # Break if we have 10 links
                    break
    return links

def extract_href(href):
    if not href:
        return None
    parsed_url = urlparse(href)
    query_params = parse_qs(parsed_url.query)
    if 'q' in query_params and query_params['q']:
        return query_params['q'][0]
    elif parsed_url.netloc:
        return parsed_url.netloc
    else:
        return None

def total_education_tutor(question):
    # Translate the Tamil question to English
    english_question = GoogleTranslator(source='ta', target='en').translate(question)

    # Check if the question contains keywords related to the bot's identity
    identity_keywords = ["யார் நீ", "உன் பெயர் என்ன", "நீங்கள் ஒரு செயற்கை நுண்ணறிவா?","வணக்கம்", "who are you", "what is your name"]
    if any(keyword in question.lower() for keyword in identity_keywords):
        answer = "வணக்கம் ! நான் நோகோபாட். உங்கள் சந்தேகங்களை தீர்க்க நான் இங்கு வந்துள்ளேன்"
        return answer, None, None, []  # Return four values with resource_links as empty list
    
    query = english_question
    url = f"https://www.google.com/search?q={query}"

    # Send a request to Google search
    response = requests.get(url)
    print("Response status code:", response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract search results
    resource_links = extract_links(soup)[:10]  # Limit to 10 links at most

    # Construct the request data
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": english_question}]
            }
        ]
    }

    # Send the request to Gemini API
    response = requests.post(gemini_api_endpoint, json=data)

    if response.status_code == 200:
        # Parse the response and extract the answer
        response_data = response.json()
        if 'candidates' in response_data and response_data['candidates']:
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and candidate['content']['parts']:
                answer = candidate['content']['parts'][0]['text']
                # Translate the answer back to Tamil
                tamil_translation = GoogleTranslator(source='en', target='ta').translate(answer)
                # Search for relevant video
                primary_link, additional_links = search_video(question)
                return tamil_translation, primary_link, additional_links, resource_links
            else:
                print("Error: 'content' or 'parts' key not found or empty in response")
                return None, None, None, []
        else:
            print("Error: 'candidates' key not found or empty in response")
            return None, None, None, []
    else:
        print("Error fetching answer from Gemini API")
        print("Full response content:", response.content.decode("utf-8"))
        return None, None, None, []


def search_video(query):
    videosSearch = VideosSearch(query, limit = 2)
    primary_link = videosSearch.result()['result'][0]['link']
    additional_links = [video['link'] for video in videosSearch.result()['result'][1:]]
    return primary_link, additional_links

# English sentence
english_sentence = "How are you?"

# Translate to Tamil
tamil_translation = GoogleTranslator(target='ta').translate(english_sentence)

# Print the translated text
print(f"English: {english_sentence}")
print(f"Tamil: {tamil_translation}")
