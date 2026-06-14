import spacy

nlp = spacy.load("en_core_web_sm")
text = "Sarah grabbed her coat and called out to him before he could leave. The dog was hers, after all, and she wasn't about to let himself — or rather, David — walk out with it. She tucked his leash into her bag and told herself that his stubbornness wasn't worth fighting today."

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