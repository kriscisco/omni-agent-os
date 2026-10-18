---
name: report-mimic-synthesizer
description: Automatically generates new reports by mimicking the exact structure, tone, format, and section depth of an existing reference report, while synthesizing relevant data extracted from multiple files (CSV, JSON, Markdown, text, logs).
---

# Report Mimic & Data Synthesizer Skill

## 1. Konsep & Tujuan
Skill ini dirancang untuk menyelesaikan tugas penyusunan laporan berbasis acuan (*Reference-Conditioned Document Synthesis*):
1. **Meniru Gaya Laporan Sebelumnya (*Style & Structure Mimicry*):**
   Menganalisis dokumen acuan untuk mengekstraksi hirarki judul (`#`, `##`, `###`), pola ringkasan eksekutif, susunan tabel, gaya bahasa (*tone* formal/teknis/manajemen), serta tingkat kedalaman analisis.
2. **Kombinasi Data Multi-Sumber (*Multi-Source Data Ingestion*):**
   Membaca dan memilah data aktual dari berbagai format file (CSV, JSON, Log, TXT, Excel/Spreadsheet, atau dokumen Markdown lain), memetakan data tersebut ke bagian bab laporan yang relevan, dan menghasilkan laporan baru dengan format yang **100% konsisten** dengan laporan acuan.

---

## 2. Metodologi Eksekusi 3-Tahap

```
[1. PARSE REFERENCE REPORT]
       │ • Ekstraksi struktur heading, format tabel, bullet style, dan tone penulisan.
       ▼
[2. INGEST & MAP DATA SOURCES]
       │ • Pembacaan data aktual dari file sumber (CSV/JSON/Log).
       │ • Korelasi data numerik/faktual ke bagian bab target.
       ▼
[3. FEW-SHOT SYNTHESIS & COMPILE]
       │ • Menjalankan LLM (Tier 1 Fast atau Tier 3 Qwen $0) dengan temperature rendah (0.2).
       │ • Validasi bahwa seluruh placeholder terisi dan format identik dengan referensi.
```

---

## 3. Penggunaan Skrip CLI Otomatis

Tersedia skrip otomasi mandiri di dalam folder `scripts/`:

```bash
python3 skills/report-mimic-synthesizer/scripts/synthesize_report.py \
  --reference "path/to/laporan_lama.md" \
  --data-sources "path/to/data1.csv" "path/to/data2.json" \
  --output "path/to/laporan_baru.md"
```

### Parameter Opsional:
* `--model <nama_model>`: Pilihan model (Default: `qwen2.5:3b-throttled` lokal di Ollama, atau model API cloud seperti `gemini-3.8-flash`).
* `--temperature <float>`: Suhu kreativitas LLM (Default: `0.2` untuk menjaga kepatuhan format).
* `--lang <id|en>`: Bahasa laporan akhir (Default: `id` / Bahasa Indonesia).

---

## 4. Panduan Prompting untuk AI Agent

Jika agen menyusun laporan secara mandiri tanpa skrip CLI, ikuti format prompt baku berikut:

```markdown
Anda adalah Technical & Management Report Synthesizer.
Tugas Anda adalah membuat laporan baru yang MENIRU 100% gaya, susunan bab, dan kedalaman analisis dari DOKUMEN ACUAN di bawah ini, tetapi HANYA menggunakan DATA AKTUAL dari FILE SUMBER yang diberikan.

<DOKUMEN_ACUAN>
{isi teks laporan referensi}
</DOKUMEN_ACUAN>

<FILE_SUMBER_DATA>
{isi data CSV/JSON/teks}
</FILE_SUMBER_DATA>

ATURAN WAJIB:
1. Pertahankan semua heading, penomoran bab, dan format tabel persis seperti Dokumen Acuan.
2. Jangan mengarang data (0 halusinasi). Gunakan data aktual dari File Sumber.
3. Gunakan gaya bahasa (tone) yang identik dengan Dokumen Acuan.
```
