---
name: data-preprocessing
description: Text preprocessing for Information Retrieval. Tokenization, stopword removal, stemming, and normalization.
---

## Yang saya lakukan
- Membersihkan teks mentah dari noise
- Tokenisasi (pecah teks jadi token/kata)
- Stopword removal (hapus kata umum yang tidak bermakna)
- Stemming (aku kata ke bentuk dasar)
- Normalisasi teks

## Saat menggunakan saya
Gunakan skill ini saat kamu perlu bersihkan data teks sebelum diproses lebih lanjut (TF-IDF, clustering, ranking).

## Library yang Tersedia
| Library | Fungsi | Contoh import |
|---------|--------|---------------|
| `nltk` | Tokenisasi, stopword | `from nltk.tokenize import word_tokenize` |
| `Sastrawi` | Stemming Bahasa Indonesia | `from Sastrawi.Stemmer.StemmerFactory import StemmerFactory` |
| `spacy` | NLP modern, POS tagging | `import spacy; nlp = spacy.load('id_core_news_sm')` |
| `scikit-learn` | TF-IDF, CountVectorizer | `from sklearn.feature_extraction.text import TfidfVectorizer` |

## Workflow Preprocessing

### 1. Tokenisasi
```python
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')

tokens = word_tokenize(teks)
```

### 2. Stopword Removal (Bahasa Indonesia)
```python
from nltk.corpus import stopwords
nltk.download('stopwords')

stop_id = set(stopwords.words('indonesian'))
tokens_bersih = [t for t in tokens if t.lower() not in stop_id]
```

### 3. Stemming (Bahasa Indonesia)
```python
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.createStemmer()

teks_stemmed = stemmer.stem(teks)
```

### 4. Gabungan (Pipeline)
```python
def preprocess(teks):
    # Tokenisasi
    tokens = word_tokenize(teks.lower())
    # Hapus stopword
    tokens = [t for t in tokens if t not in stop_id and len(t) > 2]
    # Stemming
    stemmed = [stemmer.stem(t) for t in tokens]
    return " ".join(stemmed)

df['isi_bersih'] = df['isi_berita'].apply(preprocess)
```

## Tips Penting
- Selalu download resource NLTK dulu: `nltk.download('punkt_tab')`, `nltk.download('stopwords')`
- Stemming Sastrawi cukup lambat untuk data besar — pertimbangkan batch processing
- Simpan hasil preprocessing ke kolom baru, jangan timpa kolom asli
- Untuk data yang sangat besar, pertimbangkan spaCy yang lebih cepat
