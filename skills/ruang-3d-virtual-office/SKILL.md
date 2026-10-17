---
name: ruang-3d-virtual-office
description: Integrates Hermes Agent 3D Virtual Office and Three.js spatial digital twin for real-time visual monitoring of multi-agent activities on port 3001.
---

# Ruang 3D Virtual Office Integration

## 1. Konsep & Arsitektur
*Ruang* adalah kantor virtual 3D berbasis WebGL (Three.js) yang memvisualisasikan seluruh agen di meja kerja mereka secara live di port `:3001`.
- Agen yang sedang mengeksekusi tugas digambarkan sedang mengetik aktif di meja kerja.
- Agen yang sedang idle/standby berada di area lounge kantor.
- Memberikan transparansi visual langsung kepada pimpinan/Owner mengenai agen mana yang sedang bekerja.

## 2. Cara Kerja & Integrasi
- Engine Ruang berjalan sebagai user service systemd (`ruang.service`).
- Menggunakan adaptor `hermes` CLI untuk membaca sesi aktif, kanban board, dan log aktivitas secara *read-only* tanpa merubah status sistem.
- Dapat diakses langsung dari dashboard Bento Grid melalui tautan cepat ke `http://127.0.0.1:3001`.
