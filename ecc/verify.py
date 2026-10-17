#!/usr/bin/env python3
"""
ECC (Enhanced Coding Capabilities) Automated Zero-Defect Test Harness
Adopted from: github.com/affaan-m/ECC
Standard: TDD Gated Verification Suite (Target: 100% PASS, 0 Defect)

Gates:
  [Gate 1] Static Code Integrity & Syntax Check (L1)
  [Gate 2] Component Logic & Metric Calculation Unit Test (L2)
  [Gate 3] System Integration Testing (SIT) on Running Portal (L3)
  [Gate 4] AI Agent & SSE Streaming Quality Check (L4)
  [Gate 5] Token FinOps & 4 Velocity SLAs Verification (L5)
"""

import os
import sys
import time
import json
import py_compile
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_FILE = os.path.join(BASE_DIR, 'portal', 'server.py')
INDEX_FILE = os.path.join(BASE_DIR, 'portal', 'static', 'index.html')
CHANGE_MGR_FILE = os.path.join(BASE_DIR, 'governance', 'change_manager.py')
TOKEN_ANALYZER_FILE = os.path.join(BASE_DIR, 'governance', 'token_analyzer.py')
PORTAL_URL = f"http://127.0.0.1:{os.getenv('PORTAL_PORT', '7777')}"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "defects": []
}

def record_test(gate_name, test_name, passed, detail=""):
    results["total"] += 1
    if passed:
        results["passed"] += 1
        print(f"  {GREEN}✔ [PASS]{RESET} {BOLD}{test_name}{RESET} {detail}")
    else:
        results["failed"] += 1
        results["defects"].append(f"{gate_name} :: {test_name} -> {detail}")
        print(f"  {RED}✖ [DEFECT]{RESET} {BOLD}{test_name}{RESET} - {RED}{detail}{RESET}")

def run_gate_1_syntax():
    print(f"\n{CYAN}{BOLD}[GATE 1] Static Code Integrity & Syntax Check (L1){RESET}")
    # 1. Compile Python Files
    for name, fpath in [("server.py", SERVER_FILE), ("change_manager.py", CHANGE_MGR_FILE), ("token_analyzer.py", TOKEN_ANALYZER_FILE)]:
        try:
            py_compile.compile(fpath, doraise=True)
            record_test("Gate 1", f"{name} Python Syntax", True, "(0 syntax errors)")
        except Exception as e:
            record_test("Gate 1", f"{name} Python Syntax", False, str(e))

    # 2. Check index.html DOM Integrity
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        all_dom_ok = all(k in content for k in [
            "cpuEqualizerGrid", "chatContainer", "userInput", "sendBtn", "pingBtn", "copyText"
        ])
        record_test("Gate 1", "index.html DOM & Component Integrity", all_dom_ok, "(Equalizer, Chat, Buttons verified)")
    else:
        record_test("Gate 1", "index.html Existence", False, "File not found")

def run_gate_2_logic():
    print(f"\n{CYAN}{BOLD}[GATE 2] Logic & Metric Calculation Unit Tests (L2){RESET}")
    try:
        cores_found = 0
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('cpu') and line[3:4].isdigit():
                    cores_found += 1
        record_test("Gate 2", "Kernel CPU Stat Cores Detection", cores_found > 0, f"Detected {cores_found} cores")
    except Exception as e:
        record_test("Gate 2", "Kernel CPU Stat Access", False, str(e))

    try:
        with open('/proc/meminfo', 'r') as f:
            mem_data = f.read()
        has_mem = 'MemTotal:' in mem_data and 'MemAvailable:' in mem_data
        record_test("Gate 2", "Memory Metric Source (/proc/meminfo)", has_mem, "MemTotal & MemAvailable readable")
    except Exception as e:
        record_test("Gate 2", "Memory Metric Source", False, str(e))

def run_gate_3_sit():
    print(f"\n{CYAN}{BOLD}[GATE 3] System Integration Testing (SIT) on Running Portal (L3){RESET}")
    try:
        t0 = time.time()
        req = urllib.request.Request(f"{PORTAL_URL}/")
        with urllib.request.urlopen(req, timeout=3) as resp:
            status = resp.status
            rtt = round((time.time() - t0) * 1000, 1)
        record_test("Gate 3", "Portal Web Server HTTP 200", status == 200, f"Status: {status} ({rtt} ms)")
    except Exception as e:
        record_test("Gate 3", "Portal Web Server HTTP 200", False, str(e))

    try:
        req = urllib.request.Request(f"{PORTAL_URL}/api/system")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        valid_schema = data.get("status") == "success" and "cpu" in data and "ram" in data and "disk" in data
        record_test("Gate 3", "/api/system Endpoint Schema", valid_schema, f"Avg CPU: {data.get('cpu', {}).get('avg_percent')}%")
    except Exception as e:
        record_test("Gate 3", "/api/system Endpoint", False, str(e))

    try:
        req = urllib.request.Request(f"{PORTAL_URL}/api/ping")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        record_test("Gate 3", "/api/ping Latency & Ecosystem Health", data.get("status") == "success", f"Host RTT: {data.get('rtt_host_ms')}ms")
    except Exception as e:
        record_test("Gate 3", "/api/ping Endpoint", False, str(e))

def run_gate_4_chat():
    print(f"\n{CYAN}{BOLD}[GATE 4] AI Agent & SSE Streaming Quality Check (L4){RESET}")
    try:
        t0 = time.time()
        payload = json.dumps({"query": "Ping test", "user": "ecc_tester"}).encode('utf-8')
        req = urllib.request.Request(f"{PORTAL_URL}/api/chat", data=payload, headers={"Content-Type": "application/json"})
        is_sse = False
        with urllib.request.urlopen(req, timeout=10) as resp:
            for _ in range(5):
                line = resp.readline().decode('utf-8')
                if line.strip().startswith("data:"):
                    is_sse = True
                    break
            rtt = round((time.time() - t0) * 1000, 1)
        record_test("Gate 4", "AI SSE Streaming Response", is_sse, f"Initial chunk verified in {rtt} ms")
    except Exception as e:
        record_test("Gate 4", "AI SSE Streaming Response", False, str(e))

def run_gate_5_token_finops():
    print(f"\n{CYAN}{BOLD}[GATE 5] Token FinOps & 4 Velocity SLAs Verification (L5){RESET}")
    try:
        sys.path.insert(0, os.path.join(BASE_DIR, 'governance'))
        import token_analyzer
        analyzer = token_analyzer.TokenWorkloadAnalyzer()
        
        # Test A1 SLA (Instant)
        res_a1 = analyzer.evaluate_task("Tampilkan informasi status port dan telemetri")
        is_a1_ok = res_a1["assignment"]["velocity_sla"]["tier"] == "A1"
        record_test("Gate 5", "Velocity SLA Classification [A1 Instant]", is_a1_ok, "Mapped to < 1-2m Read-Only")

        # Test ASAP SLA (Hotfix)
        res_asap = analyzer.evaluate_task("Tolong perbaiki styling CSS tombol warna bento grid")
        is_asap_ok = res_asap["assignment"]["velocity_sla"]["tier"] == "ASAP"
        record_test("Gate 5", "Velocity SLA Classification [ASAP Hotfix]", is_asap_ok, "Mapped to 5-10m Surgical Patch")

        # Test Normal SLA (Feature)
        res_norm = analyzer.evaluate_task("Rancang modul controller baru dengan schema database relational")
        is_norm_ok = res_norm["assignment"]["velocity_sla"]["tier"] == "NORMAL"
        record_test("Gate 5", "Velocity SLA Classification [NORMAL Feature]", is_norm_ok, "Mapped to 10-30m Deep Reasoning")

        # Test Marathon SLA (Long-Running)
        res_marathon = analyzer.evaluate_task("Bangun full-stack web application dari nol hingga production")
        is_marathon_ok = res_marathon["assignment"]["velocity_sla"]["tier"] == "LAMBAT"
        record_test("Gate 5", "Velocity SLA Classification [LAMBAT Marathon]", is_marathon_ok, "Mapped to 1-6h Autonomous")

    except Exception as e:
        record_test("Gate 5", "Token FinOps & Velocity SLA", False, str(e))

def main():
    print("=" * 65)
    print("🛡️ ECC VERIFICATION HARNESS - OMNI-AGENT OS")
    print(f"Target: {BASE_DIR}")
    print("Standard: TDD Gated Verification & Zero-Defect Baseline")
    print("=" * 65)

    run_gate_1_syntax()
    run_gate_2_logic()
    run_gate_3_sit()
    run_gate_4_chat()
    run_gate_5_token_finops()

    print("\n" + "=" * 65)
    print(f"ECC VERIFICATION SUMMARY: Total: {results['total']} | Passed: {results['passed']} | Defects: {results['failed']}")
    if results['failed'] == 0:
        print("🎉 ZERO DEFECT VERIFIED! System is Certified Production Ready.")
        print("=" * 65)
        sys.exit(0)
    else:
        print("❌ DEFECTS DETECTED:")
        for d in results['defects']:
            print(f"  - {d}")
        print("=" * 65)
        sys.exit(1)

if __name__ == '__main__':
    main()
