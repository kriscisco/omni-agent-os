---
name: enterprise-change-enablement
description: ITIL v4 Change Enablement & ISO/IEC 27001 Audit Trail standard. Enforces automated RFC ticket creation, pre-change file snapshots, automatic disaster rollback on QA defect, and local LLM executive summaries.
---

# Enterprise Change Enablement & Automated Rollback

## 1. Alur Siklus Hidup Perubahan (RFC Lifecycle)
1. **Registrasi RFC (`create_rfc`):**
   Mendaftarkan nomor tiket perubahan (format: `RFC-YYYYMMDD_HHMMSS`), mengamankan backup snapshot file asli ke folder `snapshots/<RFC_ID>/`.
2. **Eksekusi Perubahan:**
   Worker agent menerapkan perubahan kode atau konfigurasi.
3. **Pengujian Mutu (SIT/UAT ECC):**
   Harness `ecc/verify.py` dijalankan secara menyeluruh.
4. **Pencatatan Hasil (`record_result`):**
   - **Jika PASS:** Tiket ditutup dengan status `SUCCESS`, perubahan permanen dicatat ke `change_registry.json` dan `CHANGELOG.md`.
   - **Jika FAILED:** **Disaster Auto-Rollback** otomatis terpicu. Seluruh file yang diubah direstorasi dari backup snapshot ke kondisi stabil semula.

## 2. Ringkasan Eksekutif Bahasa Manajemen ($0 Token)
Menggunakan model on-premise lokal Qwen 2.5 3B (`qwen2.5:3b-throttled`) di port `:11434` untuk menyusun ringkasan perubahan 1-2 kalimat dalam Bahasa Indonesia formal bagi jajaran Direktur/Owner. Berjalan di latar belakang tanpa biaya token cloud ($0) dan dengan CPU limit $\le 60\%$.
