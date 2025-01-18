class Tracker:
    def __init__(self):
        self.slots = {
            "route_length": None,
            "difficulty": None,
            "start_location": None,
            "end_location": None,
            "loca_end_num": None,
            "loca_start_num": None,
        }

    @staticmethod
    def update_slots(bio_tags, slots):
        slot_values = {slot: [] for slot in slots.keys()}
        
        for word, tag in bio_tags:
            if tag.startswith("B-"):
                current_slot = tag[2:]  # Extract slot name from "B-slot_name"
                if current_slot in slot_values:
                    slot_values[current_slot].append(word)
            elif tag.startswith("I-") and current_slot:
                slot_values[current_slot].append(word)
            else:
                current_slot = None
        
        # Join words and update slots
        for slot, words in slot_values.items():
            if words:
                slots[slot] = " ".join(words)
        
        return slots

    def update(self, bio_tags):
        self.slots = self.update_slots(bio_tags, self.slots)
    
    def is_complete(self):
        return all(value is not None for value in self.slots.values())
    
    def missing_slots(self):
        return [slot for slot, value in self.slots.items() if value is None]