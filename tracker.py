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

    def update_slots(self, bio_tags):
        # example bio tags: Bio tags: [(4, 'B-route_length'), ('hi', 'O'), ('ther', 'O'), ('plan', 'O'), ('you', 'O'), ('a', 'O'), ('4', 'O'), ('k', 'O'), ('running', 'O'), ('route', 'O')]
        
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
        return all(value is not None for value in self.slots.values())
    
    def missing_slots(self):
        return [slot for slot, value in self.slots.items() if value is None]
    
    def print_slots(self):
        for slot, value in self.slots.items():
            print(f"{slot}: {value}", end=", ")
            print('')