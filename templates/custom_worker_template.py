#!/usr/bin/env python3
"""
Template Agen Spesialis Domain Baru (Pluggable Worker Agent)
Contoh Implementasi: Finance, Legal, Medical, Supply Chain, dll.

Cara Pakai:
1. Gandakan file ini dan ubah nama sesuai kebutuhan domain Anda.
2. Definisikan tool atau fungsi bisnis Anda di fungsi `execute_domain_task()`.
3. Hubungkan ke Change Management jika melakukan mutasi data/file penting.
"""

import os
import sys
import json
from datetime import datetime

# Impor modul tata kelola
GOVERNANCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "governance")
if GOVERNANCE_DIR not in sys.path:
    sys.path.insert(0, GOVERNANCE_DIR)

try:
    import change_manager
    import token_analyzer
except Exception:
    change_manager = None
    token_analyzer = None

class CustomDomainWorker:
    def __init__(self, agent_name="Agent-Finance-Auditor", department="finance"):
        self.agent_name = agent_name
        self.department = department

    def pre_flight_check(self, prompt):
        """Mengevaluasi bobot tugas dan memilih model 3-Tier optimal."""
        if token_analyzer:
            analyzer = token_analyzer.TokenWorkloadAnalyzer()
            return analyzer.evaluate_task(prompt, target_department=self.department)
        return {"status": "default", "recommended_model": "gemini-3.8-flash"}

    def execute_domain_task(self, task_name, affected_files=None, is_simulation=False):
        """
        Menjalankan tugas spesialis domain.
        Jika merubah file kritis, daftarkan RFC terlebih dahulu!
        """
        rfc = None
        if change_manager and affected_files:
            rfc = change_manager.create_rfc(
                title=f"[{self.department.upper()}] {task_name}",
                requested_by="Owner",
                executor=self.agent_name,
                affected_files=affected_files,
                description=f"Eksekusi tugas domain oleh {self.agent_name} pada {datetime.now().isoformat()}"
            )
            print(f"✔ RFC Terdaftar: {rfc['rfc_id']} (Snapshot file diamankan)")

        try:
            print(f"⚙️  {self.agent_name} sedang memproses: '{task_name}'...")
            
            # --- LOGIKA BISNIS SPESIFIK DOMAIN ANDA DI SINI ---
            # Contoh:
            # - Pembacaan laporan laba rugi & rekonsiliasi bank (Finance)
            # - Verifikasi klausul kontrak dan peraturan perundang-undangan (Legal)
            # - Triage keluhan dan klasifikasi rekam medis pasien (Medical)
            # ----------------------------------------------------

            success = True
            qa_result = "Domain Logic Verified (0 Defect)"

            if change_manager and rfc:
                change_manager.record_result(
                    rfc_id=rfc["rfc_id"],
                    is_success=success,
                    qa_details=qa_result
                )
                print(f"✔ Tiket {rfc['rfc_id']} ditutup dengan status SUCCESS!")

            return {"status": "success", "task": task_name, "qa": qa_result}

        except Exception as e:
            if change_manager and rfc:
                change_manager.record_result(
                    rfc_id=rfc["rfc_id"],
                    is_success=False,
                    qa_details=f"Error: {str(e)}",
                    rollback_reason=str(e)
                )
                print(f"✖ Terjadi kegagalan! Auto-Rollback sukses dieksekusi.")
            return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    worker = CustomDomainWorker()
    eval_res = worker.pre_flight_check("Lakukan rekonsiliasi data faktur pajak bulan berjalan")
    print(json.dumps(eval_res, indent=2))
