# 🌐 Omni-Agent Operating System (Omni-Agent OS)

> **Enterprise Multi-Agent Governance & Collaboration Framework**  
> *Domain-Agnostic · Zero-Defect Architecture · 4 Velocity SLAs · ITIL v4 Change Enablement*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ECC Verified](https://img.shields.io/badge/ECC-Zero--Defect-10b981.svg)](ecc/verify.py)
[![Architecture](https://img.shields.io/badge/Architecture-3--Tier%20Hierarchical-6366f1.svg)](skills/hierarchical-multi-agent-delegation/SKILL.md)

---

## 📌 Pengenalan

**Omni-Agent OS** adalah fondasi tata kelola kecerdasan buatan otonom (*Autonomous Multi-Agent Operating System*) tingkat perusahaan. Sistem ini dirancang untuk dapat diterapkan di server mana pun dan **di industri apa pun** (Keuangan, Hukum/Legal, Medis, Logistik, E-Commerce, maupun Riset) tanpa keterikatan pada tools tertentu.

Sistem ini memecahkan 3 masalah utama dalam penerapan Multi-Agent:
1. **Mencegah Kerusakan & Hallucination:** Verifikasi bertingkat **ECC (Enhanced Coding Capabilities)** menjamin mutu zero-defect sebelum rilis.
2. **Perlindungan Data & Bencana:** Engine **Change Management** otomatis membuat snapshot dan memicu **Disaster Auto-Rollback** jika terjadi kegagalan.
3. **Efisiensi Token Maksimal:** Mesin **Cognitive FinOps** mengklasifikasikan tugas ke dalam **4 Kecepatan Kerja (SLA)** dan memanfaatkan model lokal Qwen 2.5 3B throttled untuk audit internal seharga **$0 Token**.

---

## 🏛️ Arsitektur 7 Agen Inti (Core Agent Matrix)

Sistem digerakkan oleh 7 agen inti dengan pembagian tugas yang baku:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ALUR KERJA HIERARKI 7 AGEN INTI                 │
└────────────────────────────────────────────────────────────────────────┘

  [1. OWNER (User)]
         │ (Perintah / Prompt Tugas Baru)
         ▼
  [2. DIRECTOR (Chief Orchestrator)]
         │ • Menterjemahkan visi bisnis menjadi brief teknis terukur.
         ▼
  [3. LEAD ARSITEK + ANALIS TOKEN (Pre-Flight Assessment)]
         │ • Memetakan Model 3-Tier (Cloud Fast, Cloud Deep, On-Premise Qwen).
         │ • Menghitung estimasi token & budget FinOps.
         │ • Menetapkan 1 dari 4 Kecepatan Kerja (Velocity SLA).
         ▼
  [4. LAPORAN PRE-FLIGHT & MODE STANDBY]
         │ • Melaporkan rencana kerja kepada Owner.
         │ • STANDBY MENUNGGU PERSETUJUAN OWNER SEBELUM EKSEKUSI!
         ▼
  [5. EKSEKUSI, CHANGE MANAGEMENT & QA]
         ├─► [CHANGE MANAGEMENT] : Terbitkan RFC & backup snapshot file
         ├─► [WORKER AGENT]      : Pengerjaan logika domain
         ├─► [SIT/UAT QA (ECC)]  : Verifikasi 5-Gate (Wajib 100% PASS)
         ├─► [DESIGN UI/UX]      : Penyajian Bento Grid 50/50 & Telemetri
         └─► [RUANG 3D]          : Visualisasi status kerja agen di kantor 3D
```

---

## ⚡ Standar 4 Kecepatan Kerja (Workload Velocity SLA)

| Kategori | Target Waktu | Sifat Pekerjaan | Model AI | Alur QA |
| :--- | :--- | :--- | :--- | :--- |
| **`A1`** | **< 1 - 2 Menit** | *Read-only*, info IP, status port, telemetri live, log. | Tier 1 Fast / Tier 3 Qwen ($0) | **Bypass QA & RFC** *(0ms overhead)* |
| **`ASAP`** | **5 - 10 Menit** | *Surgical micro-patch*, bugfix UI, 1 route helper, config. | Tier 1 Cloud $\rightarrow$ Tier 2 Haiku | **Targeted Smoke Test** *(Gate 1-3)* |
| **`Normal`** | **10 - 30 Menit** | Fitur baru, schema database, controller, analisis mendalam. | Tier 2 Deep Reasoning (Sonnet/Combo) | **Full 5-Gate ECC (12/12 PASS)** |
| **`Lambat`** | **1 - 6 Jam** | Full-stack app dari nol, migrasi besar, marathon task. | Hybrid Cascade + Qwen 3B Batch | **Multi-Stage + Milestone Heartbeat** |

---

## 📂 Struktur Repositori

```text
omni-agent-os/
├── README.md                           # Dokumentasi Master Arsitektur & Quickstart
├── LICENSE                             # MIT License
├── install.sh                          # Skrip deploy otomatis 1-klik di server baru
├── .gitignore                          # Menjaga keamanan kredensial & file lokal
├── .env.example                        # Template environment variables
│
├── skills/                             # 📦 PAKET SKILL RESMI 7 AGEN INTI
│   ├── hierarchical-multi-agent-delegation/
│   ├── accidental-data-loss-prevention/
│   ├── managing-python-dependencies/
│   ├── zero-defect-ecc-testing/
│   ├── enterprise-change-enablement/
│   ├── bento-uiux-spatial-design/
│   └── ruang-3d-virtual-office/
│
├── governance/                         # ENGINE TATA KELOLA & FINOPS
│   ├── change_manager.py               # RFC, Snapshot & Disaster Auto-Rollback
│   ├── token_analyzer.py               # Cognitive Workload & 4 Velocity SLAs
│   └── Modelfile.qwen3b                # Ollama CPU Throttled template (<= 60%)
│
├── portal/                             # CORE WEB GATEWAY & BENTO UI
│   ├── server.py                       # Modular FastAPI Server (Extensible)
│   ├── static/
│   │   └── index.html                  # Bento Grid 50/50 + Anti-Stretch Scroll
│   └── systemd/
│       └── portal.service.template     # Systemd user daemon
│
├── ecc/                                # ZERO-DEFECT TESTING HARNESS
│   └── verify.py                       # Automated Quality Gate Verification Suite
│
├── agents/                             # STANDAR PROMPT & PERAN 7 AGEN INTI
│   ├── 01_director.md
│   ├── 02_lead_architect.md
│   ├── 03_token_analyst.md
│   ├── 04_change_management.md
│   ├── 05_qa_ecc.md
│   ├── 06_ui_ux_designer.md
│   └── 07_ruang_virtual_office.md
│
├── ruang/                              # 3D SPATIAL VIRTUAL OFFICE
│   ├── install_ruang.sh
│   └── hermes_bridge_config.json
│
└── templates/                          # TEMPLATE UNTUK BIDANG BARU (NON-IT)
    ├── custom_worker_template.py       # Cara pasang agen non-IT (Finance, Legal, dll)
    └── custom_bento_widget.html        # Cara tambah kartu widget di dashboard
```

---

## 🚀 Panduan Memasang di Server Baru

### 1. Clone Repositori
```bash
git clone https://github.com/USERNAME/omni-agent-os.git
cd omni-agent-os
```

### 2. Jalankan Installer Otomatis
```bash
chmod +x install.sh
./install.sh
```

### 3. Jalankan Portal Gateway
```bash
python3 portal/server.py
```
Akses dashboard di browser Anda: `http://IP_SERVER_ANDA:7777`

### 4. Pasang Kantor Virtual 3D (Opsional)
```bash
./ruang/install_ruang.sh
```
Akses kantor virtual 3D di: `http://IP_SERVER_ANDA:3001`

---

## 🔌 Cara Menambahkan Agen Spesialis Non-IT (Finance, Legal, Medis, dll.)

Sistem dirancang *pluggable*. Anda cukup menyalin file template:
```bash
cp templates/custom_worker_template.py workers/finance_agent.py
```
Isi fungsi bisnis Anda, dan agen tersebut langsung mewarisi:
- Perlindungan **Auto-Rollback** jika eksekusi error.
- Evaluasi token otomatis dari **Analis Token**.
- Tampil di **Bento Grid Dashboard** dan **Ruang 3D**.

---

## 📄 Lisensi
Didistribusikan di bawah lisensi open-source **MIT License**. Lihat [LICENSE](LICENSE) untuk informasi lebih lanjut.
