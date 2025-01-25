from tracker import Tracker
from policy import Policy
from bio_tagger_ron import Bio_Tagger
import random

def pretty_print(message, color):
    # Define ANSI escape codes for supported colors
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"  # Reset to default
    }

    # Get the color code, default to reset if the color is not recognized
    color_code = colors.get(color.lower(), colors["reset"])

    # Print the message with the selected color
    print(f"{color_code}{message}{colors['reset']}")



def wantToContinue():
    continueUser = ["yes", "y", "yeah", "sure", "ok", "okay", "yup", "yea", "ya", "yep", "of course", "indeed", "absolutely", "definitely", "please", "start over", "try again", "restart", "reset"]
    messages = [
        "I seem to be having trouble understanding you. Do you still want to continue?",
        "Apologies, I’m having difficulty following. Do you want to keep going on?",
        "I seem to be having trouble understanding you. Do you want to keep going?",
        "Apologies, I’m having difficulty following. Would you like to keep on describing your route?",
        "I seem to be having trouble understanding you. Do you still want to continue?",
        "Apologies, I’m having difficulty following. Would you want to keep going on?",
        "I may not have understood completely. Would you like to keep on describing your route?",
    ]
    print("Bot: ", random.choice(messages))
    user_input = input("User: ")
    if user_input.lower() in continueUser:
        return True
    else:
        for inp in continueUser:
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

# main function to run the chatbot
def main():
    # Initialize tracker and policy
    tracker = Tracker()
    policy = Policy(tracker)
    bio_tagger = Bio_Tagger("../street_scraping/final_streets.txt")

    # Simulate chatbot flow
    done = False
    next_slot = None
    user_round = 0
    pretty_print("Bot: Welcome the R&D route planner bot!. I can help you plan a route for your next run. Let's get started!", "green")
    while not done:
        # try:
            user_round += 1
            print("\033[33mYou: ", end="")
            user_input = input()
            user_input = bio_tagger.tag_bio(user_input, next_slot)
            tracker.update(user_input)
            msg, isDone, next_slot = policy.next_action(done)
            nlg_msg = "" + msg # get from guy here
            pretty_print(f"Bot: {nlg_msg}", "blue")
            user_round += 1
            if isDone:
                return
            if user_round > 1:
                if wantToContinue():
                    user_round = 0
                    next_slot = None
                    pretty_print(f"Bot: {generate_starting_message()}", "red")
                else:
                    pretty_print(f"Bot: {generate_ending_message()}", "green")
                    return
        # except Exception as e:
        #     pretty_print("Got an Error: " + str(e), "red")
        #     pretty_print(f"Bot: {generate_ending_message()}", "green")
        #     return

# -------------------------------------------------
main()