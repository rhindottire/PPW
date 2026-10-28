# Information Extraction

## Task 1 — Court Scraping

**Objective.** Get metadata for general criminal court decisions from one selected District Court (Pengadilan Negeri) in East Java.

**What to do.**
1. Coordinate with class/group leader to pick a District Court in East Java. Avoid picking the same court as others.
2. Study the scraping code provided in the [class drive](https://drive.google.com/drive/folders/1StUCQDNn7Gp7BG9yHiCVwMOojlZ4EDap?usp=sharing).
3. Get the URL for the "Pidana Umum" list for the chosen court via the MA site:
   - Open <https://putusan3.mahkamahagung.go.id/pengadilan/profil/pengadilan/pt-surabaya.html>
   - Pick the target PN from the left sidebar.
   - Click/select "Pidana Umum" in the left sidebar once the PN appears (name shown top-left).
   - Take the URL that appears at that point to run `getURLlist.ipynb`.
4. Run `getURLlist.ipynb` then `getMETAINFO.ipynb`. Modifications are allowed as long as the core logic to collect metadata from decision detail pages remains.
5. Collect metadata for at least **200** decisions. The dataset must be **different** from others.

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
2. Annotate **12 entities** for each decision following the **IOB** schema in the provided table.
3. Have the dataset checked by **at least 2** members of the assigned group.
4. Prepare the annotated dataset files with group check info.

**Process:** [Task 4](IE/04-Dataset-230411100197.ipynb)
