from tracker import Tracker
from policy import Policy
from bio_tagger_ron import Bio_Tagger
import random


def wantToStartOver():
    startOverUser = ["yes", "y", "yeah", "sure", "ok", "okay", "yup", "yea", "ya", "yep", "of course", "indeed", "absolutely", "definitely", "please", "start over", "try again", "restart", "reset"]
    messages = [
        "I seem to be having trouble understanding you. Would you like to start over?",
        "Apologies, I’m having difficulty following. Do you want to start over?",
        "I seem to be having trouble understanding you. Do you want to try again?",
        "Apologies, I’m having difficulty following. Would you like to try again?",
        "I seem to be having trouble understanding you. Do you want to restart?",
        "Apologies, I’m having difficulty following. Would you like to restart?",
        "I may not have understood completely. Do you want to reset?",
        "I may not have understood completely. Would you like to reset?"
    ]
    print("Bot: ", random.choice(messages))
    user_input = input("User: ")
    if user_input.lower() in startOverUser:
        return True
    else:
        for inp in startOverUser:
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

def prepare_slot(slot):
    if slot == None:
        return "all"
    if slot == "route_length":
        return "route_length"
    elif slot == "difficulty":
        return "difficulty_lvl"
    elif slot == "start_location":
        return "start_loc"
    elif slot == "end_location":
        return "end_loc"
    return slot

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
    print("Bot:", "Welcome the R&D route planner bot!. I can help you plan a route for your next run. Let's get started!")
    while not done:
        try:
            next_slot = prepare_slot(next_slot)
            print("Next slot to fill:", next_slot)
            user_input = input("User: ")
            user_input = bio_tagger.tag_bio(user_input, next_slot)
            tracker.update(user_input)
            msg, isDone, next_slot = policy.next_action(done)
            nlg_msg = "" + msg # get from guy here
            print("Bot:", nlg_msg)
            user_round += 1
            if isDone:
                return
            if user_round > 10:
                if wantToStartOver():
                    tracker = Tracker()
                    policy = Policy(tracker)
                    user_round = 0
                    next_slot = None
                    print("Bot: ", generate_starting_message())
                else:
                    print("Bot: ", generate_ending_message())
                    return
        except Exception as e:
            print("Got an Error: ", e)
            print("Bot: ", "I'm sorry, I seem to be having trouble understanding you. Let me try to generate a route with the details I have so far.")
            print("Bot: ", generate_ending_message())
            return

# -------------------------------------------------
main()

# def generate_starting_message():