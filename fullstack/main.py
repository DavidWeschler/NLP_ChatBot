from tracker import Tracker
from policy import Policy
from bio_tagger import Bio_Tagger
import random

def main():
    # Initialize tracker and policy
    tracker = Tracker()
    policy = Policy(tracker)
    bio_tagger = Bio_Tagger("../street_scraping/final_streets.txt")

    # Example BIO-tagged inputs
    # bio_inputs = [
    #     [("ending", "O"), ("at", "O"), ("location", "O"), ("2", "O")],
    #     [("I", "O"), ("want", "O"), ("an", "O"), ("easy", "B-difficulty"), ("5km", "B-route_length")],
    #     [("starting", "O"), ("at", "O"), ("Central", "B-start_location"), ("Park", "I-start_location"), ("1", "I-loca_start_num")],
    #     [("ending", "O"), ("at", "O"), ("the", "O"), ("Empire", "B-end_location"), ("State", "I-end_location"), ("Building", "I-end_location")],
    #     [("ending", "O"), ("at", "O"), ("location", "B-loca_end_num"), ("2", "I-loca_end_num")],
    # ]

    # Simulate chatbot flow
    done = False
    user_round = 0
    print("Bot:", "Welcome the R&D route planner bot!. I can help you plan a route for your next run. Let's get started!")
    while not done:
        user_input = input("User: ")
        user_input = bio_tagger.tag_bio(user_input)
        tracker.update(user_input)
        msg, isDone = policy.next_action(done)
        print("Bot:", msg)
        user_round += 1
        if isDone:
            return
        if user_round > 10:
            print("Bot:", "I'm sorry, I'm having trouble understanding you. I'll try to generate a route based on what i have.")
            return

# -------------------------------------------------
main()





# For Ron:
# def format_bio_tags(input_dict):
#     bio_tags = []    
#     for tag, words in input_dict.items():
#         for word in words:
#             bio_tags.append((word, tag))
#     return bio_tags