# Catatan Folder RULE-BASED

Catatan pembacaan `resource/IE/RULE-BASED/`. Dibaca read-only; file sumber
tidak diubah. Sumber data `INPUT-*.zip` & `OUTPUT-*.zip` sudah diekstrak ke
`RULE-BASED/INPUT/` dan `RULE-BASED/OUTPUT/`; arsip `.zip` aslinya dihapus dari
repo setelah ekstraksi (semua isi terverifikasi terekstrak).

## Inventori File

- **Python (7)**: `entityGenerator.py`, `newEntityGenerator.py`, `entityGenerator3.py`,
  `ruleBased-IE.py`, `newRule-BasedIE.py`, `ruleBased-IE3.py`, `courtHistoryCsv.py`
- **Data**: `courtHistory.csv` (85 baris, 15 kolom), `INPUT/` (14 .txt putusan),
  `OUTPUT/` (15 .txt hasil ekstraksi `O-*.txt`)

## Alur Pipeline

```
INPUT/*.txt (putusan asli, format Salinan/MAJELIS HAKIM)
   ↓  entityGenerator*.py   (regex + pencarian keyword per baris)
OUTPUT/O-*.txt  (hasil ekstraksi entitas)
   ↓  courtHistoryCsv.py
courtHistory.csv  (baris per putusan, 15 kolom)
```

Pasangan input→output konsisten EXCEPT: `OUTPUT/O-200Pid.B2015.PNJKTTIM.txt`
ada tapi tidak ada `INPUT`-nya (200Pid). Jadi OUTPUT berisi 15 file, INPUT 14.

## Entitas yang Diekstrak (15 kolom courtHistory.csv)

```
Nomor Putusan, Nama Terdakwa 1..3, Tuntutan Pidana, Tuntutan KUHP,
Tuntukan Hukuman [typo: Tuntukan], Putusan Pidana, Putusan Hukuman,
Tanggal Putusan, Hakim Ketua, Hakim Anggota1, Hakim Anggota2,
Panitera, Penuntut Umum
```

## Per Platform Versi

### entityGenerator.py — versi lama (menulis ke OUTPUT/O-*.txt)
- Keyword by baris (lowercased): `pid.b+nomor`, `nama terdakwa :`/`nama lengkap :`,
  `menyatakan terdakwa...sebagaimana/pasal/kuhp`, `menjatuhkan pidana selama`,
  `diputuskan dalam...tanggal/oleh/dibantu`, dst.
- Menulis ke `OUTPUT/` + meng-`print` hasil ke console.
- Lemah: hardcode indeks slice (mis. `cari_pidanaT+32`); `find()` bernilai -1
  bila pola tak ada → deduksi gagal; `cari_hakim_anggota1` rawan unbound;
  `hakim_anggota.find(" dan")` = -1 bila tak ada " dan" → slice aneh.

### newEntityGenerator.py — versi regex (menulis O-*.txt)
- Menambah regex: `re.search(r'\d+/(.)*/\d{4}/(.)*', nomor, re.M|re.I)`.
- **BUG KRITIS (NameError)**: variabel `nomor` **tidak pernah didefinisikan**
  — di `entityGenerator.py` variabel itu `baris`. Baris ini akan melempar
  `NameError: name 'nomor' is not defined` begitu baris berisi `pid.b` pertama
  ditemukan → **tidak mungkin jalan** seperti sekarang.
- **BUG struktur**: bagian bawah script memanggil `generateEntity(...)` langsung
  (bukan di dalam `if __name__ == "__main__":`) → kode dieksekusi **saat import**,
  memaksa nama file hardcode (`48Pid.B2015.PNJKTTIM.txt`) mengharap INPUT sudah isi.

### entityGenerator3.py — versi modern (return list, tanpa tulis file)
- `generateEntity(pathFile, fileName)` → `return listHasil` (list 15 elemen,
  urut sesuai 15 kolom CSV). Berargumen untuk dipakai bersama courtHistoryCsv.
- **Anomali penting**: memakai `terdakwa` sebagai penanda urutan tuntutan —
  logika `terdakwa == 1/2/3` saat baris `ditahan` tampak untuk menyusun
  daftar terdakwa; rapuh bila format input tak konsisten.
- Dipakai oleh `ruleBased-IE3.py` TAPI dengan import yang salah (lihat di bawah).

### ruleBased-IE.py & newRule-BasedIE.py
- Loop input → panggil `generateEntity` dari `entityGenerator`/`newEntityGenerator`
  (modul yang TIDAK dipakai versi 3). `hasil_path` tak terpakai.

### ruleBased-IE3.py
- **BUG KRITIS (ImportError)**: `from entityGenerator2 import generateEntity`
  → modul `entityGenerator2.py` **tidak ada** di folder (yang ada
  `entityGenerator3.py`). Perlu diganti `entityGenerator3`.
- Memanggil `courtHistory(listHasil)` dari `courtHistoryCsv.py` untuk menulis CSV.

### courtHistoryCsv.py
- Menulis header 15 kolom bila file belum ada; baris hasil di-append.
- Variabel `csvFolrder` tak terpakai; penanganan `append` vs `write` memakai
  `os.path.exists`.

## Poin Kritis

1. **`ruleBased-IE3.py` tidak mengimpor modul yang benar** → ImportError (file:line `ruleBased-IE3.py:2`). Perbaikan: `from entityGenerator3 import generateEntity`.
2. **`newEntityGenerator.py` NameError variabel `nomor`** (file: `newEntityGenerator.py` di blok nomor putusan) → tidak jalan.
3. **`newEntityGenerator.py` modul-level code** → efek samping saat import.
4. Magic offset di `entityGenerator.py` (mis. `+16`, `+14`, `+32`, `+13`,
   `+21`, `+9`, `+5`, `+8`) rapuh terhadap variasi penulisan di teks putusan.
5. Semua script memakai `lower()` sebelum pencarian → entitas kehilangan casing
   asli (nama orang jadi lowercase); berdampak bila data dipakai untuk NER nanti.
6. `courtHistory.csv` berisi hasil output yang sudah pernah di-generate
   sebelumnya (85 baris) — jangan di-timpa saat uji coba tanpa izin.
7. Anomali `O-200Pid...txt` tanpa sumber INPUT-nya → terjelaskan oleh replika:
   file `INPUT-*.zip` ikut terbaca `listdir` saat pipeline dijalankan penuh
   (lihat Penilaian Run-Readiness).

## Penilaian Run-Readiness (tugas dosen: pastikan bisa jalan)

Status terkini 2026-09-13 — diverifikasi di SALINAN `/tmp` (source asli
tidak diubah; replicanya dibuang setelah dicek).

- `ruleBased-IE.py` : ⚠️ jalan bila import `entityGenerator` (versi lama ok);
  input folder harus berisi txt hasil ekstrak.
- `newRule-BasedIE.py`: ✅ **run-true** setelah fix `nomor`→`baris` di
  `newEntityGenerator.py`; 14 txt → 14 `O-*.txt`. Perlu `errors='ignore'` agar
  tahan baris non-UTF8; crash hanya pada file `INPUT-*.zip` tanpa itu.
- `ruleBased-IE3.py` : ✅ **run-true** setelah fix import `entityGenerator2`
  → `entityGenerator3`; pipeline penuh INPUT→CSV berjalan, 14 nomor putusan
  cocok dengan `courtHistory.csv` asli. Butuh `errors='ignore'` + guard
  `if eNomor:` (regex gagal di sebagian file).
- `entityGenerator3.py`: ✅ **run-true**; return list; di replika ditambah
  guard `eNomor`.

Temuan tambahan dari replika: file `INPUT-*.zip` ikut terbaca `os.listdir` →
baris CSV kosong ke-15 (menjelaskan anomali `O-200Pid.*.txt` tanpa input pada
run asli); `courtHistory.csv` asli 85 baris = hasil 6× run (mode append).