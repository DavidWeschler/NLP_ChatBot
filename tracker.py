class Tracker:
    def __init__(self):
        """
        Initialize the Tracker with predefined slots.
        """
        self.slots = {
            "route_length": None,
            "difficulty": None,
            "start_location": None,
            "end_location": None,
            "loca_end_num": None,
            "loca_start_num": None,
        }

    def update_slots(self, bio_tags):
        """
        Update the slots based on BIO tags.
        
        Args:
            bio_tags (list of tuples): List of (value, tag) tuples where tag is in BIO format.
        
        Returns:
            dict: Updated slots.
        """
        # first update all the B- tags
        for val, tag in bio_tags:
            if tag.startswith("B-"):
                slot = tag.split("-")[1]    # e.g: route_length
                self.slots[slot] = val

        # then add all the I-tags
        for val, tag in bio_tags:
            if tag.startswith("I-"):
                slot = tag.split("-")[1]    # e.g: start_location
                if self.slots[slot] is not None:
                    self.slots[slot] += " " + val
                else:
                    self.slots[slot] = val

        return self.slots

    def update(self, bio_tags):
        self.slots = self.update_slots(bio_tags)
    
    def is_complete(self):
        """
        Check if all slots are filled.
        
        Returns:
            bool: True if all slots are filled, False otherwise.
        """
        return all(value is not None for value in self.slots.values())
    
    def missing_slots(self):
        """
        Get a list of slots that are not filled.
        
        Returns:
            list: List of slot names that are not filled.
        """
        return [slot for slot, value in self.slots.items() if value is None]
    
    def print_slots(self):
        """
        Print the current state of all slots, used for debbuging.
        """
        for slot, value in self.slots.items():
            print(f"{slot}: {value}", end=", ")
            print('')