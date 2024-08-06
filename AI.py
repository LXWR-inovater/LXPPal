import socket
import threading
import difflib
import subprocess
import webbrowser

print("LXPal Version 0.1 alpha. This LXM model CANNOT remember context. It also cannot store previous conversations on its own. Learn more at (site goes here when ready)")

# Predefined prompts and responses
prompts = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hi there! How can I help you today?",
    "hey": "Hi there! How can I help you today?",
    "hey there": "Hi there! How can I help you today?",
    "how are you": "I'm doing well",
    "porn":"I can't talk about that. It's punishable by law to sell pornography. Try something else?",
    "pornography":"I can't talk about that. It's punishable by law to sell pornography. Try something else?",
    "fuck":"That's not needed to sort things out.",
    "shit":"Dang, had to say that, didn't ya?",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome! If you have any other questions, feel free to ask.",
    "what are you doing": "I'm idling.",
    "what are you": "I'm a simple LXM Model, ready to serve you!",
    "why are your sentences so robotic": "It's a side effect of being the most lightweight AI assistant to exist :}",
    "Can you help me": "Sure! What's going on?",
    "Help":"What seems to be the problem?",
    "open app": "Which application would you like to open?"
}

# Vocabulary for spell checking
vocabulary = ["hello", "how", "are", "you", "bye", "thanks", "what", "doing", "hi", "high", "A", "Absorb", "Abuse", "Academic", "Accept", "Your", "Sentences", "so", "robotic", "can", "help", "me", "porn", "pornography", "fuck", "shit", "bye", "thanks", "open", "app"]

# Mapping of natural names to system commands
app_commands = {
    "terminal": "gnome-terminal",
    "text editor": "gedit",
    "web browser": "flatpak run net.waterfox.waterfox",
    # Add more mappings as needed
}

def open_application(app_name):
    system_command = app_commands.get(app_name)
    if system_command:
        try:
            subprocess.Popen(system_command)
        except Exception as e:
            print(f"Failed to open {app_name}: {e}")
    else:
        print(f"No known command for {app_name}")
        response = "That app does not seem to be in my database. Try a different app."
        return response




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
    if 'open app' in user_input.lower():
        # Extract the app name after 'open app'
        app_name = user_input.lower().split('open app')[1].strip()
        # Call the open_application function with the extracted app name
        response = open_application(app_name)
        return f"Opening {app_name}..." if response is None else response
    if 'open website' in user_input.lower():
        # Extract the app name after 'open website'
        web_name = user_input.lower().split('open website')[1].strip()
        response = webbrowser.open(web_name, new=2)
        return f"Opening url {web_name}..." if response is None else response
    else:
        words = user_input.lower().split()
        corrected_words = [get_closest_match(word) for word in words]
        corrected_prompt = " ".join(corrected_words)
        closest_prompt = get_closest_prompt(corrected_prompt)
        response = prompts.get(closest_prompt, "I'm not sure how to respond to that.")
        return response


def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        response = respond_to_prompt(request)
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

