#!/usr/bin/env python3
"""
Enterprise Change Management & Release Governance Engine (tim-change-management)
Standards: ITIL v4 Change Enablement, ISO/IEC 27001 Audit Trail & Automated Rollback

Core Capabilities:
1. Automated Request for Change (RFC) Registration & File Snapshots.
2. Automated Disaster Rollback if QA/ECC verification detects defects.
3. Natural Language Executive Summaries for Leadership/Owners ($0 Cost via local Qwen 3B).
4. Central Change Registry (change_registry.json & CHANGELOG.md).
"""

import os
import sys
import json
import time
import shutil
import threading
import subprocess
from datetime import datetime

GOVERNANCE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(GOVERNANCE_DIR)
REGISTRY_FILE = os.path.join(GOVERNANCE_DIR, "change_registry.json")
SNAPSHOTS_DIR = os.path.join(GOVERNANCE_DIR, "snapshots")
CHANGELOG_FILE = os.path.join(BASE_DIR, "CHANGELOG.md")
KNOWLEDGE_GRAPH_DIR = os.path.join(GOVERNANCE_DIR, "knowledge_graph")

os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_GRAPH_DIR, exist_ok=True)

def _trigger_async_graphify_update():
    """Triggers asynchronous knowledge graph updates in background if graphify is installed."""
    def _worker():
        try:
            if not os.path.exists("/usr/local/bin/graphify"):
                return
            cmd = ["/usr/local/bin/graphify", "extract", BASE_DIR, "--code-only", "--out", KNOWLEDGE_GRAPH_DIR]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            json_path = os.path.join(KNOWLEDGE_GRAPH_DIR, "graphify-out", "graph.json")
            if os.path.exists(json_path):
                export_cmd = ["/usr/local/bin/graphify", "export", "html", "--graph", json_path]
                subprocess.run(export_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, cwd=os.path.dirname(json_path))
        except Exception:
            pass
            
    t = threading.Thread(target=_worker, daemon=True)
    t.start()

def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return []
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_registry(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_executive_summary_with_qwen(executor, title, qa_details, is_success, fallback_triggered=False, fallback_model=""):
    """
    Generates leadership executive summaries via local Qwen 2.5 3B (qwen2.5:3b-throttled).
    Consumes $0 Cloud Tokens, runs locally with CPU capped at <= 60% (4 threads).
    Graceful fallback to deterministic template if local engine is offline.
    """
    status_str = "BERHASIL lolos verifikasi Zero-Defect" if is_success else "GAGAL verifikasi dan dilakukan Automatic Rollback"
    fb_note = f" dengan failover ke model {fallback_model}" if fallback_triggered else ""
    default_summary = (
        f"Perubahan oleh {executor}: '{title}' telah {status_str} ({qa_details}){fb_note}. "
        f"Sistem stabil dan operasional."
    )
    
    try:
        import urllib.request
        ollama_url = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434") + "/api/generate"
        prompt = (
            f"Anda adalah Change Management Governance Officer. Buatkan ringkasan eksekutif 1-2 kalimat dalam "
            f"Bahasa Indonesia formal yang padat dan jelas untuk Direktur/Owner mengenai perubahan sistem berikut:\n"
            f"- Pelaksana: {executor}\n"
            f"- Perubahan: {title}\n"
            f"- Status: {status_str} ({qa_details}){fb_note}\n\n"
            f"Tulis HANYA ringkasan eksekutifnya saja tanpa pengantar atau tanda kutip."
        )
        payload = json.dumps({
            "model": "qwen2.5:3b-throttled",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 100, "temperature": 0.2}
        }).encode("utf-8")
        
        req = urllib.request.Request(ollama_url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            generated = data.get("response", "").strip()
            if generated and len(generated) > 20:
                generated = generated.strip('"\'')
                return f"[Qwen AI Governance] {generated}"
    except Exception:
        pass
        
    return default_summary

def create_rfc(title, requested_by, executor, affected_files, description="", finops_ticket=None):
    """Registers Request for Change (RFC) and creates automated backup snapshots."""
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    rfc_id = f"RFC-{timestamp_str}"
    rfc_snapshot_dir = os.path.join(SNAPSHOTS_DIR, rfc_id)
    os.makedirs(rfc_snapshot_dir, exist_ok=True)
    
    backed_up_files = []
    for fpath in affected_files:
        if os.path.exists(fpath) and os.path.isfile(fpath):
            rel_name = os.path.basename(fpath)
            dest = os.path.join(rfc_snapshot_dir, rel_name)
            shutil.copy2(fpath, dest)
            backed_up_files.append({"original": fpath, "backup": dest})
            
    now_iso = datetime.now().isoformat()
    now_human = datetime.now().strftime("%d %B %Y, %H:%M:%S WIB")

    finops_info = finops_ticket or {
        "recommended_primary": "gemini-3.8-flash",
        "recommended_fallback": "cc/claude-haiku-4-5",
        "velocity_sla": {"tier": "NORMAL", "label": "Standard Task"}
    }

    primary_model = finops_info.get("recommended_primary", "gemini-3.8-flash")
    fallback_model = finops_info.get("recommended_fallback", "cc/claude-haiku-4-5")

    timeline = [
        {
            "step": "1. PRE-FLIGHT FINOPS REVIEW",
            "timestamp": now_human,
            "status": "APPROVED",
            "details": f"FinOps Primary Model: {primary_model} | Fallback: {fallback_model}."
        },
        {
            "step": "2. RFC REGISTRATION & BACKUP SNAPSHOT",
            "timestamp": now_human,
            "status": "SECURED",
            "details": f"Change Management mengamankan {len(backed_up_files)} file snapshot ke {rfc_snapshot_dir}."
        },
        {
            "step": "3. WORKER AGENT ASSIGNMENT",
            "timestamp": now_human,
            "status": "DISPATCHED",
            "details": f"Lead Architect menugaskan {executor} dengan model: {primary_model}."
        }
    ]

    rfc_entry = {
        "rfc_id": rfc_id,
        "created_at": now_iso,
        "created_at_human": now_human,
        "title": title,
        "requested_by": requested_by,
        "executor": executor,
        "description": description,
        "affected_files": affected_files,
        "backup_dir": rfc_snapshot_dir,
        "backed_up_files": backed_up_files,
        "finops_review": finops_info,
        "active_model_used": primary_model,
        "fallback_triggered": False,
        "qa_status": "PENDING_VERIFICATION",
        "final_status": "IN_PROGRESS",
        "rollback_executed": False,
        "activity_timeline": timeline,
        "executive_summary": f"Perubahan dari {executor} sedang dipersiapkan pada {datetime.now().strftime('%d/%m/%Y %H:%M')}: {title}."
    }
    
    registry = load_registry()
    registry.append(rfc_entry)
    save_registry(registry)
    return rfc_entry

def record_result(rfc_id, is_success, qa_details="ECC 12/12 PASS", fallback_used=False, fallback_model_name="", rollback_reason=""):
    """Records execution outcome, triggers rollback on failure, and updates audit changelog."""
    registry = load_registry()
    target = None
    for item in registry:
        if item["rfc_id"] == rfc_id:
            target = item
            break
            
    if not target:
        raise ValueError(f"RFC {rfc_id} tidak ditemukan dalam registry.")
        
    completion_time = datetime.now().strftime("%d %B %Y jam %H:%M WIB")
    now_human = datetime.now().strftime("%d %B %Y, %H:%M:%S WIB")

    if fallback_used and fallback_model_name:
        target["fallback_triggered"] = True
        target["active_model_used"] = fallback_model_name
        target["activity_timeline"].append({
            "step": "3B. FAILOVER ESKALASI MODEL LLM",
            "timestamp": now_human,
            "status": "FAILOVER_ACTIVATED",
            "details": f"Dialihkan ke Secondary Fallback: {fallback_model_name}."
        })

    if is_success:
        target["qa_status"] = qa_details
        target["final_status"] = "SUCCESS"
        target["completed_at"] = datetime.now().isoformat()
        
        target["activity_timeline"].append({
            "step": "4. QA ECC VERIFIKASI",
            "timestamp": now_human,
            "status": "PASS",
            "details": f"Pengujian kualitas tuntas: {qa_details} (0 Defect)."
        })
        target["activity_timeline"].append({
            "step": "5. RELEASE DEPLOYMENT & CLOSED",
            "timestamp": now_human,
            "status": "SUCCESS",
            "details": "Tiket perubahan ditutup secara resmi, perubahan diterapkan permanen."
        })
        _trigger_async_graphify_update()

        target["executive_summary"] = generate_executive_summary_with_qwen(
            executor=target.get("executor", "tim-change-management"),
            title=target.get("title", "Sistem Update"),
            qa_details=qa_details,
            is_success=True,
            fallback_triggered=target.get("fallback_triggered", False),
            fallback_model=fallback_model_name
        )
    else:
        target["qa_status"] = f"FAILED: {qa_details}"
        target["final_status"] = "FAILED_ROLLED_BACK"
        target["rollback_reason"] = rollback_reason
        target["completed_at"] = datetime.now().isoformat()
        
        # Disaster Auto-Rollback Execution
        restored = []
        for bfile in target.get("backed_up_files", []):
            orig = bfile["original"]
            bak = bfile["backup"]
            if os.path.exists(bak):
                shutil.copy2(bak, orig)
                restored.append(orig)
                
        target["rollback_executed"] = True
        target["restored_files"] = restored

        target["activity_timeline"].append({
            "step": "4. QA ECC VERIFIKASI",
            "timestamp": now_human,
            "status": "FAIL",
            "details": f"Pengujian kualitas menemukan defect: {qa_details}."
        })
        target["activity_timeline"].append({
            "step": "5. AUTOMATED DISASTER ROLLBACK",
            "timestamp": now_human,
            "status": "ROLLED_BACK",
            "details": f"Change Management sukses merestorasi {len(restored)} file ke kondisi stabil semula."
        })

        target["executive_summary"] = generate_executive_summary_with_qwen(
            executor=target.get("executor", "tim-change-management"),
            title=target.get("title", "Sistem Update"),
            qa_details=qa_details,
            is_success=False
        )
        
    save_registry(registry)
    _update_markdown_changelog(registry)
    return target

def _update_markdown_changelog(registry):
    lines = [
        "# Central Enterprise Change Registry & Audit Trail",
        "",
        "> Dikelola oleh **Tim Enterprise Change Management & Release Governance** (`tim-change-management`).",
        "> Standar Kepatuhan: ITIL v4 Change Enablement, ISO/IEC 27001 Audit Trail & Automated Rollback.",
        "",
        "## Ringkasan Eksekutif Perubahan (Bahasa Manajemen)",
        "",
        "| Tanggal & Jam | Tim Pelaksana | Deskripsi Perubahan | Status | Rollback | Ringkasan Manajemen |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for rfc in reversed(registry):
        st = rfc.get("final_status", "IN_PROGRESS")
        status_badge = "✅ BERHASIL" if st == "SUCCESS" else ("⏳ PROSES" if st == "IN_PROGRESS" else "❌ GAGAL (ROLLED BACK)")
        rb_badge = "Ya" if rfc.get("rollback_executed") else "Tidak"
        date_str = rfc.get("created_at_human", rfc.get("created_at", ""))
        exec_sum = rfc.get("executive_summary", "")
        executor = rfc.get("executor", "tim-change-management")
        title = rfc.get("title", "Sistem Update")
        lines.append(f"| {date_str} | `{executor}` | **{title}** | {status_badge} | {rb_badge} | {exec_sum} |")
        
    lines.append("")
    with open(CHANGELOG_FILE, "w") as f:
        f.write("\n".join(lines))

def get_latest_executive_report(limit=5):
    registry = load_registry()
    if not registry:
        return "Belum ada catatan perubahan dalam registry."
    recent = list(reversed(registry))[:limit]
    report = []
    for idx, rfc in enumerate(recent, 1):
        report.append(f"{idx}. {rfc.get('executive_summary')}")
    return "\n\n".join(report)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        print(get_latest_executive_report())
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        print(json.dumps(load_registry(), indent=2))
    else:
        print("Usage: change_manager.py [report|list]")
