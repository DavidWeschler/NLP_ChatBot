import re
import string
import spacy

class Bio_Tagger:
    def __init__(self, streets_file_path):
        self.difficulty_keywords = {
            "easy",
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

            # Immediate vicinity phrases
            "near you",
            "around you",
            "around here",
            "this area",
            "this neighborhood",
            "your vicinity",
            "nearby",
            "in this area",
            "from where you are",

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
        regex_pattern = r'\b(?:to|from|near|at|on|in)\s((?:[a-z]+\s)*(?:\d+)|(?=\s\b(?:to|from|near|at|on|in|and)\b))'
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
        sentence = re.sub(r'\bfrom here\b', "from where you are", sentence)
        sentence = re.sub(r'\bto here\b', "to where you are", sentence)
        sentence = re.sub(r'\bwant to\b', "want", sentence)
        sentence = re.sub(r'\bto run\b', "run", sentence)
        sentence = re.sub(r'\bto explore\b', "explore", sentence)
        sentence = re.sub(r'\bto generate\b', "generate", sentence)
        sentence = re.sub(r'\bto make\b', "make", sentence)
        sentence = re.sub(r'\bto recive\b', "recive", sentence)
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
            # sentence, tokens = self.preprocess_sentence(sentence) ASK RON
            sentence = self.preprocess_sentence(sentence)
            return sucssus, sentence, bio_tags

        sucssus, _, bio_tags = self.fill_locations(1, sentence, bio_tags)
        location, _ = self.curr_location(sentence)
        if location:
            sentence = " ".join(sentence.split())
            if sucssus or any(phrase+" "+location in sentence for phrase in ["ending at", "finishing at", "ends at", "finishes at", "to", "ending"]):
                bio_tags = self.append_to_end_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            elif any(phrase+" "+location in sentence for phrase in ["starting at", "begin at", "start at", "beginning at", "from", "starting"]) and not bio_tags['B-start_location']:
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
            if sucssus or any(phrase+" "+location in sentence for phrase in ["starting at", "begin at", "start at", "beginning at", "from", "starting"]):
                bio_tags = self.append_to_start_location(location, bio_tags)
                sentence = sentence.replace(location, "")
                sucssus = True
            elif any(phrase+" "+location in sentence for phrase in ["ending at", "finishing at", "ends at", "finishes at", "to", "ending"]) and not bio_tags['B-end_location']:
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
                    if(i>0 and i<len(s)-1):
                        if (word in["from", "starting"] or " ".join(s[i-1:i+1]) in ["starting at", "begin at", "beginning at", "start at", "starts at", "begins at"]) and " ".join(s[i + 1:]).startswith(st) and not bio_tags['B-start_location']:
                            start_sucssus = True
                            bio_tags = self.append_to_start_location(st, bio_tags)
                            to_remove.append(st.split())
                        elif (word in["to", "ending"] or " ".join(s[i-1:i+1]) in ["ending at", "finishing at", "ends at", "finishes at", "end at"]) and " ".join(s[i + 1:]).startswith(st) and not bio_tags['B-end_location']:
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
        print("Focus: ", focus)
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

        print("Bio tags: ", self.format_bio_tags(bio_tags))
        return self.format_bio_tags(bio_tags)