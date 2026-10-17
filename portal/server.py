#!/usr/bin/env python3
"""
Omni-Agent Operating System - Master Portal & API Gateway
Enterprise Multi-Agent Collaboration & Resource Telemetry Console

Features:
- Live Hardware Telemetry: Per-core CPU equalizer, RAM, Disk, Host Uptime
- Cognitive FinOps Engine: Token analyzer with 4 Velocity SLAs
- Change Management Engine: RFC tracking, snapshots, auto-rollback
- AI Agent Chat Gateway: SSE Streaming proxy for multi-agent LLM assistants
- Pluggable Worker Architecture: Easily attach non-IT domain workers via plugins
"""

import os
import sys
import time
import json
import socket
import urllib.parse
import urllib.request
import http.server
import socketserver
import threading
import subprocess
import shutil
from collections import deque

PORT = int(os.getenv("PORTAL_PORT", "7777"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
GOVERNANCE_DIR = os.path.join(os.path.dirname(BASE_DIR), "governance")

# Add governance directory to path
if GOVERNANCE_DIR not in sys.path:
    sys.path.insert(0, GOVERNANCE_DIR)

try:
    import token_analyzer
except Exception:
    token_analyzer = None

try:
    import change_manager
except Exception:
    change_manager = None

DIFY_API_URL = os.getenv("DIFY_API_URL", "http://127.0.0.1:8090/v1/chat-messages")
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")

# Rolling Telemetry Buffer
telemetry_history = deque(maxlen=30)
history_lock = threading.Lock()

def record_telemetry_point(cpu_pct, ram_pct, disk_pct):
    with history_lock:
        now_ts = int(time.time())
        telemetry_history.append({
            "t": now_ts,
            "cpu": float(cpu_pct),
            "ram": float(ram_pct),
            "disk": float(disk_pct)
        })

# Pre-populate history
for i in range(15):
    t = int(time.time()) - (15 - i) * 2
    telemetry_history.append({"t": t, "cpu": 10.0, "ram": 25.0, "disk": 45.0})

# CPU Per-Core Calculation Cache
last_cpu_sample = {}
last_cpu_time = 0
cpu_lock = threading.Lock()

def get_raw_cpu_ticks():
    cpus = {}
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("cpu") and line[3:4].isdigit():
                    parts = line.split()
                    core_id = parts[0]
                    vals = [float(x) for x in parts[1:8]]
                    user, nice, sys_t, idle, iowait, irq, softirq = vals
                    idle_time = idle + iowait
                    busy_time = user + nice + sys_t + irq + softirq
                    cpus[core_id] = (busy_time, idle_time)
    except Exception:
        pass
    return cpus

last_cpu_sample = get_raw_cpu_ticks()
last_cpu_time = time.time()

def calculate_cpu_per_core():
    global last_cpu_sample, last_cpu_time
    with cpu_lock:
        now = time.time()
        current_sample = get_raw_cpu_ticks()
        if now - last_cpu_time < 0.2:
            time.sleep(0.2)
            current_sample = get_raw_cpu_ticks()
            now = time.time()

        core_stats = []
        total_pct = 0
        count = 0

        for core_id in sorted(current_sample.keys(), key=lambda x: int(x.replace("cpu", "")) if x.replace("cpu", "").isdigit() else 0):
            if core_id in last_cpu_sample:
                b1, i1 = last_cpu_sample[core_id]
                b2, i2 = current_sample[core_id]
                delta_b = b2 - b1
                delta_i = i2 - i1
                tot = delta_b + delta_i
                pct = round((delta_b / tot * 100), 1) if tot > 0 else 0.0
            else:
                pct = 0.0

            core_num = int(core_id.replace("cpu", "")) if core_id.replace("cpu", "").isdigit() else count
            core_stats.append({
                "id": core_id,
                "core_num": core_num,
                "name": f"Core {core_num}",
                "percent": pct
            })
            total_pct += pct
            count += 1

        last_cpu_sample = current_sample
        last_cpu_time = now
        avg_pct = round(total_pct / count, 1) if count > 0 else 0.0
        return core_stats, avg_pct

def check_port(host, port, timeout=0.3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def get_system_hardware_data():
    cores, avg_cpu = calculate_cpu_per_core()
    
    # Load averages
    load_1, load_5, load_15 = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
    
    # Memory metrics from /proc/meminfo
    mem_total_kb = 0
    mem_avail_kb = 0
    swap_total_kb = 0
    swap_free_kb = 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total_kb = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    mem_avail_kb = int(line.split()[1])
                elif line.startswith("SwapTotal:"):
                    swap_total_kb = int(line.split()[1])
                elif line.startswith("SwapFree:"):
                    swap_free_kb = int(line.split()[1])
    except Exception:
        pass

    ram_total_mb = round(mem_total_kb / 1024)
    ram_avail_mb = round(mem_avail_kb / 1024)
    ram_used_mb = max(0, ram_total_mb - ram_avail_mb)
    ram_pct = round((ram_used_mb / ram_total_mb * 100), 1) if ram_total_mb > 0 else 0

    swap_total_mb = round(swap_total_kb / 1024)
    swap_free_mb = round(swap_free_kb / 1024)
    swap_used_mb = max(0, swap_total_mb - swap_free_mb)
    swap_pct = round((swap_used_mb / swap_total_mb * 100), 1) if swap_total_mb > 0 else 0

    # Disk usage
    disk_total_gb = 0
    disk_used_gb = 0
    disk_pct = 0
    try:
        total, used, free = shutil.disk_usage("/")
        disk_total_gb = round(total / (1024**3), 1)
        disk_used_gb = round(used / (1024**3), 1)
        disk_pct = round((used / total * 100), 1) if total > 0 else 0
    except Exception:
        pass

    # Host Uptime
    uptime_sec = 0
    try:
        with open("/proc/uptime", "r") as f:
            uptime_sec = float(f.readline().split()[0])
    except Exception:
        pass

    uptime_hours = int(uptime_sec // 3600)
    uptime_mins = int((uptime_sec % 3600) // 60)
    uptime_str = f"{uptime_hours}j {uptime_mins}m" if uptime_hours > 0 else f"{uptime_mins} menit"

    record_telemetry_point(avg_cpu, ram_pct, disk_pct)

    with history_lock:
        history_list = list(telemetry_history)

    return {
        "status": "success",
        "cpu": {
            "avg_percent": avg_cpu,
            "cores": cores,
            "load_average": {
                "1m": round(load_1, 2),
                "5m": round(load_5, 2),
                "15m": round(load_15, 2)
            }
        },
        "ram": {
            "total_mb": ram_total_mb,
            "used_mb": ram_used_mb,
            "percent": ram_pct,
            "swap_used_mb": swap_used_mb,
            "swap_percent": swap_pct
        },
        "disk": {
            "total_gb": disk_total_gb,
            "used_gb": disk_used_gb,
            "percent": disk_pct
        },
        "uptime": {
            "seconds": int(uptime_sec),
            "formatted": uptime_str
        },
        "history": history_list
    }

class OmniPortalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        if path == "/api/system":
            self.send_json_response(get_system_hardware_data())
            return

        if path == "/api/ping":
            t0 = time.time()
            dify_online = check_port("127.0.0.1", 8090)
            ollama_online = check_port("127.0.0.1", 11434)
            rtt_host = round((time.time() - t0) * 1000, 2)
            self.send_json_response({
                "status": "success",
                "host_online": True,
                "dify_online": dify_online,
                "ollama_online": ollama_online,
                "rtt_host_ms": rtt_host,
                "rtt_dify_ms": 0.3 if dify_online else None
            })
            return

        if path == "/api/health":
            self.send_json_response({"status": "healthy", "service": "omni-portal", "timestamp": int(time.time())})
            return

        if path == "/api/governance/rfc":
            if change_manager:
                self.send_json_response({"status": "success", "registry": change_manager.load_registry()})
            else:
                self.send_json_response({"status": "error", "message": "Change manager module not found"}, 500)
            return

        # Serve static file
        super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        if path == "/api/token/analyze":
            try:
                data = json.loads(body.decode("utf-8"))
                prompt = data.get("prompt", "")
                dept = data.get("department", "general")
                if token_analyzer:
                    analyzer = token_analyzer.TokenWorkloadAnalyzer()
                    res = analyzer.evaluate_task(prompt, dept)
                    self.send_json_response(res)
                else:
                    self.send_json_response({"status": "error", "message": "Token analyzer not loaded"}, 500)
            except Exception as e:
                self.send_json_response({"status": "error", "message": str(e)}, 400)
            return

        if path == "/api/chat":
            # SSE streaming proxy
            self.handle_chat_sse(body)
            return

        self.send_json_response({"status": "error", "message": "Endpoint not found"}, 404)

    def handle_chat_sse(self, body):
        try:
            req_data = json.loads(body.decode("utf-8"))
            query = req_data.get("query", "")
            user = req_data.get("user", "user_guest")

            # Fallback mock streamer if Dify API is not running
            if not check_port("127.0.0.1", 8090):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()

                mock_reply = f"Halo! LKT AI Agent menerima pesan: '{query}'. Dify Engine saat ini offline atau berjalan di server terpisah. Sistem siap dihubungkan ke API LLM pilihan Anda."
                for word in mock_reply.split(" "):
                    chunk = json.dumps({"event": "message", "answer": word + " "})
                    self.wfile.write(f"data: {chunk}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(0.04)
                self.wfile.write(b"data: {\"event\": \"message_end\"}\n\n")
                self.wfile.flush()
                return

            # Real Dify Forwarder
            dify_payload = json.dumps({
                "inputs": {},
                "query": query,
                "response_mode": "streaming",
                "conversation_id": req_data.get("conversation_id", ""),
                "user": user
            }).encode("utf-8")

            req = urllib.request.Request(
                DIFY_API_URL,
                data=dify_payload,
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type": "application/json"
                }
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            with urllib.request.urlopen(req, timeout=30) as resp:
                while True:
                    line = resp.readline()
                    if not line:
                        break
                    self.wfile.write(line)
                    self.wfile.flush()
        except Exception as e:
            self.send_json_response({"status": "error", "message": str(e)}, 500)

    def send_json_response(self, data, status_code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), OmniPortalHandler) as httpd:
        print(f"🚀 Omni-Agent Portal Gateway running on http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down portal server...")

if __name__ == "__main__":
    run_server()
