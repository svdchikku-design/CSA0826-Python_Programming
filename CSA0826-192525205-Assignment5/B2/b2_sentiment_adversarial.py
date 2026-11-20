"""B2: inputs designed to fool the lexicon + negation scorer of common/sentiment.py."""
import sys
sys.path.insert(0, "../common")
from sentiment import score, label

cases = [  # (text, what a person would say, why it is hard)
    ("The air today is good", "positive", "plain case - control"),
    ("The service is not good", "negative", "negation just before the word - handled"),
    ("Oh great, another smoke filled morning", "negative", "sarcasm: 'great' is not in the lexicon, 'smoke' is: right by luck"),
    ("The air is so good that I had to wear a mask", "negative", "sarcasm with a positive word"),
    ("The air is not at all good", "negative", "negator is two words before 'good'"),
    ("The helpline was never not helpful", "positive", "double negative: 'never not helpful' means helpful"),
    ("Good staff but dirty office, slow lift and rude guard", "negative", "mixed opinions: one positive, three negative"),
    ("Good bus, bad air", "neutral", "balanced mixed opinion"),
    ("No smoke today", "positive", "'no' flips a negative word: absence of a problem"),
    ("The response was gooood and fasst", "positive", "spelling variants not in the lexicon"),
    ("GOOD!!!", "positive", "punctuation attached to the word"),
    ("Not bad", "positive", "negation of a negative word"),
    ("It was not helpful, not slow", "neutral", "two negations: one bad, one good news"),
    ("", "neutral", "empty text"),
    ("badly broken", "negative", "'badly' is a different word from 'bad'; 'broken' is in the lexicon"),
]
print(f"{'text':<52}{'expected':<10}{'program':<10}{'score':>5}  result")
wrong = 0
for text, expected, why in cases:
    got = label(text); ok = got == expected; wrong += not ok
    print(f"{text[:50]:<52}{expected:<10}{got:<10}{score(text):>5}  {'ok' if ok else 'WRONG'}   ({why})")
print(f"\n{len(cases) - wrong} of {len(cases)} right, {wrong} wrong. The program never raises an error and never says 'unsure': a wrong label looks exactly like a right one.")
