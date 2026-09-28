---
description: Commit semua perubahan dengan pesan Conventional Commits
---

Stage semua perubahan dan buat commit dengan pesan berikut: $ARGUMENTS

Langkah:
1. Jalankan `git status --short` dan `git diff --cached --stat` setelah staging
2. Stage semua perubahan: `git add -A`
3. Verifikasi tidak ada file sensitif ter-stage (`.env`, `.venv/`, data besar yang tidak perlu)
4. Commit dengan pesan $ARGUMENTS
5. Pastikan pesan mengikuti Conventional Commits (contoh: feat:, fix:, docs:, refactor:, chore:)
6. Setelah commit, tampilkan ringkasan commit terakhir dengan `git log --oneline -3`

Jika $ARGUMENTS kosong, buat pesan commit deskriptif berdasarkan diff yang ter-stage.