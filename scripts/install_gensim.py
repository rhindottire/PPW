#!/usr/bin/env python3
"""Reproducible gensim install for CPython 3.14.

gensim 4.4.0 ships no cp314 wheel and its bundled C sources are too old
for Python 3.14 ('PyLongObject.ob_digit' was removed). This script builds
gensim from the sdist after regenerating the C code with a modern Cython
and restores the missing 'fastss' extension as a pure-Python stub.

Usage:
    python scripts/install_gensim.py            # install if missing
    python scripts/install_gensim.py --force    # rebuild regardless
    python scripts/install_gensim.py --check    # verify only
"""

import argparse
import pathlib
import shutil
import subprocess
import sys
import tarfile

GENSIM_VERSION = "4.4.0"
CYTHON_PIN = "Cython==3.3.0"
BUILD_DIR = pathlib.Path("/tmp") / f"gensim-build-{GENSIM_VERSION}"

FASTSS_STUB = '''\
# Pure-Python stand-in for the missing gensim "fastss" compiled extension.
# The gensim 4.4.0 sdist ships no fastss.pyx/.c source, so the C module
# cannot be built on CPython 3.14. This module keeps the lazy imports
# (e.g. gensim.similarities.levenshtein) working with the same public API.


def editdist(a, b):
    """Levenshtein distance between two strings."""
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i]
        ac = a[i - 1]
        for j in range(1, lb + 1):
            cost = 0 if ac == b[j - 1] else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[lb]


class FastSS:
    """Simple kNN fuzzy-search index backed by Levenshtein distance."""

    def __init__(self, words=None, max_dist=2):
        self.words = list(dict.fromkeys(words)) if words else []
        self.max_dist = max_dist

    def query(self, word, distance):
        """Return {distance: [terms]} with terms at exactly `distance`."""
        result = {}
        for candidate in self.words:
            if editdist(word, candidate) == distance:
                result.setdefault(distance, []).append(candidate)
        return result
'''


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def is_installed():
    try:
        import gensim  # type: ignore[import-not-found]

        return gensim.__version__ == GENSIM_VERSION
    except ImportError:
        return False


def verify():
    sys.stdout.write("verifying gensim import and skip-gram training...\n")
    import gensim  # type: ignore[import-not-found]

    assert gensim.__version__ == GENSIM_VERSION, gensim.__version__
    from gensim.models import Word2Vec  # type: ignore[import-not-found]

    corpus = [
        ["olahraga", "sepakbola", "liga", "juara"],
        ["saham", "pasar", "modal", "investasi"],
        ["finansial", "bank", "kredit", "bunga"],
    ]
    model = Word2Vec(corpus, vector_size=8, min_count=1, sg=1, workers=1, seed=7)
    model.wv.most_similar("saham", topn=1)
    sys.stdout.write("OK gensim %s (skip-gram sg=1)\n" % GENSIM_VERSION)


def ensure_cython():
    try:
        import Cython  # type: ignore[import-not-found]

        if Cython.__version__.split(".")[0] == "3":
            return
    except ImportError:
        pass
    run([sys.executable, "-m", "pip", "install", "-q", CYTHON_PIN])


def download_sdist(dest):
    dest.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "download",
                    "-q",
                    f"gensim=={GENSIM_VERSION}",
                    "--no-binary",
                    ":all:",
                    "--no-deps",
                    "-d",
                    str(dest),
                ]
            )
            return
        except subprocess.CalledProcessError:
            sys.stderr.write(f"download attempt {attempt + 1}/3 failed, retrying\n")
    raise SystemExit("could not download the gensim sdist")


def patch_setup(root):
    setup_py = root / "setup.py"
    text = setup_py.read_text()
    stale = "    ('gensim.similarities.fastss', 'gensim/similarities/fastss.c'),\n"
    if stale in text:
        setup_py.write_text(text.replace(stale, ""))


def install_fastss_stub():
    import gensim  # type: ignore[import-not-found]

    filepath = gensim.__file__
    assert filepath is not None
    site_packages = pathlib.Path(filepath).resolve().parent.parent
    stub = site_packages / "gensim" / "similarities" / "fastss.py"
    if stub.exists() and "Pure-Python stand-in" in stub.read_text():
        return
    stub.write_text(FASTSS_STUB)


def install(force=False):
    if is_installed() and not force:
        verify()
        sys.stdout.write(
            "gensim already installed; skipping build (--force to rebuild)\n"
        )
        return

    ensure_cython()
    download_sdist(BUILD_DIR)
    sdist = next(BUILD_DIR.glob(f"gensim-{GENSIM_VERSION}.tar.gz"))
    root = BUILD_DIR / f"gensim-{GENSIM_VERSION}"
    if root.exists():
        shutil.rmtree(root)
    with tarfile.open(sdist) as tar:
        tar.extractall(BUILD_DIR)

    for stale in root.rglob("*"):
        if stale.suffix in {".c", ".cpp"}:
            stale.unlink()
    patch_setup(root)

    run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            ".",
            "--no-build-isolation",
            "--no-cache-dir",
        ],
        cwd=root,
    )
    install_fastss_stub()
    verify()
    sys.stdout.write("gensim %s installed and verified\n" % GENSIM_VERSION)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force", action="store_true", help="rebuild even if installed"
    )
    parser.add_argument("--check", action="store_true", help="verify installation only")
    args = parser.parse_args()

    if args.check:
        if not is_installed():
            raise SystemExit("gensim is not installed")
        verify()
        return
    install(force=args.force)


if __name__ == "__main__":
    main()
