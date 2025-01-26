import re
import string

class Bio_Tagger:
    def __init__(self, streets_file_path):
        self.streets = self.load_streets(streets_file_path)
        self.start_location_keywords = {
            "from"
            #,"at"
        }
        self.end_location_keywords = {
            "to",
            "at"
        }
        self.difficulty_keywords = {
            "easy",
            "moderate",
            "hard",
            "beginner",
            "intermediate",
            "advanced",
            "medium",
            "mediumlevel",
            "med",
            "light",
            "heavy",
            "simple",
            "basic",
            "challenging",
            "difficult",
            "entrylevel",
            "novice",
            "expert",
            "strenuous",
            "elementary",
            "complex",
            "very",
            "difficult",
        }

        self.in_start_location = False
        self.in_end_location = False
        self.in_difficulty = False
        self.digit_found = False

    def a_func(self, lst_a, lst_b):
        for word in lst_a:
            if word in lst_b:
                return True
        return False

    def load_streets(self, file_path):
        with open(file_path, 'r') as file:
            streets = [name.strip().replace("'", "") for name in file.read().splitlines()]
        return streets

    def preprocess_sentence(self, sentence):
        lower_streets = [street.lower() for street in self.streets]

        sentence = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', sentence)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        # Convert to lowercase
        sentence = sentence.lower()

        sentence = re.sub(r'\bmy\b', "your", sentence)
        # sentence = re.sub(r'\bi am\b', "you are", sentence)

        # Remove punctuation
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))

        # Tokenize the sentence
        tokens = sentence.split()
        i = 0
        while i < len(tokens):
            for length in range(1, len(tokens) - i + 1):  # Check word combinations of length 1 to len(sentence)
                word_sequence = ' '.join(tokens[i:i+length])
                if word_sequence in lower_streets:  # If the sequence is found in streets
                    tokens[i:i+length] = [word_sequence]  # Merge the sequence into one token
                    i += length - 1  # Skip over the words that have been merged
                    break
            i += 1  # Continue to the next token

        # Remove empty tokens
        tokens = [token for token in tokens if token]
        return tokens
    
    def ends_with_sentence(self, tokens, bio_tags):
        sentence_ends = [
                {"phrase": "bro", "word_count": 1},
                {"phrase": "bruh", "word_count": 1},
                {"phrase": "your man", "word_count": 2},
                {"phrase": "your sister", "word_count": 2},
                {"phrase": "your brother", "word_count": 2},
                {"phrase": "plz", "word_count": 1},
                {"phrase": "thx", "word_count": 1},
                {"phrase": "please", "word_count": 1},
                {"phrase": "thanks", "word_count": 1},
                {"phrase": "thank you", "word_count": 2},
                {"phrase": "if you could", "word_count": 3},
                {"phrase": "if you dont mind", "word_count": 4},
                {"phrase": "when you get a chance", "word_count": 5},
                {"phrase": "at your earliest convenience", "word_count": 4},
                {"phrase": "id appreciate it", "word_count": 3},
                {"phrase": "if possible", "word_count": 2},
                {"phrase": "kindly", "word_count": 1},
                {"phrase": "if you would", "word_count": 3},
                {"phrase": "much appreciated", "word_count": 2},
                {"phrase": "looking forward to it", "word_count": 4},
                {"phrase": "whenever you can", "word_count": 3},
                {"phrase": "id be grateful", "word_count": 3}
            ]

        for entry in sentence_ends:
            phrase = entry["phrase"].lower().split()  # Convert phrase to lowercase and split into tokens
            word_count = entry["word_count"]

            # Check if the last `word_count` tokens of the sentence match the phrase
            if len(tokens) >= word_count and tokens[-word_count:] == phrase:
                # Mark those tokens as 'O' in the bio_tags
                for i in range(word_count):
                    bio_tags['O'].append(tokens[-word_count + i])

                # Shorten the tokens list by removing the marked tokens
                tokens = tokens[:-word_count]
                return tokens, bio_tags

        # If no phrase is matched, return the original tokens and bio_tags
        return tokens, bio_tags

    def format_bio_tags(self, bio_tags):
        formatted_tags = []
        for tag, words in bio_tags.items():
            for word in words:
                formatted_tags.append((word, tag))
        return formatted_tags


    def tag_bio(self, sentence, next_slot):
        # Initialize the dictionary to store BIO tags
        bio_tags = {
            'B-loca_start_num': [],
            'I-start_location': [],
            'B-end_location': [],
            'I-difficulty': [],
            'B-route_length': [],
            'B-start_location': [],
            'I-route_length': [],
            'B-loca_end_num': [],
            'I-end_location': [],
            'B-difficulty': [],
            'O': []
        }
        tokens = self.preprocess_sentence(sentence)
        tokens, bio_tags = self.ends_with_sentence(tokens, bio_tags)

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Rule for B-loca_start_num: numeric token at the start of a location
            if token.isdigit():
                if i+1 < len(tokens) and tokens[i+1] in ["km", "kilometers", "meters", "miles", "k"]:
                    bio_tags['B-route_length'].append(token)
                elif not self.digit_found and not self.a_func(tokens[:i], self.end_location_keywords):
                    bio_tags['B-loca_start_num'].append(token)
                    self.digit_found = True
                else:
                    bio_tags['B-loca_end_num'].append(token)

            elif "and" == token:
             bio_tags['O'].append(token)

            elif i+1 < len(tokens) and token == "to" and tokens[i+1] not in [street.lower() for street in self.streets]:
                bio_tags['O'].append(token)
                bio_tags['O'].append(tokens[i+1])
                i += 1
            
            elif i+1 < len(tokens) and token == "to" and tokens[i+1] in [street.lower() for street in self.streets]:
                bio_tags['O'].append(token)
                bio_tags['B-end_location'].append(tokens[i+1])
                i += 1

            elif token in self.difficulty_keywords and not self.in_difficulty and not bio_tags['B-difficulty']:
                bio_tags['B-difficulty'].append(token)
                self.in_difficulty = True

            elif token in self.difficulty_keywords and self.in_difficulty and bio_tags['B-difficulty'] and tokens[i-1] in bio_tags['B-difficulty']+bio_tags['I-difficulty']:
                bio_tags['I-difficulty'].append(token)

            # Rule for B-start_location: first token in a location
            elif (re.match(r"^[a-z]+(?: [a-z]+)*$", token) and token in self.streets) or i-1 >= 0 and re.match(r"^[a-z]+(?: [a-z]+)*$", token) and tokens[i-1] in self.start_location_keywords and not self.in_start_location and not bio_tags['B-start_location'] or (i-2>=0 and tokens[i-2] == "starting" and tokens[i-1] == "at"):
                bio_tags['B-start_location'].append(token)
                self.in_start_location = True

            # Rule for I-start_location: subsequent tokens in the location name
            elif i - 1 >= 0 and self.in_start_location and re.match(r"^[a-z]+$", token) and not re.match(r"^[a-z] +$", tokens[i-1]) and tokens[i-1] in bio_tags['B-start_location']+bio_tags['I-start_location'] and token not in set(list(self.start_location_keywords)+list(self.end_location_keywords)):
                bio_tags['I-start_location'].append(token)

            # Rule for B-end_location: first token after 'to' or 'at'
            elif (re.match(r"^[a-z]+(?: [a-z]+)*$", token) and token in self.streets) or i - 1 >= 0 and re.match(r"^[a-z]+(?: [a-z]+)*$", token) and tokens[i-1] in self.end_location_keywords and not self.in_end_location and not bio_tags['B-end_location'] or (i-2>=0 and tokens[i-2] == "ending" and tokens[i-1] == "at"):
                bio_tags['B-end_location'].append(token)
                self.in_end_location = True

            # Rule for I-end_location: subsequent tokens in the location name
            elif i - 1 >= 0 and self.in_end_location and re.match(r"^[a-z]+$", token) and not re.match(r"^[a-z] +$", tokens[i-1]) and tokens[i-1] in bio_tags['B-end_location']+bio_tags['I-end_location'] and token not in set(list(self.start_location_keywords)+list(self.end_location_keywords)):
                bio_tags['I-end_location'].append(token)

            # Rule for O: any token not matching other tags
            else:
                bio_tags['O'].append(token)

            i += 1

        return self.format_bio_tags(bio_tags)






# sentences = [
#     "I would like to run 5 km starting from my current location to hanevim 7 and make it very difficult.",
#     "from my current location",
#     "Show me a running path from downtown to ekrmh ben avi ghl",
#     "i want to generate a route. 10 km long, starting from my location and very hard. should end at haneviim 37. lets go!",
#     "I want to go for a 3km easy run starting from Edsh Shafik to Eko eko",
#     "Plan a moderate difficulty route from my house to Elr that's about 7km",
#     "Need a challenging 10km loop beginning from Elr",
#     "Create a beginner-friendly 2km route starting from the train station",
#     "I'd like to run from the coffee shop to the library, make it hard",
#     "Plan a 5k route departing from the community center"
#     # "Looking for an intermediate trail run starting at the forest entrance to the lake",
#     # "Map out an advanced 8km path from my office to the park",
#     # "Need a running route from the school to the sports complex, around 4km",
#     # "Create a strenuous route beginning at the plaza ending at the hill viewpoint",
#     # "Show me an easy running path that starts and ends at the mall",
# ]