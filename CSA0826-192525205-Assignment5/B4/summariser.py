"""Summariser (design of Task A5.2) and the alternative 'first k sentences'."""
import re
STOP = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "to", "of", "and", "in", "on", "at", "for", "it", "this", "that", "i", "we", "our", "my",
        "me", "you", "your", "they", "their", "he", "she", "with", "from", "by", "as", "or", "but", "so", "not", "no", "very", "has", "have", "had", "do", "does",
        "did", "will", "would", "can", "could", "please", "all", "any", "also", "just", "than", "then", "there", "its", "now", "still", "every", "again", "too"}

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]

def words(sentence):
    return [w for w in re.findall(r"[a-z0-9']+", sentence.lower()) if w not in STOP]

def summarise_frequency(text, k=1):
    """Pick the k sentences whose important words are most frequent in the whole complaint (shown in original order)."""
    sents = sentences(text)
    if len(sents) <= k:
        return sents
    freq = {}
    for s in sents:
        for w in words(s):
            freq[w] = freq.get(w, 0) + 1
    scores = [sum(freq[w] for w in words(s)) / (len(words(s)) or 1) ** 0.5 for s in sents]    # damped by length so long sentences do not always win
    best = sorted(range(len(sents)), key=lambda i: (-scores[i], i))[:k]
    return [sents[i] for i in sorted(best)]

def summarise_first(text, k=1):
    """Alternative: the first k sentences. Needs only the start of the text, O(1) in the length of the complaint for small k."""
    out, start = [], 0
    for m in re.finditer(r"[.!?](?:\s+|$)", text):
        out.append(text[start:m.end()].strip()); start = m.end()
        if len(out) == k: break
    return out or [text.strip()]
