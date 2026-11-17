# Information Extraction

## Task 1 — Court Scraping

**Objective.** Collect metadata for at least 200 general criminal court decisions from a selected District Court (Pengadilan Negeri) in East Java.

**What to do.**
1. Select one District Court in East Java from the assigned list (PN Ngawi).
2. Collect decision listing URLs from the "Pidana Umum" directory using `getURLlist.ipynb`.
3. Extract decision detail metadata into structured format using `getMETAINFO.ipynb` for at least 200 unique decisions.
4. Export the metadata dataset (`IE-PN-Ngawi-230411100197.csv`) and document the execution in PDF format (`IE-Scraping-230411100197.pdf`).

**Process:** [Task 1](IE/01-Scraping-230411100197.ipynb)

## Task 2 — Entity Extraction

**Objective.** Apply rule-based Information Extraction to decision documents from Task 1.

**What to do.**
1. Study the rule-based IE code in the [class drive](https://drive.google.com/drive/folders/1g8vkKr7k1YlPsT25-vTaSGM9W4eYieEz?usp=drive_link).
2. Run and verify the provided code works end-to-end.
3. Convert decision PDFs from Task 1 to TXT format.
4. Run rule-based extraction to extract the target entities from each decision.
5. Do this for at least **5** decisions.

**Process:** [Task 2](IE/02-RuleBased-IE-230411100197.ipynb)

## Task 3 — Machine Learning

**Objective.** Apply Machine Learning-based Information Extraction to decision documents.

**What to do.**
1. Study ML code from ML1 and ML2 in the [class drive](https://drive.google.com/drive/folders/16GKudbRKcmUgMpRpaKVKUk1sSGyT9P1n?usp=drive_link) (ML1 uses word/POS/Prev/Next features, ML2 adds word shape features).
2. Run both ML1 and ML2 to verify they produce output.
3. Create a dataset in the required format using decisions from your chosen PN (from Task 1).
4. Modify either ML1 or ML2 to run on your own dataset. You may add features/modifications if needed.
5. Run ML-based extraction to get the target entities.

**Process:** [Task 3](IE/03-MachineLearning-IE-230411100197.ipynb)

## Task 4 — Dataset Annotation

**Objective.** Build an annotated dataset for sequence labeling (IOB) from court decisions.

**What to do.**
1. Take **200** general criminal decisions from the PN chosen in Task 1.
2. Annotate **12 entities** for each decision following the **IOB** schema (`VERN`, `DEFN`, `CRIA`, `ARTV`, `PENA`, `PUNI`, `TIMV`, `JUDP`, `JUDG`, `REGI`, `PROS`, `ADVO`).
3. Have the dataset checked by **at least 2** members of the assigned group.
4. Prepare the annotated dataset file (`PN-NGW-230411100197.csv`) with standard columns `doc,sentence,word,prev,next,tag` and group audit note (`PN-NGW-230411100197.txt`).

**Process:** [Task 4](IE/04-Dataset-230411100197.ipynb)

## Task 5 — Deep Learning

**Objective.** Apply Deep Learning-based Information Extraction to court decision documents.

**What to do.**
1. Study Deep Learning IE code provided in the class drive (DL1 uses standard embeddings; DL2 uses CBOW Word2Vec representations).
2. Run baseline trials for both DL1 and DL2 to verify end-to-end execution and export verification PDFs (`IE-coba-DL1-230411100197.pdf` and `IE-coba-DL2-230411100197.pdf`).
3. Prepare the sequence dataset format using annotated decisions from Task 4 (`PN-NGW-230411100197.csv`).
4. Implement a comparative Bi-LSTM pipeline evaluating both trainable dense embeddings and pretrained Continuous Bag-of-Words (CBOW) representations on the PN Ngawi corpus.
5. Mitigate extreme tag class imbalance (96.8% `O` tokens) using masked cross-entropy loss with calibrated class weighting.
6. Extract target legal entities from court decision texts and export the documented pipeline to PDF (`IE-modif-DL-230411100197.pdf`).

**Process:** [Task 5](IE/05-DeepLearning-IE-230411100197.ipynb)

