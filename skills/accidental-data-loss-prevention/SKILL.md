---
name: accidental-data-loss-prevention
description: STOP AND VERIFY before running any command or tool that results in irreversible data loss, data wiping, schema destruction, or mass deletions. Explicit user consent must be obtained.
---

# Accidental Data Loss Prevention (Guardrail Kritis)

> [!CAUTION]
> **ATURAN MUTLAK:** Sebelum menjalankan perintah apa pun yang menyebabkan kehilangan data permanen, kerusakan skema, atau penghapusan sumber daya tak terpulihkan, agen **WAJIB BERHENTI DAN MEMINTA PERSETUJUAN EKSPLISIT DARI USER / OWNER**.

## 1. Operasi yang Memerlukan Konfirmasi Wajib:
- **Database:** `DROP DATABASE`, `DROP TABLE`, `DROP SCHEMA`, `TRUNCATE`, atau `DELETE` massal tanpa klausa WHERE.
- **Sistem File:** `rm -rf /`, `rm -rf` pada folder root proyek atau direktori data penting, `git clean -fdx`, atau `git reset --hard` tanpa backup snapshot.
- **Infrastruktur & Cloud:** Penghapusan bucket penyimpanan, instance server, cluster Kubernetes, atau secret kunci enkripsi.

## 2. Prosedur Wajib Sebelum Eksekusi:
1. Identifikasi dampak kerusakan (*blast radius*).
2. Periksa ketersediaan backup snapshot (melalui `change_manager.py`).
3. Sajikan konfirmasi transparan kepada User:
   - Sumber daya apa yang akan dihapus.
   - Mengapa tindakan tersebut diperlukan.
   - Opsi mitigasi atau backup yang tersedia.
4. Tunggu persetujuan tertulis ("Setuju / Lanjutkan") dari User sebelum mengeksekusi.
