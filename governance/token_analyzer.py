#!/usr/bin/env python3
"""
AI Token FinOps & Workload Governance Engine (tim-ai-finops)
Analyzes cognitive workload, token weight, and automatically assigns optimal LLM models across 4 Velocity SLAs.
Prevents token exhaustion and maximizes ROI/accuracy trade-off.
"""

import sys
import json
import re
import os

# Model Catalog & Pricing/Weight Multipliers (Normalized scale)
MODEL_CATALOG = {
    "custom-vision": {
        "provider": "Vision Lentera",
        "tier": "Tier 1: Fast Utility (Vision Lentera)",
        "relative_cost": 2.0,
        "speed_rating": "Ultra Fast (~250ms)",
        "context_window": "200,000 tokens",
        "best_for": "Quick lookups, status checks, speedtests, UI chat, and high-frequency queries."
    },
    "gemini-3.8-flash": {
        "provider": "Google",
        "tier": "Tier 1: Micro/Fast",
        "relative_cost": 1.0,
        "speed_rating": "Ultra Fast (~250ms)",
        "context_window": "1,000,000 tokens",
        "best_for": "Quick lookups, status checks, speedtests, UI chat, and high-frequency queries."
    },
    "cc/claude-haiku-4-5": {
        "provider": "Vision Lentera",
        "tier": "Tier 2: Fast Utility",
        "relative_cost": 3.0,
        "speed_rating": "Fast (~1.2s)",
        "context_window": "200,000 tokens",
        "best_for": "Medium summaries, log parsing, straightforward scripts, communications."
    },
    "enhance-think": {
        "provider": "Vision Lentera",
        "tier": "Tier 3: Deep Reasoning (CoT)",
        "relative_cost": 7.5,
        "speed_rating": "Thoughtful (~3.0s)",
        "context_window": "High Context",
        "best_for": "Complex reasoning, multi-step problem solving, correlation analysis."
    },
    "powerfull-combo": {
        "provider": "Vision Lentera",
        "tier": "Tier 3: Strategic Combo",
        "relative_cost": 8.0,
        "speed_rating": "Thoughtful (~3.2s)",
        "context_window": "High Context",
        "best_for": "System evaluations, architecture trade-offs, complex orchestration."
    },
    "cc/claude-sonnet-5": {
        "provider": "Vision Lentera",
        "tier": "Tier 4: Heavyweight / Zero-Defect",
        "relative_cost": 12.0,
        "speed_rating": "Deliberate (~2.8s)",
        "context_window": "1,000,000 tokens",
        "best_for": "ECC automated verification, zero-defect refactoring, complex multi-file architecture."
    },
    "qwen2.5:3b": {
        "provider": "Ollama (Local On-Premise)",
        "tier": "Tier 3: Local Safety Net & Recurring Batch",
        "relative_cost": 0.0,
        "speed_rating": "Fast CPU (~18-22 t/s)",
        "context_window": "32,000 tokens",
        "best_for": "Local fallback, background batch processing, log parsing, zero-cost offline operations."
    }
}

class TokenWorkloadAnalyzer:
    def __init__(self):
        self.patterns = {
            "critical_code": re.compile(r'\b(refactor|bug|defect|zero defect|ecc|tdd|unit test|segfault|race condition|architecture|memory leak)\b', re.IGNORECASE),
            "feature_development": re.compile(r'\b(rancang|buatkan|modul|controller|fitur|schema|database|relational|integrasi|arsitektur|backend|api)\b', re.IGNORECASE),
            "deep_analysis": re.compile(r'\b(audit|analisa|compliance|baseline|deep|strategi|evaluasi|korelasi)\b', re.IGNORECASE),
            "data_summary": re.compile(r'\b(ringkas|summarize|analisa log|rekap|tabel|laporan|csv|telemetri)\b', re.IGNORECASE),
            "simple_lookup": re.compile(r'\b(ping|speedtest|port|status|halo|hai|cek ram|cek cpu|uptime|siapa|apa itu)\b', re.IGNORECASE)
        }

    def estimate_tokens(self, text):
        if not text:
            return 0
        return max(1, int(len(text) / 3.2))

    def evaluate_task(self, prompt, target_department="general", context_length=0):
        prompt_len = len(prompt)
        prompt_tokens = self.estimate_tokens(prompt)
        total_tokens = prompt_tokens + context_length

        # 1. Base Score from Token Length
        if total_tokens < 300:
            length_score = 1
        elif total_tokens < 1500:
            length_score = 2
        elif total_tokens < 6000:
            length_score = 4
        else:
            length_score = 6

        # 2. Intent Complexity Scoring
        intent_type = "GENERAL_CONVERSATION"
        intent_score = 2

        if self.patterns["critical_code"].search(prompt) or target_department in ("qa_ecc", "core_gateway", "tim-qa-testing", "agent-dev-lead-architect"):
            intent_type = "ZERO_DEFECT_CODE_OR_ECC"
            intent_score = 8
        elif self.patterns["feature_development"].search(prompt):
            intent_type = "FEATURE_DEVELOPMENT_OR_INTEGRATION"
            intent_score = 7
        elif self.patterns["deep_analysis"].search(prompt):
            intent_type = "DEEP_ANALYTICAL_WORKLOAD"
            intent_score = 6
        elif self.patterns["data_summary"].search(prompt):
            intent_type = "DATA_SYNTHESIS_AND_LOGS"
            intent_score = 4
        elif self.patterns["simple_lookup"].search(prompt) or target_department in ("hardware_telemetry", "ui_ux", "tim-infra-sre", "tim-uiux-spatial"):
            intent_type = "SYSTEM_LOOKUP_AND_STATUS"
            intent_score = 1

        # Composite Cognitive Weight
        if intent_score >= 7:
            cognitive_weight = max(intent_score, int((length_score * 0.3) + (intent_score * 0.7)))
        else:
            cognitive_weight = min(10, max(1, int((length_score * 0.4) + (intent_score * 0.6))))

        # 2B. Velocity SLA Classification (A1, ASAP, Normal/Medium, Lambat/Marathon)
        is_marathon = bool(re.search(r'\b(full-stack|dari nol|0 sampai|0 hingga|marathon|seluruh sistem|end-to-end)\b', prompt, re.IGNORECASE))
        is_read_only = bool(re.search(r'\b(siapa|apa|info|cek|status|ping|topologi|ip|port|log|history|uptime|tampilkan)\b', prompt, re.IGNORECASE)) and not bool(re.search(r'\b(buat|ubah|edit|ganti|tambah|update|refactor|hapus|fix|perbaiki|install)\b', prompt, re.IGNORECASE))
        is_micro_patch = bool(re.search(r'\b(css|styling|warna|padding|margin|typo|tulisan|tombol|button|tweak|layout|static height)\b', prompt, re.IGNORECASE))

        if is_marathon or (cognitive_weight >= 8 and total_tokens > 2000):
            velocity_sla = {
                "tier": "LAMBAT",
                "label": "Autonomous Marathon (1 - 6 Jam)",
                "eta_range": "1 - 6 Jam",
                "qa_strategy": "Multi-Stage Gated Verification + Milestone Heartbeat",
                "finops_strategy": "Hybrid Cascade (Tier 2 Architect + Tier 1 Coder + Tier 3 Qwen Local Batch Parsing)"
            }
        elif is_read_only and cognitive_weight <= 3:
            velocity_sla = {
                "tier": "A1",
                "label": "Instant Telemetry & Query (< 1-2 Menit)",
                "eta_range": "< 1 - 2 Menit",
                "qa_strategy": "Bypass QA SIT/UAT & RFC Snapshot (Instant Zero-Overhead)",
                "finops_strategy": "Tier 1 Fast Cloud atau Tier 3 Qwen Lokal ($0 Token)"
            }
        elif is_micro_patch or cognitive_weight <= 4:
            velocity_sla = {
                "tier": "ASAP",
                "label": "Quick Hotfix & Micro-Patch (5 - 10 Menit)",
                "eta_range": "5 - 10 Menit",
                "qa_strategy": "Targeted Smoke Test (RFC Snapshot + Gate 1-3 ECC)",
                "finops_strategy": "Tier 1 Cloud (Primary) -> Tier 2 Haiku (Failover)"
            }
        else:
            velocity_sla = {
                "tier": "NORMAL",
                "label": "Deep Feature & Core Refactor (10 - 30 Menit)",
                "eta_range": "10 - 30 Menit",
                "qa_strategy": "Full 6-Gate ECC (12/12 PASS Zero-Defect) + Snapshot Rollback",
                "finops_strategy": "Tier 2 Flagship Reasoning (Strategic Combo / Sonnet 5)"
            }

        # 3. Model Recommendations
        use_dynamic_vision = True
        try:
            active_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "active_mode.json")
            if os.path.exists(active_file):
                with open(active_file, "r") as af:
                    adata = json.load(af)
                    if adata.get("mode") == "STATIC":
                        use_dynamic_vision = False
        except Exception:
            pass

        primary_model = "custom-vision" if use_dynamic_vision else "gemini-3.8-flash"
        secondary_model = "enhance-think" if use_dynamic_vision else "cc/claude-haiku-4-5"
        tertiary_model = "cc/claude-sonnet-5"
        primary_rationale = ""
        fallback_trigger = ""

        if cognitive_weight <= 3:
            if use_dynamic_vision:
                primary_model = "custom-vision"
                secondary_model = "enhance-think"
                primary_rationale = "Tugas operasional ringan. Alokasi ke Fast Utility untuk sub-second latency."
                fallback_trigger = "Eskalasi ke Secondary jika parsing data tidak lengkap."
            else:
                primary_model = "gemini-3.8-flash"
                secondary_model = "cc/claude-haiku-4-5"
                primary_rationale = "Tugas ringan operasional. Efisiensi token hingga ~92%."
                fallback_trigger = "Eskalasi ke Secondary jika response timeout (>3s)."
        elif cognitive_weight <= 5:
            primary_model = "cc/claude-haiku-4-5"
            secondary_model = "enhance-think"
            primary_rationale = "Tugas berbobot sedang (sintesis data/skrip). Presisi sintaks tinggi."
            fallback_trigger = "Eskalasi ke Secondary jika diperlukan CoT lebih mendalam."
        elif cognitive_weight <= 7:
            primary_model = "enhance-think"
            secondary_model = "cc/claude-sonnet-5"
            primary_rationale = "Tugas analitis tinggi. Membutuhkan chain-of-thought mendalam."
            fallback_trigger = "Eskalasi ke Secondary jika verifikasi multi-file diperlukan."
        else:
            primary_model = "cc/claude-sonnet-5"
            secondary_model = "powerfull-combo"
            primary_rationale = "Tugas berbobot kritis (Verifikasi Zero-Defect / Arsitektur Inti)."
            fallback_trigger = "Eskalasi ke Secondary jika konsensus multi-perspektif dibutuhkan."

        multi_tier_recommendations = [
            {
                "level": "Level 1 (Primary - Rekomendasi Utama)",
                "model": primary_model,
                "tier": MODEL_CATALOG[primary_model]["tier"],
                "speed": MODEL_CATALOG[primary_model]["speed_rating"],
                "relative_cost": MODEL_CATALOG[primary_model]["relative_cost"],
                "role": "Model awal yang dieksekusi pertama kali.",
                "rationale": primary_rationale
            },
            {
                "level": "Level 2 (Secondary - Fallback / Failover)",
                "model": secondary_model,
                "tier": MODEL_CATALOG[secondary_model]["tier"],
                "speed": MODEL_CATALOG[secondary_model]["speed_rating"],
                "relative_cost": MODEL_CATALOG[secondary_model]["relative_cost"],
                "role": "Model cadangan jika model pertama gagal atau timeout.",
                "failover_condition": fallback_trigger
            },
            {
                "level": "Level 3 (Tertiary - Deep Escalation)",
                "model": tertiary_model,
                "tier": MODEL_CATALOG[tertiary_model]["tier"],
                "speed": MODEL_CATALOG[tertiary_model]["speed_rating"],
                "relative_cost": MODEL_CATALOG[tertiary_model]["relative_cost"],
                "role": "Model eskalasi puncak jika defect berulang."
            }
        ]

        heavyweight_cost = MODEL_CATALOG["cc/claude-sonnet-5"]["relative_cost"]
        current_cost = MODEL_CATALOG[primary_model]["relative_cost"]
        savings_vs_max = round((1 - (current_cost / heavyweight_cost)) * 100, 1)

        return {
            "status": "success",
            "prompt_sample": prompt[:80] + ("..." if len(prompt) > 80 else ""),
            "metrics": {
                "estimated_tokens": total_tokens,
                "target_department": target_department,
                "intent_classification": intent_type,
                "cognitive_weight_score": cognitive_weight,
                "velocity_sla": velocity_sla
            },
            "assignment": {
                "recommended_model": primary_model,
                "velocity_sla": velocity_sla,
                "projected_token_savings": f"{savings_vs_max}% hemat token dibanding eksekusi langsung di flagship model"
            },
            "finops_guidance": {
                "recommended_primary": primary_model,
                "recommended_fallback": secondary_model,
                "multi_tier_models": multi_tier_recommendations,
                "projected_primary_savings": f"{savings_vs_max}% hemat token dibanding eksekusi langsung di flagship model"
            }
        }

def main():
    analyzer = TokenWorkloadAnalyzer()
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        custom_prompt = sys.argv[1]
        dept = "general"
        for i, arg in enumerate(sys.argv):
            if arg == "--dept" and i + 1 < len(sys.argv):
                dept = sys.argv[i + 1]
        
        res = analyzer.evaluate_task(custom_prompt, dept)
        m = res["metrics"]
        fg = res["finops_guidance"]
        v = m["velocity_sla"]
        print("=" * 75)
        print("🏛️ AI TOKEN FINOPS & WORKLOAD GOVERNANCE - SPRINT ASSIGNMENT REPORT")
        print("=" * 75)
        print(f"\n[Task] \"{custom_prompt}\"")
        print(f"  • Dept Assigned: {m['target_department']} | Intent: {m['intent_classification']}")
        print(f"  • Bobot Kognitif: {m['cognitive_weight_score']}/10 | Est Input Tokens: ~{m['estimated_tokens']}")
        print(f"  • Velocity SLA: \033[1m\033[96m[{v['tier']}] {v['label']}\033[0m")
        print(f"  • QA Strategy: {v['qa_strategy']}")
        print(f"  • Efisiensi: {fg['projected_primary_savings']}")
        print("\n  🎯 REKOMENDASI MULTI-TIER LLM:")
        for rec in fg["multi_tier_models"]:
            print(f"    ▶ {rec['level']}: \033[1m\033[92m{rec['model']}\033[0m ({rec['tier']})")
        print("=" * 75)
        return

    print("Usage: python3 token_analyzer.py \"<prompt>\" [--dept <name>]")

if __name__ == '__main__':
    main()
