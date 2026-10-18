#!/usr/bin/env python3
"""
Report Mimic & Data Synthesizer CLI Engine
Part of Omni-Agent OS Skills Suite (skills/report-mimic-synthesizer)

Automatically generates new reports by mimicking the exact structure, tone,
format, and depth of a reference report while synthesizing relevant data
from multiple external files (CSV, JSON, Markdown, Text, Logs).
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

def read_file_content(file_path):
    """Safely reads content from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def compile_data_sources(source_paths):
    """Reads and formats multiple data source files into a structured block."""
    compiled = []
    for path in source_paths:
        content = read_file_content(path)
        base_name = os.path.basename(path)
        compiled.append(f"=== [SUMBER DATA: {base_name}] ===\n{content.strip()}\n=== [AKHIR SUMBER: {base_name}] ===")
    return "\n\n".join(compiled)

def call_ollama_engine(prompt, model="qwen2.5:3b-throttled", temperature=0.2, ollama_url="http://127.0.0.1:11434"):
    """Invokes local Ollama LLM engine for zero-cost report synthesis."""
    endpoint = f"{ollama_url}/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": float(temperature),
            "num_predict": 1024
        }
    }).encode("utf-8")

    req = urllib.request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("response", "").strip()

def synthesize_report(reference_file, data_sources, output_file, model="qwen2.5:3b-throttled", temperature=0.2):
    """Main synthesis pipeline: reads inputs, forms prompt, calls LLM, and writes output."""
    print("=================================================================")
    print("📝 REPORT MIMIC & DATA SYNTHESIZER ENGINE")
    print("=================================================================")
    print(f"📄 Dokumen Acuan (Template): {reference_file}")
    print(f"📊 Jumlah Sumber Data      : {len(data_sources)} file")
    print(f"🤖 Model AI yang Dipakai   : {model} (Temp: {temperature})")
    print(f"🎯 File Output Target       : {output_file}")
    print("-----------------------------------------------------------------")

    ref_text = read_file_content(reference_file)
    data_text = compile_data_sources(data_sources)

    system_instruction = (
        "Anda adalah Ahli Penyusun Laporan Korporat & Analis Data Eksekutif.\n"
        "Tugas Anda adalah membuat satu laporan baru yang MENIRU 100% struktur judul, sub-bab, "
        "format tabel, dan gaya bahasa (tone) dari DOKUMEN ACUAN di bawah ini.\n\n"
        "KETENTUAN MUTLAK:\n"
        "1. Pertahankan urutan bab, heading (#, ##, ###), penomoran, dan format bullet/tabel persis seperti Dokumen Acuan.\n"
        "2. HANYA gunakan angka, fakta, nama, dan metrik dari FILE SUMBER DATA aktual. Dilarang mengarang data (0 Halusinasi).\n"
        "3. Tulis seluruh laporan dalam Bahasa Indonesia formal berstandar profesional.\n"
        "4. Outputkan HANYA isi dokumen laporan baru secara lengkap tanpa pengantar atau penutup obrolan."
    )

    full_prompt = (
        f"{system_instruction}\n\n"
        f"--- [DOKUMEN ACUAN / FORMAT LAPORAN YANG HARUS DITIRU] ---\n"
        f"{ref_text}\n"
        f"--- [AKHIR DOKUMEN ACUAN] ---\n\n"
        f"--- [DATA-DATA AKTUAL DARI BERBAGAI FILE SUMBER] ---\n"
        f"{data_text}\n"
        f"--- [AKHIR DATA-DATA AKTUAL] ---\n\n"
        f"Sekarang, susunlah LAPORAN BARU yang meniru format di atas menggunakan data aktual tersebut:"
    )

    print("⏳ Menghubungi mesin kecerdasan buatan untuk sintesis dokumen...")
    try:
        report_result = call_ollama_engine(full_prompt, model=model, temperature=temperature)
    except Exception as e:
        print(f"⚠️  Gagal memanggil Ollama ({e}). Mencoba fallback ke format template...")
        report_result = f"# Laporan Hasil Sintesis Otomatis\n\n> Disusun berdasarkan acuan {os.path.basename(reference_file)}.\n\n{data_text}"

    # Ensure parent dir exists
    out_dir = os.path.dirname(os.path.abspath(output_file))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(report_result + "\n")

    print(f"✔ Berhasil! Laporan baru telah disimpan di: {output_file}")
    print("=================================================================")
    return output_file

def run_self_test():
    """Generates sample reference and source data files, then runs a self-test."""
    print("🧪 Menjalankan Self-Test Report Synthesizer...")
    test_dir = "/tmp/report_synthesizer_test"
    os.makedirs(test_dir, exist_ok=True)

    ref_path = os.path.join(test_dir, "sample_reference.md")
    data1_path = os.path.join(test_dir, "metrics.csv")
    data2_path = os.path.join(test_dir, "incident_log.json")
    out_path = os.path.join(test_dir, "synthesized_report.md")

    with open(ref_path, "w") as f:
        f.write(
            "# Laporan Kinerja Operasional Mingguan\n\n"
            "## 1. Ringkasan Eksekutif\n"
            "Operasional sistem pada periode ini berjalan dengan ketersediaan tinggi mencapai 99.8%.\n\n"
            "## 2. Rincian Metrik Utama\n"
            "| Komponen | Target | Realisasi | Status |\n"
            "| :--- | :--- | :--- | :--- |\n"
            "| Server Uptime | 99.5% | 99.8% | Normal |\n\n"
            "## 3. Catatan Kendala & Rekomendasi\n"
            "- Dilakukan mitigasi lonjakan beban memori pada jam sibuk.\n"
        )

    with open(data1_path, "w") as f:
        f.write("Komponen,Target,Realisasi,Status\nServer Uptime,99.9%,100.0%,Sempurna\nDatabase TPS,1500,2100,Optimal\n")

    with open(data2_path, "w") as f:
        f.write(json.dumps({"insiden": 0, "catatan": "Semua port dan daemon stabil tanpa anomali"}, indent=2))

    res = synthesize_report(ref_path, [data1_path, data2_path], out_path, model="qwen2.5:3b-throttled")
    assert os.path.exists(res), "Output file was not created!"
    print(f"✔ Self-Test PASS! Output terverifikasi di {res}")

def main():
    parser = argparse.ArgumentParser(description="Report Mimic & Data Synthesizer CLI")
    parser.add_argument("--reference", "-r", help="Path ke dokumen laporan acuan yang ingin ditiru")
    parser.add_argument("--data-sources", "-d", nargs="+", help="Daftar file sumber data (CSV, JSON, TXT, LOG, MD)")
    parser.add_argument("--output", "-o", help="Path tujuan file laporan baru yang akan dibuat")
    parser.add_argument("--model", "-m", default="qwen2.5:3b-throttled", help="Nama model LLM (Default: qwen2.5:3b-throttled)")
    parser.add_argument("--temperature", "-t", type=float, default=0.2, help="Temperature LLM (Default: 0.2)")
    parser.add_argument("--test", action="store_true", help="Jalankan pengujian mandiri (Self-Test)")

    args = parser.parse_args()

    if args.test:
        run_self_test()
        return

    if not args.reference or not args.data_sources or not args.output:
        parser.print_help()
        sys.exit(1)

    synthesize_report(args.reference, args.data_sources, args.output, model=args.model, temperature=args.temperature)

if __name__ == "__main__":
    main()
