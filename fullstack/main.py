from tracker import Tracker
from policy import Policy
from bio_tagger import Bio_Tagger
import random

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
        if user_round > 20:
            for _ in range(3):
                print("Bot:", generate_ending_message())
            return

# -------------------------------------------------
main()