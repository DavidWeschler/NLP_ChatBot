from tracker import Tracker
from policy import Policy
from bio_tagger import Bio_Tagger
from nlg_model import NlgModel
import random
import time
import sys
import re

botName = "Hadas: "
userName = "You: "

def suprise_func(
    name,
    text,
    color_code,
    base_speed=0.025,
    speed_variation=0.005,
    punctuation_pause=0.4,
    word_pause_multiplier=0.3,
    sentence_pause=0.4,
    thinking_pause=0.4,
    flush=True
):
    time.sleep(0.4)
    for char in f"{color_code}{name} {"\033[0m"}":
        print(char, end="", flush=True)
        time.sleep(0.07)

    for _ in range(random.randint(1, 3)):
        for dots in [".", "..", "..."]:
            print(f"{color_code}\r{name} {dots}  {"\033[0m"}", end="", flush=True)
            time.sleep(0.25)
    print(f"{color_code}\r{name}    {"\033[0m"}", end="", flush=True)
    print(f"{color_code}\r{name}{"\033[0m"}", end="", flush=True)
    time.sleep(0.35)

    punctuation = {',', ';', ':', '!', '?', '...', '(', ')'}
    sentences = re.split(r'(?<=\. )', text)

    for sentence in sentences:
        if random.random() < 0.1:
            time.sleep(thinking_pause)

        for char in sentence:
            print(char, end='', flush=flush)
            if char in punctuation:
                time.sleep(punctuation_pause + random.uniform(0, speed_variation))
            elif char == ' ':
                time.sleep(base_speed * word_pause_multiplier + random.uniform(0, speed_variation / 2))
            else:
                time.sleep(base_speed)

        time.sleep(sentence_pause + random.uniform(0, speed_variation))

    print()

def pretty_print(name, message, color):
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    color_code = colors.get(color.lower(), colors["reset"])

    # Print the message with the selected color
    suprise_func(name, f"{color_code}{message}{colors['reset']}", color_code)


def wantToContinue():
    continueUser = ["ok", "okay", "oka", "yes", "yeah", "sure", "ok", "okay", "yup", "yea", "yep", "of course", "indeed", "absolutely", "definitely", "please", "start over", "try again", "restart", "reset"]
    messages = [
        "I seem to be having trouble understanding you. Do you still want to continue?",
        "Apologies, I’m having difficulty following. Do you want to keep going on?",
        "I seem to be having trouble understanding you. Do you want to keep going?",
        "Apologies, I’m having difficulty following. Would you like to keep on describing your route?",
        "I seem to be having trouble understanding you. Do you still want to continue?",
        "Apologies, I’m having difficulty following. Would you want to keep going on?",
        "I may not have understood completely. Would you like to keep on describing your route?",
    ]
    pretty_print(botName, f"{random.choice(messages)}", "red")
    user_input = input(f"\033[35m{userName}").strip()
    if user_input.lower() in continueUser:
        return True
    else:
        for inp in continueUser:
            if inp in user_input.lower():
                return True
    return False

def isSatisfied(done):
    satisfied = ["ok", "okay", "oka", "yes", "yeah", "sure", "ok", "okay", "yup", "yea", "ya", "yep", "of course", "indeed", "absolutely", "definitely", "please", "start over", "try again", "restart", "reset"]
    if done:
        messages = [
            "Are you happy with the route I've planned for you?",
            "Do you like the route I've planned for you?",
            "Are you happy with the route I've planned for you?",
            "Do you approve of the route I've planned for you?",
            "Are you content with the route I've planned for you?",
            "Do you find the route I've planned for you satisfactory?",
            "Are you pleased with the route I've planned for you?",
        ]
        pretty_print("", f"{random.choice(messages)}", "green")
        user_input = input(f"\033[35m{userName}").strip()
        if user_input.lower() in satisfied:
            return True
        else:
            for inp in satisfied:
                if inp in user_input.lower():
                    return True
    return False


# for finishing the bot conversation
def generate_ending_message():
    messages = [
        "I'm sorry, I seem to be having trouble understanding you. Let me try to generate a route with the details I have so far.",
        "Apologies, I’m having difficulty following. I’ll do my best to create a route with the information provided.",
        "I’m sorry, I didn’t quite catch that. I’ll try generating a route based on the details I’ve received.",
        "Sorry, I’m having some trouble understanding. Let me try to create a route with the information I have.",
        "I couldn’t fully understand your input, but I’ll attempt to generate a route based on what’s available.",
        "My apologies for the confusion. I’ll proceed with generating a route using the information I have.",
        "I may not have understood completely, but I’ll do my best to generate a route from the provided details."
    ]
    return random.choice(messages)

def generate_happy_ending_message():
    messages = [
        "I'm glad you're happy with the route I've planned for you. Enjoy your run!",
        "I'm pleased that you like the route I've planned for you. Have a great run!",
        "I'm happy that you approve of the route I've planned for you. Enjoy your run!",
        "Excellent! I'm glad you're content with the route I've planned for you. Have a great run!",
        "I'm delighted that you find the route I've planned for you satisfactory. Enjoy your run!",
        "I'm pleased that you're happy with the route I've planned for you. Have a great run!",
    ]
    return random.choice(messages)

def generate_starting_message():
    messages = [
        "Welcome to the R&D route planner bot! I can help you plan a route for your next run. Let's get started!",
        "Hello! I'm the R&D route planner bot. I can assist you in planning a route for your run. Let's begin!",
        "Greetings! I'm the R&D route planner bot. I'm here to help you plan a route for your run. Let's start!",
        "Hi there! I'm the R&D route planner bot. I can guide you in planning a route for your run. Let's get going!",
        "Hey! I'm the R&D route planner bot. I'm here to assist you in planning a route for your run. Let's begin!",
        "Hello! I'm the R&D route planner bot. I can help you map out a route for your run. Let's start!",
        "Alright, let's start over. I can help you plan a route for your next run. Let's get started!"
    ]
    return random.choice(messages)

def generate_continue_message():
    messages = [
        'Okay, let’s continue. Please provide the details for your route.',
        'Great! Let’s keep going. Please provide the remaining details for your route.',
        'Alright, let’s proceed. Please continue by providing the necessary details for your route.',
        'Understood! Let’s continue. Please provide the remaining details for your route.',
        'Got it! Let’s keep moving forward. Please provide the remaining details for your route.',
        'Sure, let’s continue. Please provide the details for your route.',
        'Alright, let’s proceed. Please continue by providing the necessary details for your route.',
    ]
    return random.choice(messages)

# main function to run the chatbot
def main():

    # assign to the variable save_directory the path to the model, given by the user in the command line
    if len(sys.argv) < 2:
        print("Please provide the path to the model directory as an argument. The model can be downloaded via the following link: https://drive.google")
        return
    save_directory = sys.argv[1]
    # save_directory = r"C:\tools\nlp_bot\gug_s_best_model_custom_seq2seq_model_with_T5"  # davids dir
    # save_directory = r"C:\Users\ronav\Downloads\gug_s_best_model_custom_seq2seq_model_with_T5"    # rons dir

    tracker = Tracker()
    policy = Policy(tracker)
    bio_tagger = Bio_Tagger("../street_scraping/final_streets.txt")
    generator = NlgModel(save_directory, save_directory)

    pretty_print(botName, f"{generate_starting_message()}", "green")

    # Simulate chatbot flow##
    done = False
    next_slot = None
    user_round = 0
    max_rounds = 20  # Max rounds before asking to continue

    while not done:
        try:
            # Get user input
            user_input = input(f"\033[35m{userName}").strip()
            user_round += 1

            # Check if user wants to continue
            if user_round > max_rounds:
                if wantToContinue():
                    user_round = 0
                    next_slot = None
                    pretty_print(botName, f"{generate_continue_message()}", "blue")
                else:
                    pretty_print(botName, f"{generate_ending_message()}", "green")
                    return
                
            # Process user input with the bio tagger
            tagged_input = bio_tagger.tag_bio(user_input, next_slot)
            tracker.update(tagged_input)

            # Get the bot's next action and response
            msg, done, next_slot = policy.next_action(done)

            if not done:
                nlg_msg = generator.respond_to_input(user_input) + " " + msg
            else:
                nlg_msg = msg

            pretty_print(botName, f"{nlg_msg}", "blue")

            # make sure user is satisfied with the route
            if done:
                if not isSatisfied(done):
                    done = False
                    next_slot = None
                    pretty_print(botName, f"{generate_continue_message()}", "blue")
                else:
                    pretty_print(botName, f"{generate_happy_ending_message()}", "green")
                    return

        except Exception as e:
            pretty_print("Got an Error: " + str(e), "red")
            pretty_print(botName, f"{generate_ending_message()}", "green")
            return

# -------------------------------------------------
main()