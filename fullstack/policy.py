import random
import re

class Policy:
    def __init__(self, tracker):
        self.tracker = tracker

    def next_action(self, done):
        """
        Decide the next action based on the state of the tracker.
        
        Returns:
        - A string/question to ask the user.
        """
        missing = self.tracker.missing_slots()
        if missing:
            important_slots = ["start_location", "end_location", "route_length", "difficulty"]
            we_have_enogh_info = all(slot not in missing for slot in important_slots)
            if we_have_enogh_info:
                done = True
                return self.conclude(done), done, None
            
            # Focus on the first missing slot
            slot_to_fill = missing[0]
            return self.ask_question(slot_to_fill), done, slot_to_fill
        else:
            done = True
            return self.conclude(done), done, None

    def ask_question(self, slot):
        """
        Generate a question to ask the user for the specific slot.
        
        Args:
        - slot: The slot name that needs to be filled.
        
        Returns:
        - A string question.
        """
        questions = {
            "difficulty": [
                "What difficulty level do you prefer? (e.g., easy, medium, hard)",
                "Could you specify your preferred difficulty?",
                "What level of challenge suits you best?",
                "Do you prefer an easy, medium, or hard route?",
                "How challenging should the route be for you?",
                "Can you tell me your preferred difficulty level?",
                "Are you looking for a simple or a more challenging route?",
                "What king of route are you looking for, light? intermediate? or expert?",
            ],
            "route_length": [
                "How long should the route be? (e.g., 5km, 10km)",
                "What is your preferred route length?",
                "Can you tell me the distance you want to run?",
                "How many kilometers do you have in mind for the route?",
                "What is the ideal route length for you?",
                "Could you specify the distance you'd like to jog?",
                "What length feels comfortable for this route?",
            ],
            "start_location": [
                "Where do you want to start?",
                "Could you provide your starting address?",
                "What is your preferred start point?",
                "Can you share the location where you’d like to begin?",
                "Where should the route begin?",
                "Which place would you like to use as your starting point?",
                "What’s the name or location of where you want to begin?",
            ],
            "end_location": [
                "Where should the route end?",
                "What is your desired endpoint?",
                "Could you specify where you want the route to stop?",
                "Where do you want to finish the route?",
                "What location would you like to mark as the endpoint?",
                "Where should the journey conclude?",
                "Where do you want the route to lead to?",
            ],
            # were not supposed to ask for these but just in case
            "loca_end_num": [
                "What is the end location number?",
                "Could you tell me the number for the end location?",
                "Please specify the number of the location where the route ends.",
                "Do you know the number assigned to the end location?",
                "Can you provide the end location number?",
                "What number corresponds to your endpoint?",
                "Do you have the number of the location where the route should end?",
            ],
            "loca_start_num": [
                "What is the start location number?",
                "Could you share the number for the starting location?",
                "Please provide the number of the location where the route starts.",
                "What is the number assigned to your starting point?",
                "Can you tell me the start location number?",
                "Do you have a number for where the route begins?",
                "What number corresponds to your starting point?",
            ],
        }

        return random.choice(questions.get(slot, ["Could you provide more details?"]))

    def conclude(self, done):
        """
        Generate a conclusion or confirmation message when all slots are filled.
        
        Returns:
        - A string message confirming the details.
        """
        filled_slots = self.tracker.slots
        filled_slots = {k: (v if v is not None else "") for k, v in filled_slots.items()}   # Replace 'None' with empty string
        possible_final_messages = [ 
            f"Greate! I'll build you a {filled_slots['route_length']} km {filled_slots['difficulty']} route from {filled_slots['start_location']} {filled_slots['loca_start_num']} to {filled_slots['end_location']} {filled_slots['loca_end_num'] or ""}. Goodbye!",
            f"Alright! I'll plan a {filled_slots['route_length']} km {filled_slots['difficulty']} route starting at {filled_slots['start_location']} {filled_slots['loca_start_num']} and ending at {filled_slots['end_location']} {filled_slots['loca_end_num']}. I'll show you the map now.",
            f"Got it! I'll create a {filled_slots['route_length']} km {filled_slots['difficulty']} route from {filled_slots['start_location']} {filled_slots['loca_start_num']} to {filled_slots['end_location']} {filled_slots['loca_end_num']}. See you later!",
        ]

        answer = re.sub(r'\s+', ' ', possible_final_messages[random.randint(0, len(possible_final_messages) - 1)]).strip()

        return answer
