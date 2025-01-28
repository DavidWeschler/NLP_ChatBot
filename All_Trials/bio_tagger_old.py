import re
import string
import spacy
import time
import random

def suprise_func(
    text,
    base_speed=0.035,
    speed_variation=0.005,
    punctuation_pause=0.6,
    word_pause_multiplier=0.3,
    sentence_pause=0.6,
    thinking_pause=0.7,
    flush=True
):
    punctuation = {',', ';', ':', '!', '?', '...', '(', ')'}
    sentences = re.split(r'(?<=\. )', text)

    for sentence in sentences:
        if random.random() < 0.1:
            time.sleep(thinking_pause)

        for char in sentence:
            print(char, end='', flush=flush)
            if char in punctuation:
                time.sleep(punctuation_pause + random.uniform(0, speed_variation))
            elif char == ' ':
                time.sleep(base_speed * word_pause_multiplier + random.uniform(0, speed_variation / 2))
            else:
                time.sleep(base_speed)

        time.sleep(sentence_pause + random.uniform(0, speed_variation))

    print()

def pretty_print(message, color):
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    color_code = colors.get(color.lower(), colors["reset"])

    # Print the message with the selected color
    suprise_func(f"{color_code}{message}{colors['reset']}")

class Bio_Tagger:
    def __init__(self, streets_file_path):
        self.difficulty_keywords = {
            "easy",
            "medium",
            "moderate",
            "hard",
            "beginner",
            "intermediate",
            "advanced",
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
            "difficult"
        }

        self.location_phrases = [
            # Current location phrases
            "your current location",
            "your location",
            "where you are",
            "where you are now",
            "your position",
            "current position",
            "right here",
            "this spot",
            "this location",
            "your present location",
            "current place",
            "this place",
            "where you are standing",
            "where you are at",
            "where you currently are",

            # Immediate vicinity phrases
            "near you",
            "around you",
            "around here",
            "this area",
            "this neighborhood",
            "your vicinity",
            "nearby",
            "in this area",
            "your currunt location",

            # GPS related
            "your gps location",
            "your coordinates",
            "your exact location",
            "your current coordinates",
            "your exact position",

            # Colloquial
            "where you are located",
            "your current spot",
            "this point",
            "your whereabouts",
            "current whereabouts",
            "present position",
            "right where you are",
            "this current location"
        ]

    def format_bio_tags(self, bio_tags):
        formatted_tags = []
        for tag, words in bio_tags.items():
            for word in words:
                formatted_tags.append((word, tag))
        return formatted_tags
    
    def print_bio_tags(self, bio_tags):
        for key, value in bio_tags.items():
            if value:
                print(f"{key}: {value}")

    def update_phrase_list(self, sentence, phrase_list):
        res=phrase_list
        sentence_words = sentence.split()
        n=[]
        for p in phrase_list:
            l=p.split()
            n+=l

        comp=[]
        for word in sentence_words:
            if sentence_words.count(word) < n.count(word):
                for l in phrase_list:
                    if l.startswith(word):
                        comp.append(l)
                if comp:
                    res.remove(min(comp, key=len))
                    comp=[]

        return res
    
    def extract_street_names(self, sentence):
        nlp = spacy.load("en_core_web_sm")
        stopwords = {"to", "from", "near", "at", "on", "in", "and"}
        regex_pattern = r'\b(?:to|from|near|at|on|in)\s((?:[a-z]+\s)*(?:\d+|street|neighborhood|avenue|district|st)|(?=\s\b(?:to|from|near|at|on|in|and)\b))'
        regex_matches = re.findall(regex_pattern, sentence)

        refined_matches = []
        for match in regex_matches:
            words = match.strip().split()
            stopword_indices = [i for i, word in enumerate(words) if word.lower() in stopwords]
            if stopword_indices:
                refined_words = []
                start_idx = 0
                for idx in stopword_indices:
                    refined_words.append(' '.join(words[start_idx:idx]))
                    start_idx = idx + 1

                refined_words.append(' '.join(words[start_idx:]))
                refined_matches = refined_words
            else:
                refined_matches.append(match.strip())

        doc = nlp(sentence)
        ner_matches = [ent.text for ent in doc.ents if ent.label_ in {"LOC", "GPE", "FAC"}]

        lst = self.update_phrase_list(sentence, list(set(refined_matches + ner_matches)))
        return lst
    
    def preprocess_sentence(self, sentence):
        sentence = sentence.lower()
        sentence = re.sub(r'\bmy\b', "your", sentence)
        sentence = re.sub(r'\bi am\b', "you are", sentence)
        sentence = re.sub(r'\bim\b', "you are", sentence)
        sentence = re.sub(r'\bi\b', "you", sentence)
        sentence = re.sub(r'\bme\b', "you", sentence)
        sentence = re.sub(r'\bam\b', "are", sentence)
        # sentence = re.sub(r'\bfrom here\b', "from where you are", sentence)
        # sentence = re.sub(r'\bto here\b', "to where you are", sentence)
        # sentence = re.sub(r'\bend here\b', "to where you are", sentence)
        sentence = re.sub(r'\bhere\b', "where you are", sentence) ################
        sentence = re.sub(r'\bwant to\b', "want", sentence)
        sentence = re.sub(r'\bto run\b', "run", sentence)
        sentence = re.sub(r'\bto explore\b', "explore", sentence)
        sentence = re.sub(r'\bto generate\b', "generate", sentence)
        sentence = re.sub(r'\bto make\b', "make", sentence)
        sentence = re.sub(r'\bto recive\b', "recive", sentence)
        sentence = re.sub(r'\blike to\b', "like", sentence)
        sentence = sentence.replace(" and ", " ")
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        sentence = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', sentence)
        sentence = re.sub(r'(\d+)(\.\s)', r'\1 ', sentence)
        sentence = sentence.replace("\'", "")
        chars_to_replace = "-—–,;:!?'\"()[]{}@#$%^&*_+/|<>\\"
        sentence = sentence.translate(str.maketrans(chars_to_replace, ' ' * len(chars_to_replace)))
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation.replace('.', '')))

        return sentence

    def fill_difficulty(self, sentence, bio_tags):
        sucssus=False
        sentence_1=sentence
        tokens = sentence.replace('.', '').split()
        bio_tags['B-difficulty']=[]
        bio_tags['I-difficulty']=[]
        for i, token in enumerate(tokens):
            if token in self.difficulty_keywords and not sucssus:
                sucssus=True
                bio_tags['B-difficulty'].append(token)
            elif token in self.difficulty_keywords and sucssus:
                bio_tags['I-difficulty'].append(token)
        
        if "very" in bio_tags['B-difficulty'] and not bio_tags['I-difficulty']:
            bio_tags['B-difficulty']=[]
            bio_tags['I-difficulty']=[]
        else:
            for word in bio_tags['B-difficulty']+bio_tags['I-difficulty']:
                sentence = sentence_1.replace(word, "")
        return sucssus, sentence, bio_tags

    def append_to_start_location(self, st, bio_tags):
        full_st=st.split()
        if len(full_st) > 0:
            if full_st[-1].isdigit():
                if full_st[-1] in bio_tags['B-loca_start_num'] or full_st[-1] in bio_tags['B-loca_end_num']:
                    return bio_tags
                bio_tags['B-loca_start_num'].append(full_st[-1])
                full_st=full_st[:-1]
            for word in full_st[1:]:
                bio_tags['I-start_location'].append(word)
        bio_tags['B-start_location'].append(full_st[0])
        return bio_tags

    def append_to_end_location(self, st, bio_tags):
        full_st=st.split()
        if len(full_st)>0:
            if full_st[-1].isdigit():
                if full_st[-1] in bio_tags['B-loca_start_num'] or full_st[-1] in bio_tags['B-loca_end_num']:
                    return bio_tags
                bio_tags['B-loca_end_num'].append(full_st[-1])
                full_st=full_st[:-1]
            for word in full_st[1:]:
                bio_tags['I-end_location'].append(word)
        bio_tags['B-end_location'].append(full_st[0])
        return bio_tags

    def fill_start_location(self, sentence, bio_tags):
        sucssus=False
        bio_tags['B-start_location']=[]
        bio_tags['I-start_location']=[]
        bio_tags['B-loca_start_num']=[]
        sentence = self.preprocess_sentence(sentence)

        if any(item == sentence for item in self.location_phrases):
            location, _ = self.curr_location(sentence)
            bio_tags = self.append_to_start_location(location, bio_tags)
            sentence = sentence.replace(location, "")
            sucssus=True
            sentence = self.preprocess_sentence(sentence)
            return sucssus, sentence, bio_tags

        sucssus, _, bio_tags = self.fill_locations(1, sentence, bio_tags)
        location, _ = self.curr_location(sentence)
        if location:
            sentence = " ".join(sentence.split())
            if sucssus or any(phrase+" "+location in sentence for phrase in ["ending at", "finishing at", "finish", "ends at", "end at", "finishes at", "finish at", "to", "ending", "end"]):
                bio_tags = self.append_to_end_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            elif any(phrase+" "+location in sentence for phrase in ["starting at", "begin at", "start at", "beginning at", "from", "starting", "start"]) and not bio_tags['B-start_location']: 
                bio_tags = self.append_to_start_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            sentence = self.preprocess_sentence(sentence)
        return sucssus, sentence, bio_tags

    def fill_end_location(self, sentence, bio_tags):
        sucssus=False
        bio_tags['B-end_location']=[]
        bio_tags['I-end_location']=[]
        bio_tags['B-loca_end_num']=[]
        sentence = self.preprocess_sentence(sentence)

        if any(item == sentence for item in self.location_phrases):
            location, _ = self.curr_location(sentence)
            bio_tags = self.append_to_end_location(location, bio_tags)
            sentence = sentence.replace(location, "")
            sucssus = True
            sentence = self.preprocess_sentence(sentence)
            return sucssus, sentence, bio_tags

        _, sucssus, bio_tags = self.fill_locations(0, sentence, bio_tags)
        location, _ = self.curr_location(sentence)
        if location:
            sentence = " ".join(sentence.split())
            if sucssus or any(phrase+" "+location in sentence for phrase in ["starting at", "begin at", "start at", "beginning at", "from", "starting", "start"]):
                bio_tags = self.append_to_start_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            elif any(phrase+" "+location in sentence for phrase in ["ending at", "finish", "finishing at", "ends at", "end at", "finishes at", "finish at", "to", "ending", "end"]) and not bio_tags['B-end_location']: 
                bio_tags = self.append_to_end_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            sentence = self.preprocess_sentence(sentence)
        return sucssus, sentence, bio_tags

    def fill_route_length(self, sentence, bio_tags):
        sucssus = False
        bio_tags['B-route_length']=[]
        tokens = self.preprocess_sentence(sentence).split()
        if sentence.isdigit():
            sucssus = True
            bio_tags['B-route_length'].append(sentence)
        else:
            for i, token in enumerate(tokens):
                if token.isdigit():
                    if i+1 < len(tokens) and tokens[i+1] in ["km", "kilometers", "meters", "miles", "k", "mile"]:
                        sucssus = True
                        bio_tags['B-route_length'].append(int(token))
                elif token.replace('.', '').isdigit():
                    if i+1 < len(tokens) and tokens[i+1] in ["km", "kilometers", "meters", "miles", "k", "mile"]:
                        sucssus = True
                        bio_tags['B-route_length'].append(float(token))
        return sucssus, sentence, bio_tags

    def fill_locations(self, start_end, sentence, bio_tags):
        start_sucssus = False
        end_sucssus = False
        ext_streets = self.extract_street_names(sentence)
        ext_streets = [item for item in ext_streets if not item.isdigit()]

        to_remove=[]
        if ext_streets:
            s= sentence.split()
            for st in ext_streets:
                for i, word in enumerate(s):
                    if(i<len(s)-1):
                        if (word in["from", "starting"] or " ".join(s[i-1:i+1]) in ["starting at", "begin at", "beginning at", "start at", "starts at", "begins at"]) and " ".join(s[i + 1:]).startswith(st) and not bio_tags['B-start_location']:
                            start_sucssus = True
                            bio_tags = self.append_to_start_location(st, bio_tags)
                            to_remove.append(st.split())
                        elif (word in["to", "ending"] or " ".join(s[i-1:i+1]) in ["ending at", "finishing at", "ends at", "finishes at", "finish at", "end at"]) and " ".join(s[i + 1:]).startswith(st) and not bio_tags['B-end_location']:
                            end_sucssus = True
                            bio_tags = self.append_to_end_location(st, bio_tags)
                            to_remove.append(st)

        ext_streets = [item for item in ext_streets if item not in to_remove]

        if ext_streets and (not start_sucssus or end_sucssus):
            if start_end:
                for st in ext_streets:
                    if start_end and not bio_tags['B-start_location'] and re.match(r"[a-z]+\s(?:[a-z]+\s)*\d+", sentence):
                        start_sucssus = True
                        bio_tags = self.append_to_start_location(st, bio_tags)
                    elif not start_end and not bio_tags['B-end_location'] and re.match(r"[a-z]+\s(?:[a-z]+\s)*\d+", sentence):
                        end_sucssus  =True
                        bio_tags = self.append_to_end_location(st, bio_tags)

        return start_sucssus, end_sucssus, bio_tags

    def curr_location(self, sentence):
        for phrase in self.location_phrases:
            if phrase in sentence:
                return phrase, sentence.replace(phrase, "")
        return False, sentence
    

    def complete_rest(self, sentence, bio_tags):
        i = 0
        sentence = self.preprocess_sentence(sentence)
        if not bio_tags['B-route_length']:
            _, sentence, bio_tags = self.fill_route_length(sentence, bio_tags)

        if not bio_tags['B-difficulty']:
            _, sentence, bio_tags = self.fill_difficulty(sentence, bio_tags)

        if not bio_tags['B-start_location']:
            _, sentence, bio_tags = self.fill_start_location(sentence, bio_tags)

        if not bio_tags['B-end_location']:
            _, sentence, bio_tags = self.fill_end_location(sentence, bio_tags)

        tokens = sentence.split()
        for token in tokens:
            if not any(token in values for values in bio_tags.values() if values != bio_tags['O']):
                bio_tags['O'].append(token)

        return False, tokens, bio_tags   

    def tag_bio(self, sentence, focus):
        if focus == None:
            focus = "all"
        # pretty_print(f"Focus: {focus}", "cyan")
        focus_dict = {
            "start_location": self.fill_start_location,
            "end_location": self.fill_end_location,
            "difficulty": self.fill_difficulty,
            "route_length": self.fill_route_length,
        }

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
        sentence = self.preprocess_sentence(sentence)
        if focus in focus_dict:
            _, sentence, bio_tags = focus_dict[focus](sentence, bio_tags)
            _, _, bio_tags = self.complete_rest(sentence, bio_tags)
        elif focus == "all":
            _, _, bio_tags = self.complete_rest(sentence, bio_tags)

        # pretty_print(f"Bio tags: {self.format_bio_tags(bio_tags)}", "magenta")
        return self.format_bio_tags(bio_tags)