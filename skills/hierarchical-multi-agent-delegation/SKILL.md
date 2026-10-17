---
name: hierarchical-multi-agent-delegation
description: Strict 3-Tier Hierarchical Asynchronous Multi-Agent Delegation Protocol. Owner -> Director translates & assigns brief to Lead Architect -> Lead Architect & Analis Token collaborate on 3-Tier LLM selection, token budgeting, agent matrix, and 4 Velocity SLAs -> Reports Pre-Flight Assessment to Owner -> Director & Lead Architect enter STANDBY mode awaiting Owner approval before any execution.
---

# Hierarchical Asynchronous Multi-Agent Delegation Protocol

## 1. Arsitektur Hirarki & Alur Kerja Lengkap (Mandat Standby Owner)

```
[1. OWNER (User)]
       │ (1. Memberikan Prompt / Request Baru)
       ▼
[2. AI GOVERNANCE DIRECTOR (Chief Orchestrator)]
       │ • Menterjemahkan visi & kebutuhan bisnis Owner menjadi sasaran teknis yang terukur.
       │ • Mendelegasikan brief resmi kepada Lead Arsitek.
       ▼
[3. LEAD ARSITEK + ANALIS TOKEN (FinOps) - PRE-FLIGHT ASSESSMENT]
       │ • Berkolaborasi bersama mengolah:
       │    1. Pemetaan Model 3-Tier (Cloud Fast, Cloud Deep, On-Premise Throttled Qwen).
       │    2. Estimasi Penggunaan Token & Proyeksi FinOps.
       │    3. Pemetaan Matriks Agent Pelaksana (Worker Agents).
       │    4. Estimasi Durasi Pengerjaan & Tagging 4 Kecepatan Kerja (Velocity SLA).
       ▼
[4. LAPORAN RESMI PRA-EKSEKUSI KEPADA OWNER]
       │ • Menyajikan laporan pra-penerbangan terstruktur kepada Owner:
       │    - Sasaran & Terjemahan Teknis Tugas
       │    - Tagging Kecepatan Kerja (A1 / ASAP / Normal / Lambat)
       │    - Alokasi Model 3-Tier
       │    - Estimasi Token & FinOps
       │    - Tim Agent yang Mengerjakan & ETA
       ▼
[5. DIREKTUR & LEAD ARSITEK MEMASUKI MODE STANDBY]
       │ • Direktur dan Lead Arsitek STANDBY MENUNGGU PERINTAH OWNER.
       │ • TIDAK MENJALANKAN EKSEKUSI PERUBAHAN APAPUN SEBELUM OWNER MENYETUJUI.
       ▼
[6. EKSEKUSI TEKNIS (Setelah Mendapat Instruksi / Approval Owner)]
       │ • Registrasi RFC Change Management & Backup Snapshot Otomatis.
       │ • Pengerjaan oleh Worker Agent spesialis.
       │ • Verifikasi Mutu Zero-Defect (ECC PASS) & Rilis.
```

## 2. Standar Baku 4 Kecepatan Kerja (Workload Velocity SLA)

1. **`A1` (Instant Telemetry & Query — Target: < 1-2 Menit)**
   - Sifat: *Read-only*, tanpa mutasi file (`0 mutation`), info topologi, IP, telemetri live, status port, log.
   - Model: Tier 1 Fast Cloud atau Tier 3 Lokal ($0 Token).
   - Jalur QA: **Bypass QA SIT/UAT & RFC Snapshot** (Respon instan tanpa overhead pengujian).

2. **`ASAP` (Quick Hotfix & Micro-Patch — Target: 5-10 Menit)**
   - Sifat: Modifikasi kode bedah mikro (*surgical micro-patch*), styling UI/UX CSS, bugfix 1 endpoint, update config.
   - Model: Tier 1 Cloud dengan failover ke Tier 2.
   - Jalur QA: **Targeted Smoke Test** (RFC Snapshot cepat + Uji Gate 1-3 ECC).

3. **`Normal / Medium` (Deep Feature & Core Refactor — Target: 10-30 Menit)**
   - Sifat: Fitur baru, logika bisnis berbobot, schema database baru, integrasi controller pihak ketiga.
   - Model: Tier 2 Flagship Reasoning.
   - Jalur QA: **Full 6-Gate ECC (Zero-Defect)** + Snapshot Rollback Protection.

4. **`Lambat` (Autonomous Marathon — Target: 1-6 Jam)**
   - Sifat: Multi-step ratusan langkah, pembuatan web app full-stack dari 0 hingga jadi, orkestrasi multi-agent.
   - Model: **Hybrid Multi-Tier Cascade** (Tier 2 Architect + Tier 1 Coder + Tier 3 Qwen Lokal untuk batch parsing).
   - Fitur Wajib: **Milestone Heartbeat Checkpoint** (Update status berkala ke Owner tiap 30-45 menit).
