# Purpose
Input text string with gendered pronouns and output same text replacing with the non-gendered pronouns "they/them" with proper grammar. 

|Function|He set|She set|Replace with|
|---|---|---|---|
|Subject|he|she|they|
|Object|him|her|them|
|Possessive adjective|his|her|their|
|Possessive noun|his|hers|theirs|
|Reflexive|himself|herself|themselves|
## Challenges

**1. "His" — adjective or noun?**

- _That's his dog_ → possessive adjective → _their dog_
- _That dog is his_ → possessive noun → _that dog is theirs_

The rule: if _his_ is followed by a noun (or noun phrase), it's an adjective. If it's at the end of a clause or followed by a verb/punctuation, it's a standalone noun.

**2. "Her" — object or adjective?**

- _I called her_ → object → _I called them_
- _Her dog ran away_ → possessive adjective → _Their dog ran away_

The rule: _her_ followed by a noun = possessive adjective. _Her_ following a verb (with no noun after it in the same phrase) = object pronoun.

**3. Capitalization**  
_He/She/His/Her_ at the start of a sentence are still pronouns — don't let the capital fool your parser into missing them. The replacement needs to preserve sentence-initial capitalization: _He left_ → _They left_, not _they left_.

## Approaches

Use a **part-of-speech tagger.** For this project, the spaCy library made the most sense. The workflow looks like so:

 - Input text with gendered pronouns.
 - Module spaCy runs through the whole text and find tokens that are pronouns.
 - Loop through whole text.
 - If word is not a pronoun, append to final output and continue...
 - If non-gendered pronoun is found, to final output and continue...
 - If gendered pronoun is found:
	 - look up its function
	 - replace with correct variable from substitution map
	 - append new pronoun to final output and continue...
-  If end of word list, return final output.

### Pseudocode

```
IMPORT spacy
LOAD spacy english model into nlp

SUBSTITUTION MAP = {
    "he": "they",
    "him": "them",
    "his": "their",        # possessive adjective
    "his (noun)": "theirs", # possessive noun
    "hers": "theirs",
    "she": "they",
    "her": "them",         # object
    "her (adj)": "their",  # possessive adjective
    "himself": "themselves",
    "herself": "themselves"
}

FUNCTION replace_pronouns(text):
    RUN nlp on text → gives you doc (list of tokens)
    
    result = empty list
    
    FOR each token in doc:
        word = token.text
        lowered = word.lowercased
        
        IF token is NOT a pronoun:
            APPEND word to result
            CONTINUE

        IF lowered is "his":
            IF token's dependency tag is possessive:
                replacement = "their"
            ELSE:
                replacement = "theirs"

        ELSE IF lowered is "her":
            IF token's part of speech is possessive:
                replacement = "their"
            ELSE:
                replacement = "them"

        ELSE IF lowered is in SUBSTITUTION MAP:
            replacement = SUBSTITUTION MAP[lowered]

        ELSE:
            replacement = word  # not a gendered pronoun, leave it

        IF word was capitalized:
            replacement = capitalize replacement

        APPEND replacement to result

    RETURN result joined as a string with spaces
```
