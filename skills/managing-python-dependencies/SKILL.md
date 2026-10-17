---
name: managing-python-dependencies
description: Ensures proper Python dependency isolation and packaging, avoiding global pip install conflicts and maintaining project virtual environments.
---

# Managing Python Dependencies (Standar Isolasi Dependensi)

## 1. Aturan Dasar
- **DILARANG** melakukan instalasi paket global secara serampangan menggunakan `sudo pip install` yang dapat merusak paket sistem operasi Ubuntu/Debian (`PEP 668: externally-managed-environment`).
- Gunakan virtual environment terisolasi (`venv`) untuk setiap modul proyek:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## 2. Kebutuhan Library Eksternal
Sebelum menyarankan atau mengeksekusi kode Python dengan `import` pihak ketiga:
1. Periksa ketersediaan library di sistem (`python3 -c "import <package>"`).
2. Jika belum ada, catat dependensi ke dalam file `requirements.txt`.
3. Verifikasi kompatibilitas versi Python (minimal Python 3.10+).
