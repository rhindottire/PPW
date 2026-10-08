"""News classifier inference for the Hugging Face Space.

Reproduces the serving transform of the Data Preparation notebook so a new
article is cleaned exactly like the training corpus: ascii normalization,
artifacts and number rules, sentence tokenization with slang protection, then
mean-pooled skip-gram vectors classified by Gaussian naive Bayes.
"""

import json
import re
import unicodedata
from pathlib import Path

import joblib
import numpy as np
from gensim.models import Word2Vec
from indoNLP.preprocessing import replace_slang

BASE = Path(__file__).resolve().parent
MODELS = BASE / "models"

_PROTECTED = set(json.loads((MODELS / "protected.json").read_text(encoding="utf-8")))
_LABELS = json.loads((MODELS / "labels.json").read_text(encoding="utf-8"))
_W2V = Word2Vec.load(str(MODELS / "word2vec.model"))
_GNB = joblib.load(MODELS / "gnb.joblib")

PUNCT_MAP = {
    "\u2011": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
}
ARTIFACTS = [
    r"\|[^|\n]*\|",
    r"(?m)^\s*[-*]\s|^#{1,6}\s",
    r"@\w+",
    r"https?://\S+|www\.\S+",
]
NUMBER_RULES = [
    (r"\d{1,2}/\d{1,2}/\d{4}", " "),
    (r"(?i)\b(rp)\d+", r"\1"),
    (r"(?i)\b[a-zA-Z]+-\d+\b", " "),
]
TOKEN_PATTERN = r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
SENTENCE_SPLIT = r"(?<=[.!?])\s+"


def ascii_normalize(value):
    decomposed = unicodedata.normalize("NFD", value)
    unaccented = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    for bad, good in PUNCT_MAP.items():
        unaccented = unaccented.replace(bad, good)
    return "".join(ch for ch in unaccented if ord(ch) < 128)


def clean_text(value):
    text = ascii_normalize(value)
    text = re.sub(r"\|", " ", text)
    for pattern in ARTIFACTS:
        text = re.sub(pattern, " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for pattern, replacement in NUMBER_RULES:
        text = re.sub(pattern, replacement, text)
    return text


def sentence_tokens(value):
    sentences = []
    text = clean_text(value)
    for sentence in re.split(SENTENCE_SPLIT, text):
        tokens = []
        for tok in re.findall(TOKEN_PATTERN, sentence):
            if re.fullmatch(r"\d+[xX]\d+", tok):
                tokens.append(tok.lower())
            elif any(ch.isdigit() for ch in tok) or len(tok) < 2:
                continue
            else:
                tok = tok.lower()
                if tok in _PROTECTED or replace_slang(tok) == tok:
                    tokens.append(tok)
                else:
                    tokens.append(replace_slang(tok))
        if tokens:
            sentences.append(tokens)
    return sentences


def pool(sentences):
    words = [tok for sentence in sentences for tok in sentence]
    vectors = [_W2V.wv[word] for word in words if word in _W2V.wv]
    if not vectors:
        return np.zeros(_W2V.vector_size)
    return np.mean(vectors, axis=0)


def classify(value):
    vector = pool(sentence_tokens(value)).reshape(1, -1)
    probabilities = _GNB.predict_proba(vector)[0]
    label = _GNB.classes_[int(np.argmax(probabilities))]
    scores = {
        str(c): round(float(p), 3)
        for c, p in zip(_GNB.classes_, probabilities, strict=True)
    }
    return label, scores


def describe(value):
    sentences = sentence_tokens(value)
    words = [tok for sentence in sentences for tok in sentence]
    in_vocab = sum(word in _W2V.wv for word in words)
    return {
        "labels": _LABELS,
        "sentences": len(sentences),
        "tokens": len(words),
        "words in vocabulary": in_vocab,
    }
