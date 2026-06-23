# Pronoun Translator

In the modern age, non-binary gender identity has returned to popularity. I say returned as there is historic evidence of gender non-conforming individuals across multiple cultures. The idea of gender neutrality is not new, but it is re-emerging in society. This is a subject I am well-versed in as a gender non-conforming person myself. I personally believe asking someone gender should be a sign of respect, not controversy. However, I recognize that asking someone's pronouns is still (unfortunately) a politically sensitive topic. To avoid friction on either side of the spectrum, I stick to addressing everyone with gender neutral pronouns until I am certain of the person's preference.

With that being said, English is a gendered language. All English speakers are accostumed to using "he/she" when addressing a person. The brain auto-defaults to one schema - female schemas get filed with "she/her" and males under "he/him." The brain is used to saying or writing "he" and "she" as it has been trained for decades. And the older you are, the harder it is to break out of this habit. This challenge was what inspired me to create this tool. 

Since I want to address all my clients with gender neutral pronouns if I do not confirm their preference, it can be difficult to switch back-and-forth between gendered and neutral pronouns, depending on who I am writing about. This tool is meant to solve that problem. You input any paragraph with gendered pronouns and it will convert those to neutral while doing nothing to the neutral pronouns it finds accross the string.

## Purpose

Input text string with gendered pronouns and output same text replacing with the non-gendered pronouns "they/them". 

| Function             | He set  | She set | Replace with |
| -------------------- | ------- | ------- | ------------ |
| Subject              | he      | she     | they         |
| Object               | him     | her     | them         |
| Possessive adjective | his     | her     | their        |
| Possessive noun      | his     | hers    | theirs       |
| Reflexive            | himself | herself | themselves   |

## Challenges

The real challenge of this project is not coding: it's working with the English language. Take this excerpt from Pride and Prejudice:

"""
However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.
"""

The phrase "that he is considered as the rightful property" when modified to use gender neutral pronouns, is grammatically correct when written like so: "that they are considered as the rightful property."

In its current form, there is no rule to take linking verbs into consideration. The output would be gramatically incorrect: "that they is considered as the rightful property."

What I discovered is that creating the rules for verb agreement is difficult even for experienced programmers. While certainly possible, it is beyond the scope of this project. In its current form, the grammar of the output needs to be verified. 

Here are the troubling grammar rules:

| Original           | Neutral output needed |
|--------------------|-----------------------|
| "he **is**"        | "they **are**"        |
| "he **was**"       | "they **were**"       |
| "she **has been**" | "they **have been**"  |
| "he **isn't**"     | "they **aren't**"     |
| "wasn't he"        | "weren't they"        |


So this is a problem of the English language. I had to concede on this step to avoid delaying this project's deadline by months.

---

As for the English language challenges, there are a few situations we can adjust to map out proper grammar for around 80% of cases, without relying on advanced programming knowledge.

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

---

### Code Explanation
```
import spacy

nlp = spacy.load("en_core_web_sm")
```
The spaCy module is a natural language processor that uses multiple processing pipelines.  The default option for english is `en_core_web_sm`

After tokenization, spaCy can parse and tag a given Doc. This is where the trained pipeline and its statistical models come in, which enable spaCy to make predictions of which tag or label most likely applies in this context. A trained component includes binary data that is produced by showing a system enough examples for it to make predictions that generalize across the language – for example, a word following “the” in English is most likely a noun.

Linguistic annotations are available as Token attributes. Like many NLP libraries, spaCy encodes all strings to hash values to reduce memory usage and improve efficiency. So to get the readable string representation of an attribute, we need to add an underscore _ to its name:

---


```
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for token in doc:
    print(token.text)
```
