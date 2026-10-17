---
name: zero-defect-ecc-testing
description: Enforces TDD multi-gate zero-defect automated testing harness (ECC - Enhanced Coding Capabilities). Ensures 100% PASS with 0 defects before any code change is released to production.
---

# Zero-Defect ECC Testing Framework (SIT/UAT QA Standard)

## 1. Filosofi Zero-Defect
Sistem menolak rilis kode yang cacat atau berhalusinasi. Seluruh perubahan kode harus melewati **Verification Gate Harness** melalui skrip `ecc/verify.py` dengan hasil akhir **100% PASS (0 Defect)**.

## 2. Struktur 5-Gate Standar
- **[Gate 1] Static Code Integrity & Syntax Check (L1):**
  Kompilasi Python (`py_compile`) tanpa error sintaks dan validasi elemen DOM antarmuka web.
- **[Gate 2] Component Logic & Metric Calculation Unit Tests (L2):**
  Pengujian unit kalkulasi data kernel (`/proc/stat`, `/proc/meminfo`, kalkulasi CPU per-core).
- **[Gate 3] System Integration Testing (SIT) on Running Service (L3):**
  Pengujian live HTTP 200, validasi skema JSON endpoint, dan latensi RTT.
- **[Gate 4] AI Agent & SSE Streaming Quality Check (L4):**
  Memastikan respon streaming Server-Sent Events (SSE) AI Agent merespons secara mulus tanpa chunk terputus.
- **[Gate 5] Token FinOps & Velocity SLA Verification (L5):**
  Memverifikasi klasifikasi 4 Kecepatan Kerja (`A1`, `ASAP`, `Normal`, `Lambat`) bekerja akurat.
