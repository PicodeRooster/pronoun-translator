import sys
import spacy

nlp = spacy.load("en_core_web_sm")

def user_input():
    print("Enter text. Type 'END' on a new line to finish:")
    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    text_input = "\n".join(lines)
    return text_input

try: 
    sys.argv[1]
    text = sys.argv[1]
except IndexError:
    text = user_input()

PRONOUNS = {
    "he": "they",   "she": "they",
    "him": "them",
    "himself": "themselves", "herself": "themselves",
    "hers": "theirs",    
}

def neutralize(token):
    word = token.text.lower()
    if word in PRONOUNS:
        return PRONOUNS[word]
    if word == "his":
        return "their" if token.tag_ == "PRP$" else "theirs"
    if word == "her":
        return "their" if token.tag_ == "PRP$" else "them"
    return None

doc = nlp(text)
filtered_text = list()

for token in doc:
    pronoun = neutralize(token)
    if pronoun is None:
        filtered_text.append(token.text + token.whitespace_)
    else:
        if token.text[0].isupper():
            pronoun = pronoun.capitalize()
        filtered_text.append(pronoun + token.whitespace_)

print("".join(filtered_text))