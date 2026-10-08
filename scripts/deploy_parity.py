"""Parity check between the deployed serving pipeline and the training data.

Compares deploy.serve.sentence_tokens against the sentences written by the
Data Preparation notebook, then replays the 160/40 split and checks that
serve.classify returns the same accuracy the Modeling notebook measured.
"""

import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "deploy"))
DATA_DIR = ROOT / "data" / "Web-Mining"

from serve import (  # pyright: ignore[reportMissingImports]  # pyrefly: ignore[missing-import]
    classify,
    sentence_tokens,
)


def main():
    tokens = json.loads(
        (DATA_DIR / "crisp-dm" / "tokens.json").read_text(encoding="utf-8")
    )
    raw = pd.read_csv(DATA_DIR / "crawling_detik.csv")

    mismatches = []
    for i, (expected, value) in enumerate(
        zip(tokens["sentences"], raw["isi_berita"], strict=True)
    ):
        actual = sentence_tokens(value)
        if actual != expected:
            mismatches.append(i)
            if len(mismatches) >= 5:
                break

    labels = raw["label"]
    _train_idx, test_idx = train_test_split(
        list(range(len(raw))), test_size=0.2, random_state=42, stratify=labels
    )
    predictions = []
    for i in test_idx:
        label, scores = classify(raw["isi_berita"].iloc[i])
        predictions.append((label, labels.iloc[i], scores))
    accuracy = sum(1 for label, expected, _ in predictions if label == expected) / len(
        predictions
    )

    print(f"documents checked: {len(raw)}")
    print(f"sentence mismatches vs training corpus: {len(mismatches)}")
    if mismatches:
        print("first mismatch ids (1-based):", [m + 1 for m in mismatches])
    print(f"test documents: {len(predictions)}")
    print(f"test accuracy: {accuracy:.3f}")
    print(f"expected accuracy from Modeling: {0.975}")
    return not mismatches and abs(accuracy - 0.975) < 0.01


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
