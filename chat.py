
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from urllib.parse import urlparse, parse_qs
from gtts import gTTS
from groq import Groq
from data_search import search

from dotenv import load_dotenv

load_dotenv()
import os

# Environment variable for Groq API key
GROQ_API_KEY =os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Explicit keywords for filtering out explicit contentset GROQ_API_KEY="sk_M9HS4sAbCZGcr1g3KYCsWGdyb3FYDYyCnCl0oMiKvZLy3kTEgnBL"

explicit_keywords = ["explicit", "18+", "adult"]

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

def education_tutor(question):
    # Check if the question contains keywords related to the bot's identity
    identity_keywords = ["who are you","Hello","hi" "yourself", "chatbot","Are you an AI","Are u gemini","what is your name", "Are u chatgpt","Do you use Api","who trained you"]
    if any(keyword in question.lower() for keyword in identity_keywords):
        answer = "Hi, I am KNOCOBOT, your smart tutoring chatbot."
        return answer, None, None, []  # Return four values with resource_links as empty list
    
    # Query Groq for the response
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    # Get the response content from Groq
    if chat_completion.choices:
        answer = chat_completion.choices[0].message.content
    else:
        answer = "Sorry, I couldn't find an answer to your question."

    query = question
    url = f"https://www.google.com/search?q={query}"

    # Send a request to Google search
    response = requests.get(url)
    print("Response status code:", response.status_code)
    #print("Response content:", response.content)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract search results
    resource_links = extract_links(soup)[:10]  # Limit to 10 links at most

    # Search for relevant video
    primary_link, additional_links = search_video(question)
    pdf_answer = search("C:/Users/Rohith/OneDrive/Documents/Roas-app/Roas-app/tnbook.pdf", question)

    return answer, primary_link, additional_links, resource_links, pdf_answer

def search_video(query):
    # Search for videos
    videosSearch = VideosSearch(query, limit = 3)

    # Filter out videos with explicit content
    filtered_results = []
    for video in videosSearch.result()['result']:
        if not any(keyword in video['title'].lower() for keyword in explicit_keywords):
            filtered_results.append(video)

    primary_link = filtered_results[0]['link'] if filtered_results else None
    additional_links = [video['link'] for video in filtered_results[1:]]
    return primary_link, additional_links  

# # Example usage
# question = "Explain the importance of low latency LLMs"
# answer, primary_link, additional_links, resource_links = education_tutor(question)
# pdf_answer=search("C:/Users/sanjai/Downloads/tnbook.pdf",question)
# print("Answer:", answer)
# print("Primary Video Link:", primary_link)
# print("Additional Video Links:", additional_links)
# print("Resource Links:", resource_links)
