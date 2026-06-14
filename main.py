import spacy

nlp = spacy.load("en_core_web_sm")
#text = "Sarah grabbed her coat and called out to him before he could leave. The dog was hers, after all, and she wasn't about to let himself — or rather, David — walk out with it. She tucked his leash into her bag and told herself that his stubbornness wasn't worth fighting today."
text = "them"
doc = nlp(text)

print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)