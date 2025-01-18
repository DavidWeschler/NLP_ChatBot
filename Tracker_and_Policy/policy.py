import random

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
                return self.conclude(done), done
            
            # Focus on the first missing slot
            slot_to_fill = missing[0]
            return self.ask_question(slot_to_fill), done
        else:
            done = True
            return self.conclude(done), done

    def ask_question(self, slot):
        """
        Generate a question to ask the user for the specific slot.
        
        Args:
        - slot: The slot name that needs to be filled.
        
        Returns:
        - A string question.
        """
        questions = {
            "difficulty": "What difficulty level do you prefer? (e.g., easy, medium, hard)",
            "route_length": "How long should the route be? (e.g., 5km, 10km)",
            "start_location": "Where do you want to start?",
            "end_location": "Where should the route end?",
            "loca_end_num": "What is the end location number?",
            "loca_start_num": "What is the start location number?",
        }
        return questions.get(slot, "Could you provide more details?")

    def conclude(self, done):
        """
        Generate a conclusion or confirmation message when all slots are filled.
        
        Returns:
        - A string message confirming the details.
        """
        filled_slots = self.tracker.slots
        filled_slots = {k: (v if v is not None else "") for k, v in filled_slots.items()}   # Replace 'None' with empty string
        possible_final_messages = [ 
            f"Greate! iI'll build you a {filled_slots['route_length']} {filled_slots['difficulty']} route from {filled_slots['start_location']} {filled_slots['loca_start_num']} to {filled_slots['end_location']} {filled_slots['loca_end_num'] or ""}. Goodbye!",
            f"Alright! I'll plan a {filled_slots['route_length']} {filled_slots['difficulty']} route starting at {filled_slots['start_location']} {filled_slots['loca_start_num']} and ending at {filled_slots['end_location']} {filled_slots['loca_end_num']}. I'll show you the map now.",
            f"Got it! I'll create a {filled_slots['route_length']} {filled_slots['difficulty']} route from {filled_slots['start_location']} {filled_slots['loca_start_num']} to {filled_slots['end_location']} {filled_slots['loca_end_num']}. See you later!",
        ]

        return possible_final_messages[random.randint(0, len(possible_final_messages) - 1)]
