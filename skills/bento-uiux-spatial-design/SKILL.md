---
name: bento-uiux-spatial-design
description: Bento Grid UI/UX design rules, high-contrast pop-up styling, Pantone Pastel palette, responsive 50/50 desktop split, and rigid static height container with internal scroll down.
---

# Bento Grid UI/UX & Spatial Design Standard

## 1. Prinsip Desain Antarmuka
- **Clean White Bento Grid:** Menggunakan kartu berbasis grid modular dengan border tegas (`border-2 border-slate-200`) dan elevasi pop-up kontras tinggi pada interaksi hover.
- **Palet Warna Pastel Pantone:**
  - Mint (`#10b981`): Status aktif, performa prima, RAM.
  - Sky (`#0ea5e9`): Telemetri jaringan, latensi, live stream.
  - Lavender / Indigo (`#6366f1` / `#7c3aed`): AI Agent Assistant, Dify Engine.
  - Butter / Amber (`#f59e0b`): Utilisasi penyimpanan, storage warning.
  - Rose (`#f43f5e`): Beban CPU kritis, defect alert.

## 2. Aturan Ketinggian Statis & Internal Scroll (Anti-Stretch)
Untuk mencegah kartu melebar ke bawah saat teks pesan bertambah panjang:
- **Kontainer Luar (Kartu):** Wajib menggunakan ketinggian statis kaku:
  `class="card-popup ... flex flex-col h-[620px] max-h-[620px] overflow-hidden"`
- **Kontainer Pesan Internal:** Wajib menggunakan pembatas flexbox `min-h-0`:
  `class="flex-1 min-h-0 p-5 overflow-y-auto custom-scrollbar"`
Dengan aturan ini, seluruh percakapan panjang akan bergulir (*scrolling down*) di dalam kotak agen, tanpa memperpanjang halaman web utama.
