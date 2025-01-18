from tracker import Tracker
from policy import Policy
import random


def main():
    # Initialize tracker and policy
    tracker = Tracker()
    policy = Policy(tracker)

    # Example BIO-tagged inputs
    bio_inputs = [
        [("ending", "O"), ("at", "O"), ("location", "O"), ("2", "O")],
        [("I", "O"), ("want", "O"), ("an", "O"), ("easy", "B-difficulty"), ("5km", "B-route_length")],
        [("starting", "O"), ("at", "O"), ("Central", "B-start_location"), ("Park", "I-start_location"), ("1", "I-loca_start_num")],
        [("ending", "O"), ("at", "O"), ("the", "O"), ("Empire", "B-end_location"), ("State", "I-end_location"), ("Building", "I-end_location")],
        [("ending", "O"), ("at", "O"), ("location", "B-loca_end_num"), ("2", "I-loca_end_num")],
    ]

    # Simulate chatbot flow
    done = False
    user_round = 0
    print("Bot:", "Welcome the R&D route planner bot!. I can help you plan a route for your next run. Let's get started!")
    while not done:
        # here we should read the user input and convert it to BIO tags, using the NLU model
        user_input = bio_inputs[random.randint(0, len(bio_inputs) - 1)]
        # user_input = eval(input("User: "))
        # bio_tags = get_taggs(user_input)
        tracker.update(user_input)
        msg, isDone = policy.next_action(done)
        print("Bot:", msg)
        user_round += 1
        if isDone:
            return
        if user_round > 5:
            print("Bot:", "I'm sorry, I'm having trouble understanding you. I'll try to generate a route based on what i have.")
            return

# -------------------------------------------------
main()