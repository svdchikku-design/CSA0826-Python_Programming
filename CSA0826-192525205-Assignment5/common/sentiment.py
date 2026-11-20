"""Lexicon-based sentiment scorer with simple negation (design of Task A5.1; completed program of Task B4)."""
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def tokens(text):
    return text.lower().replace(".", " ").replace(",", " ").split()

def score(text, positive=POSITIVE, negative=NEGATIVE, negators=NEGATORS):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = tokens(text)
    total = 0
    for i, w in enumerate(words):
        value = 1 if w in positive else -1 if w in negative else 0
        if value and i > 0 and words[i - 1] in negators:
            value = -value
        total += value
    return total

def label(text, **kw):
    s = score(text, **kw)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"
