# pyright: reportMissingImports=false
"""Reproduce the Orange Task 3 pipeline without the canvas.

The canvas in `task3.ows` needs an interactive `orange-canvas` session, so this
script runs the identical chain headless with the same widget methods:

    File -> Corpus -> Bag of Words -> PCA -> {Naive Bayes, kNN}
         -> Test and Score -> Confusion Matrix

Orange is installed in a separate environment because it does not support the
Python 3.14 used by the rest of the project:

    .venv-orange/bin/python scripts/orange-task3/run_pipeline.py

It prints the numbers each widget reports and writes them to results.json.
"""

import json
import os
import pathlib

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
from Orange.classification import KNNLearner, NaiveBayesLearner
from Orange.data import Domain
from Orange.evaluation import TestOnTrainingData
from Orange.preprocess import Continuize, RemoveNaNColumns
from Orange.projection import PCA
from orangecontrib.text import Corpus
from orangecontrib.text.vectorization import BowVectorizer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

REPO = pathlib.Path(__file__).resolve().parents[2]
CSV = REPO / "data" / "Web-Mining" / "crawling_detik.csv"
SPORT = 1  # class_var order is (finance, sport)


def build_table():
    """File -> Corpus -> Bag of Words."""
    corpus = Corpus.from_file(str(CSV))

    # The Corpus widget promotes the label column to the class variable and
    # marks which meta column carries the document text.
    label = next(a for a in corpus.domain.attributes if a.name == "label")
    keep = [a for a in corpus.domain.attributes if a.name != "label"]
    metas = [m for m in corpus.domain.metas if m.name in ("isi_berita", "url")]
    corpus = Corpus.from_table(Domain(keep, label, metas=metas), corpus)
    corpus.set_text_features([m for m in corpus.domain.metas if m.name == "isi_berita"])

    bow = BowVectorizer(norm=BowVectorizer.L2, wglobal=BowVectorizer.IDF)
    bow_corpus = bow.transform(corpus)
    return corpus, Continuize()(
        RemoveNaNColumns()(bow_corpus.transform(bow_corpus.domain))
    )


def pca_marks(table):
    """Cumulative explained variance at the usual thresholds."""
    model = PCA(n_components=min(table.X.shape) - 1)(table)
    cum = np.cumsum(model.explained_variance_ratio_)
    out = {}
    for t in (0.2, 0.5, 0.8, 0.9, 0.95):
        i = int(np.argmax(cum >= t))
        out[str(t)] = {"components": i + 1, "variance": round(float(cum[i]), 4)}
    return out, len(cum)


def evaluate(table):
    """Test and Score + Confusion Matrix for both learners."""
    out = {}
    for name, learner in (
        ("Naive Bayes", NaiveBayesLearner()),
        ("kNN (k=2)", KNNLearner(n_neighbors=2)),
    ):
        res = TestOnTrainingData(learners=[learner], data=table)
        actual = np.asarray(res.actual).astype(int)
        predicted = np.asarray(res.predicted)[0].astype(int)
        out[name] = {
            "accuracy": round(float(accuracy_score(actual, predicted)), 4),
            "precision_sport": round(
                float(precision_score(actual, predicted, pos_label=SPORT)), 4
            ),
            "recall_sport": round(
                float(recall_score(actual, predicted, pos_label=SPORT)), 4
            ),
            "f1_sport": round(float(f1_score(actual, predicted, pos_label=SPORT)), 4),
            "confusion": [
                [int(v) for v in row]
                for row in confusion_matrix(actual, predicted, labels=[0, 1])
            ],
        }
    return out


def main():
    corpus, table = build_table()
    marks, total = pca_marks(table)
    models = evaluate(table)

    summary = {
        "source": str(CSV.relative_to(REPO)),
        "n_documents": int(table.X.shape[0]),
        "n_terms": int(table.X.shape[1]),
        "class_values": [str(v) for v in table.domain.class_var.values],
        "text_features": [v.name for v in corpus.text_features],
        "pca_marks": marks,
        "pca_total_components": total,
        "models": models,
    }

    print(f"documents      : {summary['n_documents']}")
    print(f"bow terms      : {summary['n_terms']}")
    print(f"text feature   : {summary['text_features']}")
    print(f"pca 90% var    : {marks['0.9']} (of {total} components)")
    for name, m in models.items():
        print(
            f"{name:13}: acc={m['accuracy']:.3f} P={m['precision_sport']:.3f} "
            f"R={m['recall_sport']:.3f} F1={m['f1_sport']:.3f} "
            f"confusion={m['confusion']}"
        )

    dest = pathlib.Path(__file__).with_name("results.json")
    dest.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()
