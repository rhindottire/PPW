# Catatan Folder DATASET

Catatan pembacaan `notebook/IE/DATASET/`. Dibaca read-only via ekstraksi
markdown/code cells; file tidak diubah. Semua notebook aslinya dieksekusi di
Google Colab (kernel `python3`), path `/content/drive/MyDrive/NER nlp/...`.

## Inventori (9 notebook)

| File | Ukuran | Isi |
|---|---|---|
| (FIX) Preprocessing & Labeling Dataset.ipynb | 850 KB | Utama: anotasi+preprocessing 602 dok pidana → token-per-baris |
| Anotasi Data Perdata.ipynb | 162 KB | Anotasi 200 dok perdata (melawan hukum) |
| Anotasi Pidana.ipynb | 469 KB | Anotasi 125 dok pidana PN Sumenep |
| Convert Dataset.ipynb | 121 KB | Konversi `all.json` (993 dok, label lama) → format text/labels |
| Pre Processing Data Baru.ipynb | 367 KB | 500 dok pidana → token per baris + prev/next; split 3 CSV |
| Pre Processing Data Lama.ipynb | 114 KB | 107 dok lama → token per baris + prev/next |
| Pre Processing Data Merge.ipynb | 169 KB | Gabung 107+993=1100 dok → Dataset-Merge.csv |
| Pre Processing Data Perdata.ipynb | 113 KB | 200 dok perdata → token per baris + prev/next |
| Salinan Anotasi Pidana.ipynb | 152 KB | Salinan rusak Anotasi Pidana (dataset Sampang) |

## Skema Label NER yang Dipakai

### Skema 1 — Pidana (11 entitas + O)
`B_/I_VERN` (nomor putusan), `TIMV` (tanggal), `JUDP` (hakim ketua),
`JUG` (hakim anggota), `REGI` (panitera), `PROS` (penuntut umum),
`DEFN` (terdakwa), `CRIA` (tindak pidana), `ARTV` (pasal KUHP),
`PENA` (tuntutan hukuman), `PUNI` (putusan hukuman).

### Skema 2 — Perdata (10 entitas + O)
`VERN, TIMV, JUDP, JUG, REGI, PLAN` (penggugat), `DENN` (tergugat),
`PLAO` (turut tergugat), `LSWR` (hasil/amar gugatan), `LSWV` (putusan gugatan).

### Skema 3 — Lama (19 entitas, label deskriptif)
`Nomor Putusan, Nama Pengadilan, Tingkat Kasus, Nama Terdakwa, Nama Jaksa,
Nama Hakim Ketua, Nama Hakim Anggota, Nama Panitera, Nama Pengacara,
Jenis Dakwaan, Jenis Perkara, Tanggal Kejadian, Tanggal Putusan,
Tuntutan Hukuman, Putusan Hukuman, Jenis Amar, Melanggar UU (Dakwaan),
Melanggar UU (Tuntutan), Melanggar UU (Pertimbangan Hukum), Nama Saksi + O`.
Mapping singkatan di Merge menambah `ADVO` (pengacara) & `JUDG` (anggota).

## Alur Utama (notebook FIX)

```
4 CSV scraping (Bangkalan, Sampang, Pamekasan, Sumenep)  [Google Drive]
   + Dataentity_pn_all.xlsx (anotasi manual)
   → concat → 602 baris valid → clean_text + multiple_replace (perbaikan typo OCR)
   → generate_label() (entities→label) → labeling_token() (trie matching)
   → handleDuplicatePena() (B_PENA kedua → B_PUNI)
   → cleaning_text / split_token → split per ';' → tokenisasi per kata
   → tambah prev/next → rename → CSV token-per-baris
```

Output FIX: `Dataset-500PidanaPolBGTNITerbaru.csv`, 602 dok / 78.262 kalimat /
**4.082.192 baris** token, akurasi anotasi 98.47%. (Nama file "500" menyesatkan.)

## Ringkasan & Output Tiap Notebook

| Notebook | Output | Format |
|---|---|---|
| (FIX) Preprocessing & Labeling | Dataset-500PidanaPolBGTNITerbaru.csv | token-per-baris `doc,sentence,word,prev,next,tag` (602 dok, 4.08 jt) |
| Anotasi Data Perdata | Dataset-Perdata200-blmFix.csv | per dok `doc,text,label` (200 dok); akurasi 81.50% |
| Anotasi Pidana | datasetAnotasiSMNP.json | per dok `doc,text,label` (125 dok); akurasi 71.12% |
| Convert Dataset | hmm.csv | per dok `text,labels` string (993 dok) |
| Pre Processing Data Baru | Dataset1/2/3.csv | token-per-baris (500 dok, 3.296.250 baris) |
| Pre Processing Data Lama | Dataset-Lama.csv | token-per-baris (107 dok, 1.029.305 baris) |
| Pre Processing Data Merge | Dataset-Merge.csv | token-per-baris (1100 dok, 7.662.678 baris) |
| Pre Processing Data Perdata | Dataset-Perdata200.csv | token-per-baris (200 dok, 2.568.230 baris) |
| Salinan Anotasi Pidana | datasetcoba.json | 122 dok, semua label O (rusak) |

## Bug & Temuan Penting

1. **`Salinan Anotasi Pidana.ipynb` = tidak jalan** (paling rusak): `generate_label`
   hanya `print` (tanpa return); fungsi `anotasi()`, `countLabel`, `accuracy`
   TIDAK ada; output tersimpan berasal dari run Colab lama. Run ulang → `NameError`.
2. **Bug label-tidak-sejajar** pada `Pre Processing Data Lama` (sel 12),
   `Pre Processing Data Merge` (sel 30), `Pre Processing Data Perdata` (sel 14):
   `'tag': row['tag']`/`'text-tags': row['text-tags']` menyalin **seluruh label
   dokumen** ke setiap kalimat → panjang `text` ≠ panjang `labels`,
   `zip()` memotong diam-diam → **label kalimat korup**. Ini masalah data serius.
3. **`Pre Processing Data Merge.ipynb` tidak konsisten**: kode yang tersimpan memakai
   kolom `text`,`text-tags` (sel 20, 30) tapi output lama menampilkan
   `word,pos,prev,next,tag`; `label_converter` mapping skema lama→baru **dikomentari**
   (tidak diterapkan) → run ulang `KeyError` & label campur skema.
4. **`Convert Dataset.ipynb` cacat logika** (sel 17): konversi token-per-baris
   menghasilkan 124.704.912 baris (artefak padding), pasangan teks↔label tidak
   sejajar, `cleaning()` tak dipakai, token belum di-split sungguhan.
5. **`Anotasi Data Perdata` & `Anotasi Pidana`**: bug print accuracy pakai string
   literal `"Accuracy : {label_in/sum_label * 100}"` (tapi `return` benar f-string);
   `labeling_token` tanpa guard key kosong; SettingWithCopyWarning.
6. **Bug kecil**: `print(f"BeautifulSoup version: {tqdm.__version__}")` (menamai
   tqdm sbg BeautifulSoup); `if label != 'O' or token == ' '` (label = list, selalu True);
   `df.loc(0)` dipanggil sebagai fungsi (TypeError bila run ulang).
7. Format kolom `doc` tidak konsisten antar notebook (`doc:0` vs `doc: 1`).
8. Ketergantungan rantai yang "hilang": tidak ada notebook yang menghasilkan
   `datasetAnotasi.json` (500 dok), `DatasetPos-Baru.csv`, `Perdata Melawan Hukum 200.json`.

## Run-Readiness (di luar Colab/Drive)

| Notebook | Status | Syarat |
|---|---|---|
| (FIX) Preprocessing & Labeling | ✅ paling siap | Drive berisi 4 CSV + xlsx anotasi; kernel perlu `enWebmining` |
| Anotasi Data Perdata | ✅ jalan (gdown) | akses gdown / URL |
| Anotasi Pidana | ✅ jalan (gdown) | akses gdown / URL |
| Convert Dataset | ⚠️ jalan ½; logika konversi cacat | Drive `all.json` |
| Pre Processing Data Baru | ✅ jalan | Drive `datasetAnotasi.json` (500 dok) |
| Pre Processing Data Lama | ⚠️ jalan tapi data korup | Drive CSV lama |
| Pre Processing Data Merge | ❌ tidak konsisten | 2 file Drive + perbaiki kolom |
| Pre Processing Data Perdata | ⚠️ jalan tapi bug label | Drive JSON perdata |
| Salinan Anotasi Pidana | ❌ pasti NameError | perbaiki generate_label/definisikan fungsi |

Catatan: semua notebook memakai Colab + Drive; untuk memenuhi aturan PPW
kernel harus `enWebmining` dan path harus dilokalkan bila dipindah ke notebook
deliverable.