---
description: Inisialisasi repo git + setup remote (untuk project baru)
---

Inisialisasi repository Git untuk project ini.

Langkah:
1. Cek apakah repository sudah ada: `git rev-parse --is-inside-work-tree`
   - Jika sudah ada, beritahu user dan berhenti
2. Inisialisasi dengan branch main: `git init -b main`
3. Verifikasi `.gitignore` mengecualikan `.venv/`, `node_modules/`, `.env`, dan `.opencode/`
4. Stage semua file: `git add -A`
5. Tampilkan file yang akan di-commit dengan `git status --short`
6. Buat commit awal: `feat: inisialisasi project`
7. Jika argumen berisi `--push`:
   - Tanyakan nama repo ke user atau gunakan nama folder project
   - Buat repo di GitHub (public/private sesuai argumen, default public)
   - Tambah remote dan push: `git remote add origin git@github.com:<user>/<repo>.git && git push -u origin main`
8. Jika tanpa `--push`, berhenti setelah commit lokal

Argumen: $ARGUMENTS (dukung flag `--push` dan `--private`)