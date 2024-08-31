import difflib
import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import wikipediaapi
import socket
import threading

# Predefined prompts and responses
prompts = {
    "hello": ["Hi there! How can I help you today?", "Hello! How can I assist you today?"],
    "how are you": ["I'm just a bot, but I'm here to assist you!", "I'm doing well, thank you! How can I help you?"],
    "bye": ["Goodbye! Have a great day!", "See you later!"],
    "thanks": ["You're welcome! If you have any other questions, feel free to ask.", "No problem! Happy to help."]
}

# Vocabulary for spell checking
vocabulary = ["hello", "how", "are", "you", "bye", "thanks"]

def add_to_vocabulary(word):
    if word not in vocabulary:
        vocabulary.append(word)

def get_closest_match(word):
    matches = difflib.get_close_matches(word, vocabulary)
    return matches[0] if matches else word

def get_closest_prompt(user_input):
    closest_prompt = difflib.get_close_matches(user_input, prompts.keys(), n=1, cutoff=0.6)
    return closest_prompt[0] if closest_prompt else None

def respond_to_prompt(user_input):
    words = user_input.lower().split()
    corrected_words = [get_closest_match(word) for word in words]
    corrected_prompt = " ".join(corrected_words)
    
    closest_prompt = get_closest_prompt(corrected_prompt)
    if closest_prompt:
        response = prompts.get(closest_prompt)
        if response:
            return response[0]  # Return the first response for simplicity
    return None

def respond_to_combined_prompt(user_input):
    for prompt, responses in prompts.items():
        pattern = re.compile(r'\b' + re.escape(prompt) + r'\b')
        if pattern.search(user_input):
            return responses[0]  # Return the first response for simplicity
    return None

def google_search(query):
    search_results = []
    for result in search(query, num_results=1):
        search_results.append(result)
    return search_results

def get_first_paragraph(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if len(paragraph.text) > 50 and "privacy policy" not in paragraph.text.lower():  # Filter out short or irrelevant paragraphs
            return paragraph.text
    return "No relevant content found."

def get_wikipedia_summary(query):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="MyBot/1.0 (https://example.com/mybot)")
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary.split('\n')[0]  # Return the first paragraph of the summary
    return None

# Function to handle client connection
def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        response = respond_to_combined_prompt(request)
        if not response:
            response = respond_to_prompt(request)
        if not response:
            wiki_summary = get_wikipedia_summary(request)
            if wiki_summary:
                response = f"Idk how to respond to that, so i pulled some info from wikipedia: \n ---------------------------- \n {wiki_summary}"
            else:
                search_results = google_search(request)
                if search_results:
                    first_paragraph = get_first_paragraph(search_results[0])
                    response = f"Hard question. So hard that Wikipedia did not have the answer :O. Here is some information I found on google (may not be accurate (at all sometimes)):\n --------------------------------- \n {first_paragraph}"
                else:
                    response = "I'm not sure how to respond to that, and I couldn't find any relevant information. Sorry, bruh, but you are on your own :/ \n If you still think i'm up for the challenge, go to my github and see if there's a new release - get it and brace yourself, soldier :}"
        client_socket.send(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Server started on port 9999")
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

