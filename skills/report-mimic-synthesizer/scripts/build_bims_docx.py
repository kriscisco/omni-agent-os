#!/usr/bin/env python3
"""
build_bims_docx.py
Generates an editable, professionally formatted Word (.docx) document
for the BIMS / Rekapitulasi Budget FR - Estate Penetration Testing Report,
matching the bilingual format and executive styling of Lentera Teknologi.
"""

import sys
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    # Remove existing shd if any
    for child in list(tc_pr):
        if child.tag.endswith('shd'):
            tc_pr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    """Sets subtle table borders."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def add_bilingual_section(doc, en_paragraphs, id_paragraphs, en_header="English", id_header="Bahasa Indonesia"):
    """Creates a dual-column bilingual table (English left, Bahasa Indonesia right)."""
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # 7.5 inches printable width total -> 3.75 in each
    col_width = Inches(3.75)
    for row in table.rows:
        for cell in row.cells:
            cell.width = col_width
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    # Header Row
    cell_en_h = table.cell(0, 0)
    set_cell_background(cell_en_h, "E0F2FE") # Soft Sky Blue
    p_en_h = cell_en_h.paragraphs[0]
    p_en_h.paragraph_format.space_before = Pt(2)
    p_en_h.paragraph_format.space_after = Pt(2)
    r_en_h = p_en_h.add_run(en_header)
    r_en_h.bold = True
    r_en_h.font.size = Pt(9.5)
    r_en_h.font.color.rgb = RGBColor(0x03, 0x69, 0xA1)

    cell_id_h = table.cell(0, 1)
    set_cell_background(cell_id_h, "D1FAE5") # Soft Mint Green
    p_id_h = cell_id_h.paragraphs[0]
    p_id_h.paragraph_format.space_before = Pt(2)
    p_id_h.paragraph_format.space_after = Pt(2)
    r_id_h = p_id_h.add_run(id_header)
    r_id_h.bold = True
    r_id_h.font.size = Pt(9.5)
    r_id_h.font.color.rgb = RGBColor(0x04, 0x78, 0x57)

    # Content Row
    cell_en_c = table.cell(1, 0)
    set_cell_background(cell_en_c, "F8FAFC")
    for i, p_text in enumerate(en_paragraphs):
        p = cell_en_c.paragraphs[0] if i == 0 else cell_en_c.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        # Parse simple bold markdown
        format_runs(p, p_text)

    cell_id_c = table.cell(1, 1)
    set_cell_background(cell_id_c, "FFFFFF")
    for i, p_text in enumerate(id_paragraphs):
        p = cell_id_c.paragraphs[0] if i == 0 else cell_id_c.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        format_runs(p, p_text)

    set_table_borders(table, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def format_runs(paragraph, text):
    """Parses simple inline bold markers (**text**) and code markers (`code`)."""
    import re
    # Split by bold or code tokens
    parts = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        elif part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        else:
            run = paragraph.add_run(part)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

def add_terminal_box(doc, text):
    """Creates a dark slate code terminal box for PoC command evidence."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.rows[0].cells[0].width = Inches(7.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "0F172A") # Slate 900
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGBColor(0xF8, 0xFA, 0xFC)
    
    set_table_borders(table, color="334155", sz="6")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def generate_docx(output_path):
    doc = Document()
    
    # Set page layout: A4 with 0.5 inch (36 pt) margins for wide readable split
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("LENTERA TEKNOLOGI | BIMS FR Estate — Internal Web Pentest Report (Editable)")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(7.5)
        hrun.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun1 = fp.add_run("CONFIDENTIAL ")
        frun1.bold = True
        frun1.font.name = "Arial"
        frun1.font.size = Pt(7.5)
        frun1.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
        
        frun2 = fp.add_run("— Internal Security Assessment Report | Non-Destructive OWASP Top 10 Single-Pass")
        frun2.font.name = "Arial"
        frun2.font.size = Pt(7.5)
        frun2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # -------------------------------------------------------------
    # COVER / HEADER
    # -------------------------------------------------------------
    p_org = doc.add_paragraph()
    p_org.paragraph_format.space_before = Pt(0)
    p_org.paragraph_format.space_after = Pt(2)
    r_org = p_org.add_run("LENTERA TEKNOLOGI — CYBER SECURITY ASSESSMENT SERVICE")
    r_org.bold = True
    r_org.font.name = "Arial"
    r_org.font.size = Pt(10.5)
    r_org.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("INTERNAL WEB PENETRATION TESTING REPORT — 18 OKTOBER 2026")
    r_sub.bold = True
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Metadata Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.rows[0].cells[0].width = Inches(2.0)
    meta_table.rows[0].cells[1].width = Inches(5.5)

    meta_rows = [
        ("Target System", "Rekapitulasi Budget FR - Estate (BIMS) — https://rekapbudget-estate.first-resources.com / 10.110.1.9:1627"),
        ("DNS / Routing", "CNAME lkt-infra.first-resources.com -> A 10.100.2.64 (Reverse Proxy)"),
        ("Assessment Scope", "Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran)"),
        ("Attacker / Audit Node", "Internal Workstation Node (Linux Security Subsystem / RFC1918 Scope)"),
        ("Access Level Tested", "Unauthenticated Access & Controlled Dummy Credential Authentication Probe"),
        ("Classification", "CONFIDENTIAL — INTERNAL ENTERPRISE SECURITY ASSESSMENT")
    ]

    for i, (k, v) in enumerate(meta_rows):
        c0 = meta_table.cell(i, 0)
        c1 = meta_table.cell(i, 1)
        c0.width = Inches(2.0)
        c1.width = Inches(5.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=120, right=120)
        set_cell_margins(c1, top=60, bottom=60, left=120, right=120)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(v)
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        if k == "Classification":
            r1.bold = True
            r1.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
        else:
            r1.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    set_table_borders(meta_table, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Helper for Section Titles
    def add_section_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    def add_section_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # -------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    add_section_h1("1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF")
    en_exec = [
        "On 18 October 2026, a focused, non-destructive internal web penetration test was conducted against the **BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate** web application.",
        "Assessment targeted both the public HTTPS hostname (`https://rekapbudget-estate.first-resources.com` resolving to `10.100.2.64`) and the direct internal server instance (`http://10.110.1.9:1627`). Testing strictly adhered to an anti-loop linear single-pass methodology aligned with OWASP Top 10 standards.",
        "The principal high-risk finding is **F-01: Plaintext HTTP Transport on Internal Login Endpoint (Port 1627)**. Server `10.110.1.9:1627` runs an unencrypted HTTP/1.0 service (`Server: RBFR`) exposing an active login form (`POST /masuk`), placing credentials and session tokens at risk of eavesdropping and interception within internal RFC1918 networks.",
        "Additional configuration weaknesses include **F-02: Permissive Content Security Policy with `unsafe-inline`** and **F-03: Redundant & Conflicting Security Headers** resulting from proxy layering. Perimeter defenses on HTTPS showed valid Sectigo wildcard certificates, HSTS enforcement, and standard 401 dummy auth rejection.",
        "**Overall Assessment:** The evidence supports **1 High-Risk finding** and **2 Configuration Weaknesses**. Post-login cookie flags and internal IDOR remain unverified due to single-pass constraints."
    ]
    id_exec = [
        "Pada 18 Oktober 2026 dilakukan pengujian penetrasi web internal non-destruktif terhadap sistem **BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate**.",
        "Pengujian mencakup hostname publik (`https://rekapbudget-estate.first-resources.com` ter-resolve ke `10.100.2.64`) dan instans server internal langsung (`http://10.110.1.9:1627`). Pengujian menerapkan alur linear satu putaran bebas macet sesuai standar OWASP Top 10.",
        "Temuan utama berisiko tinggi adalah **F-01: Transport Plaintext HTTP pada Endpoint Login Internal (Port 1627)**. Host `10.110.1.9:1627` menjalankan layanan HTTP/1.0 tanpa enkripsi (`Server: RBFR`) yang menyajikan form login (`POST /masuk`), membuka celah penyadapan kredensial dan sesi di jaringan lokal.",
        "Ditemukan pula dua kelemahan konfigurasi: **F-02: CSP Permisif (`unsafe-inline`)** dan **F-03: Duplikasi Header Keamanan** akibat layering proxy. Sisi perimeter HTTPS terverifikasi kuat dengan sertifikat wildcard Sectigo valid, HSTS aktif, serta penolakan login dummy 401.",
        "**Kesimpulan Umum:** Hasil mendukung **1 Temuan High** dan **2 Kelemahan Konfigurasi**. Atribut cookie sesi dan IDOR ditandai belum teruji akibat limitasi iterasi 1 putaran."
    ]
    add_bilingual_section(doc, en_exec, id_exec)

    # -------------------------------------------------------------
    # 2. TARGET SYSTEM & ASSESSMENT PARAMETERS
    # -------------------------------------------------------------
    add_section_h1("2. TARGET SYSTEM & ASSESSMENT PARAMETERS")
    en_params = [
        "**Target 1 (Public Hostname):** `https://rekapbudget-estate.first-resources.com`\n• DNS CNAME: `lkt-infra.first-resources.com` -> `10.100.2.64`\n• Stack: Nginx Reverse Proxy, HTTP/2 over TLS 1.3/1.2\n• Certificate: `*.first-resources.com` (Sectigo CA DV R36, valid 2026-06-29 to 2027-01-13)",
        "**Target 2 (Internal Direct Service):** `http://10.110.1.9:1627`\n• Network: Direct RFC1918 Private IPv4 (No PTR/DNS)\n• Stack: HTTP/1.0 Plaintext (Server banner: `RBFR`)\n• Title: Rekapitulasi Budget FR - Estate (Identical BIMS application)",
        "**Engagement Boundary:** Isolated evaluation strictly for the BIMS system scope without carrying forward prior target data."
    ]
    id_params = [
        "**Target 1 (Hostname Publik):** `https://rekapbudget-estate.first-resources.com`\n• DNS CNAME: `lkt-infra.first-resources.com` -> `10.100.2.64`\n• Stack: Nginx Reverse Proxy, HTTP/2 melalui TLS 1.3/1.2\n• Sertifikat: `*.first-resources.com` (Sectigo CA DV R36, aktif 2026-06-29 s/d 2027-01-13)",
        "**Target 2 (Layanan Internal Langsung):** `http://10.110.1.9:1627`\n• Jaringan: Alamat Privat IPv4 RFC1918 Langsung (Tanpa PTR/DNS)\n• Stack: HTTP/1.0 Plaintext (Banner server: `RBFR`)\n• Judul: Rekapitulasi Budget FR - Estate (Aplikasi BIMS identik)",
        "**Batasan Engagement:** Evaluasi terisolasi khusus untuk ruang lingkup sistem BIMS tanpa membawa temuan dari target lain."
    ]
    add_bilingual_section(doc, en_params, id_params)

    # -------------------------------------------------------------
    # 3. METHODOLOGY
    # -------------------------------------------------------------
    add_section_h1("3. TESTING METHODOLOGY / METODOLOGI")
    en_meth = [
        "**1. Passive Reconnaissance:** DNS resolution, HTTP-to-HTTPS redirect validation, TLS chain verification, and metadata checks (`/robots.txt`, `/.well-known/security.txt`).",
        "**2. Targeted TCP Enumeration:** Rapid single-pass scan via Nmap (`-sT -sV -sC -T4 --top-ports 1000 -p1627`) on host `10.110.1.9` without UDP flooding or disruptive probes.",
        "**3. OWASP Web Analysis:** Non-destructive audit of login endpoint (`/masuk`), transport security verification, safe dummy credential probing, security header analysis (CSP, HSTS, X-Frame-Options), and cookie inspection.",
        "**4. Evidence Classification:** Strict segregation of confirmed exploitable risks vs configuration anomalies vs untested limits."
    ]
    id_meth = [
        "**1. Reconnaissance Pasif:** Resolusi DNS, validasi redirect HTTP-ke-HTTPS, verifikasi rantai TLS, dan pemeriksaan metadata (`/robots.txt`, `/.well-known/security.txt`).",
        "**2. Enumerasi TCP Terarah:** Pemindaian satu putaran cepat via Nmap (`-sT -sV -sC -T4 --top-ports 1000 -p1627`) pada host `10.110.1.9` tanpa UDP scan maupun probe agresif.",
        "**3. Analisis Web OWASP:** Audit non-destruktif endpoint login (`/masuk`), verifikasi keamanan transport, pengujian aman kredensial dummy, inspeksi security headers (CSP, HSTS, X-Frame-Options), dan inspeksi cookie.",
        "**4. Klasifikasi Bukti:** Pemisahan ketat antara risiko nyata terverifikasi, anomali konfigurasi, dan batasan belum teruji."
    ]
    add_bilingual_section(doc, en_meth, id_meth)

    # -------------------------------------------------------------
    # 4. RISK MATRIX & FINDINGS OVERVIEW
    # -------------------------------------------------------------
    add_section_h1("4. RISK MATRIX & FINDINGS OVERVIEW / MATRIKS RISIKO & TEMUAN")
    matrix_table = doc.add_table(rows=6, cols=4)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    matrix_table.autofit = False
    
    col_widths = [Inches(0.8), Inches(3.6), Inches(1.1), Inches(2.0)]
    
    headers = ["Finding ID", "Security Issue / Isu Keamanan", "Severity", "Status / Verification Note"]
    for j, h in enumerate(headers):
        c = matrix_table.cell(0, j)
        c.width = col_widths[j]
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    m_rows = [
        ("F-01", "Plaintext HTTP Transport on Internal Login Endpoint\nTransport HTTP Plaintext pada Endpoint Login (10.110.1.9:1627)", "HIGH", "FFF1F2", "991B1B", "Verified Vulnerability (CWE-319)\nTerverifikasi Nyata"),
        ("F-02", "Permissive Content Security Policy with unsafe-inline\nKebijakan CSP Permisif Mengizinkan unsafe-inline", "MEDIUM", "FFFBEB", "92400E", "Configuration Weakness (CWE-1021/79)\nKelemahan Konfigurasi"),
        ("F-03", "Redundant & Conflicting Security Headers from Proxy Layer\nDuplikasi dan Konflik Header Keamanan Akibat Layering Proxy", "LOW", "EFF6FF", "1E40AF", "Configuration Inconsistency (CWE-16)\nInkonsistensi Konfigurasi"),
        ("O-01", "Web Server & Backend Tech Stack Banner Disclosure\nPengungkapan Banner Layanan Server (nginx, Server: RBFR)", "INFO", "FFFFFF", "334155", "Operational Hygiene Observation\nObservasi Higiene Operasional"),
        ("O-02", "Metadata Path Redirect & TLS Validation Anomalies\nAnomali Redirect Metadata & Error Validasi TLS (curl 60 / 35)", "INFO", "FFFFFF", "334155", "Network Telemetry Recording\nCatatan Telemetri Jaringan"),
    ]

    for i, (fid, title, sev, bg_color, text_color, status) in enumerate(m_rows, start=1):
        row = matrix_table.rows[i]
        
        # ID
        c0 = row.cells[0]
        c0.width = col_widths[0]
        set_cell_background(c0, bg_color)
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(fid)
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(8.5)

        # Title
        c1 = row.cells[1]
        c1.width = col_widths[1]
        set_cell_background(c1, bg_color)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        lines = title.split('\n')
        r1a = p1.add_run(lines[0] + "\n")
        r1a.bold = True
        r1a.font.name = "Arial"
        r1a.font.size = Pt(8.5)
        r1b = p1.add_run(lines[1])
        r1b.italic = True
        r1b.font.name = "Arial"
        r1b.font.size = Pt(7.5)
        r1b.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Severity
        c2 = row.cells[2]
        c2.width = col_widths[2]
        set_cell_background(c2, bg_color)
        set_cell_margins(c2, top=60, bottom=60, left=100, right=100)
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(sev)
        r2.bold = True
        r2.font.name = "Arial"
        r2.font.size = Pt(8.5)
        # Parse hex color
        rgb = tuple(int(text_color[k:k+2], 16) for k in (0, 2, 4))
        r2.font.color.rgb = RGBColor(*rgb)

        # Status
        c3 = row.cells[3]
        c3.width = col_widths[3]
        set_cell_background(c3, bg_color)
        set_cell_margins(c3, top=60, bottom=60, left=100, right=100)
        p3 = c3.paragraphs[0]
        p3.paragraph_format.space_before = Pt(2)
        p3.paragraph_format.space_after = Pt(2)
        st_lines = status.split('\n')
        r3a = p3.add_run(st_lines[0] + "\n")
        r3a.font.name = "Arial"
        r3a.font.size = Pt(8.0)
        r3b = p3.add_run(st_lines[1])
        r3b.italic = True
        r3b.font.name = "Arial"
        r3b.font.size = Pt(7.5)
        r3b.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    set_table_borders(matrix_table, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 5. DETAILED FINDINGS BREAKDOWN
    # -------------------------------------------------------------
    add_section_h1("5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN")

    # F-01
    add_section_h2("F-01: Plaintext HTTP Transport on Internal Login Endpoint (Port 1627)")
    en_f01 = [
        "**Risk Rating:** HIGH  |  **CWE:** CWE-319  |  **Status:** Confirmed Verified",
        "**Impact:** The application at `http://10.110.1.9:1627` runs an unencrypted HTTP/1.0 service serving an active login form (`POST /masuk`). Because traffic lacks TLS encryption, user/admin credentials and session tokens can be intercepted via network sniffing, ARP spoofing, or MitM attacks across the internal RFC1918 subnet.",
        "**Detailed Narrative:** Nmap scan revealed TCP port 1627 is open (`Server: RBFR`). HTTPS probes failed with `curl: (35) wrong version number`. HTTP/1.0 GET returned a 3,995-byte HTML payload containing the BIMS login form. A safe dummy credential probe produced `HTTP 401 Unauthorized`, proving the authentication gateway is live and actively processing requests.",
        "**Recommended Remediation:**\n1. Rebind BIMS service to `127.0.0.1:1627` and enforce access through an authoritative HTTPS reverse proxy.\n2. Block direct cross-VLAN inbound access to port 1627 using host-level firewall rules (`iptables`).\n3. Force immediate HTTP 301 redirection to HTTPS if port 1627 remains active.\n4. Rotate credentials of all users previously authenticated via this endpoint."
    ]
    id_f01 = [
        "**Risk Rating:** HIGH  |  **CWE:** CWE-319  |  **Status:** Terverifikasi Nyata",
        "**Dampak:** Layanan pada `http://10.110.1.9:1627` beroperasi pada HTTP/1.0 tanpa enkripsi dan menyajikan form login aktif (`POST /masuk`). Ketiadaan TLS membuka risiko penyadapan kredensial dan token sesi via network sniffing, ARP poisoning, atau serangan MitM pada jaringan lokal RFC1918.",
        "**Deskripsi Rinci:** Scan Nmap menemukan port TCP 1627 terbuka (`Server: RBFR`). Probe HTTPS gagal dengan `curl: (35) wrong version number`. Permintaan HTTP/1.0 GET menghasilkan respons 3.995 byte memuat form login BIMS. Uji coba kredensial dummy menghasilkan respons `HTTP 401 Unauthorized`, membuktikan endpoint autentikasi aktif.",
        "**Rekomendasi Perbaikan:**\n1. Batasi binding BIMS hanya ke `127.0.0.1:1627` dan wajibkan akses via reverse proxy HTTPS.\n2. Blokir akses langsung antar-VLAN menuju port 1627 dengan firewall host (`iptables`).\n3. Terapkan redirect 301 otomatis ke HTTPS bila port 1627 tetap dibuka sementara.\n4. Rotasi kata sandi seluruh staf yang pernah login melalui endpoint IP plaintext tersebut."
    ]
    add_bilingual_section(doc, en_f01, id_f01)
    
    term_f01 = (
        "$ nmap -sT -sV -sC -T4 --top-ports 1000 -p1627 10.110.1.9\n"
        "PORT     STATE SERVICE VERSION\n"
        "1627/tcp open  http    RBFR custom HTTP server (HTTP/1.0)\n"
        "|_http-server-header: RBFR\n"
        "|_http-title: Rekapitulasi Budget FR - Estate\n"
        "\n"
        "$ curl -i http://10.110.1.9:1627/masuk\n"
        "HTTP/1.0 200 OK\n"
        "Server: RBFR\n"
        "<form method=\"post\" action=\"/masuk\">\n"
        "  <input type=\"text\" name=\"username\" /> <input type=\"password\" name=\"password\" />\n"
        "</form>\n"
        "\n"
        "$ curl -k https://10.110.1.9:1627/masuk\n"
        "curl: (35) error:0A00010B:SSL routines::wrong version number (HTTP-only endpoint)"
    )
    add_terminal_box(doc, term_f01)

    # F-02
    add_section_h2("F-02: Permissive Content Security Policy with unsafe-inline Directives")
    en_f02 = [
        "**Risk Rating:** MEDIUM  |  **CWE:** CWE-1021 / CWE-79  |  **Status:** Verified Config Flaw",
        "**Impact:** Both endpoints emit a Content Security Policy containing `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'`. This disables browser defense-in-depth against XSS, allowing injected scripts to execute if unsanitized reflection points exist.",
        "**Detailed Narrative:** Header audits confirmed permissive CSP settings. Reflected XSS probing was not completed due to single-pass iteration limits. The issue is classified as a verified configuration flaw rather than a demonstrated exploit.",
        "**Recommended Remediation:** Remove `'unsafe-inline'`, implement cryptographic nonces (`'nonce-...'`), and perform an authenticated XSS audit."
    ]
    id_f02 = [
        "**Risk Rating:** MEDIUM  |  **CWE:** CWE-1021 / CWE-79  |  **Status:** Kelemahan Konfigurasi Terverifikasi",
        "**Dampak:** Kedua target menyajikan header CSP yang memuat `script-src 'unsafe-inline'` dan `style-src 'unsafe-inline'`. Hal ini meniadakan perlindungan utama browser terhadap XSS, sehingga script berbahaya dapat dieksekusi bila ditemukan celah injeksi input.",
        "**Deskripsi Rinci:** Pemeriksaan header membuktikan CSP permisif. Pengujian reflected XSS terhenti oleh batas iterasi satu putaran. Isu ini diklasifikasikan sebagai kelemahan konfigurasi nyata, bukan eksploitasi terbukti.",
        "**Rekomendasi Perbaikan:** Hapus `'unsafe-inline'`, gunakan cryptographic nonce (`'nonce-...'`), dan lakukan audit penetrasi terotorisasi lanjutan."
    ]
    add_bilingual_section(doc, en_f02, id_f02)
    term_f02 = "Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; frame-ancestors 'none'"
    add_terminal_box(doc, term_f02)

    # F-03
    add_section_h2("F-03: Redundant & Conflicting Security Headers via Reverse Proxy Layering")
    en_f03 = [
        "**Risk Rating:** LOW  |  **CWE:** CWE-16  |  **Status:** Configuration Inconsistency Confirmed",
        "**Impact:** HTTPS responses emit duplicated and contradictory security headers: `X-Frame-Options: DENY` and `SAMEORIGIN` simultaneously, duplicate `Referrer-Policy`, and duplicated `X-Content-Type-Options`. Browsers may resolve conflicting directives inconsistently, potentially negating clickjacking protections.",
        "**Remediation:** Designate the edge Nginx reverse proxy as the authoritative header injector; suppress backend duplicates using `proxy_hide_header`."
    ]
    id_f03 = [
        "**Risk Rating:** LOW  |  **CWE:** CWE-16  |  **Status:** Inkonsistensi Konfigurasi Terverifikasi",
        "**Dampak:** Respons HTTPS menyajikan header keamanan ganda yang saling bertentangan: `X-Frame-Options: DENY` dan `SAMEORIGIN` secara bersamaan, duplikasi `Referrer-Policy`, serta `X-Content-Type-Options` ganda. Browser dapat memproses konflik secara acak dan berpotensi membatalkan proteksi anti-clickjacking.",
        "**Rekomendasi Perbaikan:** Tetapkan edge reverse proxy Nginx sebagai pengendali header tunggal; bersihkan header duplikat dari backend menggunakan `proxy_hide_header`."
    ]
    add_bilingual_section(doc, en_f03, id_f03)

    # -------------------------------------------------------------
    # 6. OBSERVATIONS & 7. VERIFIED CONTROLS
    # -------------------------------------------------------------
    add_section_h1("6. ADDITIONAL SECURITY OBSERVATIONS & TELEMETRY")
    en_obs = [
        "**O-01 (Server Banner Disclosure):** The public endpoint exposes `Server: nginx` while the internal endpoint exposes `Server: RBFR`. Although build versions are not displayed, disclosing software names aids attacker fingerprinting.",
        "**O-02 (Metadata Routing & TLS Errors):** `/robots.txt` and `/.well-known/security.txt` trigger HTTP 303 redirects to `/masuk` on port 1627. Strict TLS validation on hostname produced `curl (60)` due to local trust bundle limits."
    ]
    id_obs = [
        "**O-01 (Pengungkapan Banner Layanan):** Endpoint publik mengekspos `Server: nginx` sedangkan endpoint internal mengekspos `Server: RBFR`. Kendati versi build spesifik tidak terlihat, informasi ini mempermudah pemetaan teknologi target.",
        "**O-02 (Routing Metadata & Error TLS):** Path `/robots.txt` dan `/.well-known/security.txt` dialihkan via HTTP 303 ke `/masuk` pada port 1627. Validasi TLS strict pada hostname memunculkan error `curl (60)` akibat trust store lokal."
    ]
    add_bilingual_section(doc, en_obs, id_obs)

    add_section_h1("7. VERIFIED CONTROLS & NEGATIVE TEST RESULTS / KONTROL TERVERIFIKASI")
    ctrl_table = doc.add_table(rows=7, cols=2)
    ctrl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ctrl_table.autofit = False
    
    col_w = Inches(3.75)
    c0 = ctrl_table.cell(0, 0)
    c1 = ctrl_table.cell(0, 1)
    c0.width = col_w
    c1.width = col_w
    set_cell_background(c0, "E2E8F0")
    set_cell_background(c1, "E2E8F0")
    set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
    set_cell_margins(c1, top=80, bottom=80, left=120, right=120)

    p0 = c0.paragraphs[0]
    r0 = p0.add_run("Security Parameter & Verified Control (English)")
    r0.bold = True
    r0.font.name = "Arial"
    r0.font.size = Pt(8.5)

    p1 = c1.paragraphs[0]
    r1 = p1.add_run("Hasil Verifikasi & Kontrol Keamanan (Bahasa Indonesia)")
    r1.bold = True
    r1.font.name = "Arial"
    r1.font.size = Pt(8.5)

    ctrl_rows = [
        ("Host Network Attack Surface: Nmap scan on host 10.110.1.9 across top-1000 ports plus port 1627 confirmed that only TCP/1627 is open.",
         "Permukaan Serangan Host: Pemindaian Nmap pada 10.110.1.9 mengonfirmasi hanya port 1627 yang terbuka. Tidak ada port manajemen (SSH, RDP, DB) yang terekspos."),
        ("HTTP-to-HTTPS Redirection: Hostname rekapbudget-estate.first-resources.com enforces HTTP 301 Moved Permanently redirect to HTTPS.",
         "Pengalihan HTTP ke HTTPS: Hostname publik secara benar menerapkan pengalihan 301 dari HTTP biasa ke koneksi aman HTTPS."),
        ("HSTS Implementation: Strict-Transport-Security active with max-age=15552000 and includeSubDomains.",
         "Penerapan HSTS: Header HSTS aktif pada HTTPS dengan durasi 180 hari (15552000 detik) mencakup seluruh subdomain."),
        ("TLS Certificate Legitimacy: Valid commercial Sectigo wildcard certificate (*.first-resources.com) active through January 2027.",
         "Validitas Sertifikat TLS: Menggunakan sertifikat resmi Sectigo wildcard valid dengan masa aktif hingga 13 Januari 2027."),
        ("Authentication Rejection: Dummy POST probe to /masuk returned HTTP 401 Unauthorized without error bypass.",
         "Penolakan Autentikasi Dummy: Percobaan kredensial palsu pada /masuk menghasilkan respons 401 Unauthorized yang valid."),
        ("HTTP Method Restriction: Probing HTTP OPTIONS on port 1627 resulted in 405 Method Not Allowed.",
         "Restriksi Metode HTTP: Request HTTP OPTIONS pada port 1627 menghasilkan 405 Method Not Allowed.")
    ]

    for i, (en, idn) in enumerate(ctrl_rows, start=1):
        cell_en = ctrl_table.cell(i, 0)
        cell_id = ctrl_table.cell(i, 1)
        cell_en.width = col_w
        cell_id.width = col_w
        set_cell_background(cell_en, "FFFFFF")
        set_cell_background(cell_id, "FFFFFF")
        set_cell_margins(cell_en, top=60, bottom=60, left=120, right=120)
        set_cell_margins(cell_id, top=60, bottom=60, left=120, right=120)

        pen = cell_en.paragraphs[0]
        pen.paragraph_format.space_before = Pt(2)
        pen.paragraph_format.space_after = Pt(2)
        ren = pen.add_run(en)
        ren.font.name = "Arial"
        ren.font.size = Pt(8.0)

        pid = cell_id.paragraphs[0]
        pid.paragraph_format.space_before = Pt(2)
        pid.paragraph_format.space_after = Pt(2)
        rid = pid.add_run(idn)
        rid.font.name = "Arial"
        rid.font.size = Pt(8.0)

    set_table_borders(ctrl_table, color="CBD5E1", sz="4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 8. LIMITATIONS & UNTESTED ITEMS
    # -------------------------------------------------------------
    add_section_h1("8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN")
    en_lim = [
        "• **Linear Single-Pass Constraint:** Conducted under strict anti-loop execution guidelines (max 1 probe per tool, no retries, no deep recursion).",
        "• **Session Cookie Flags Unverified:** No `Set-Cookie` header observed on unauthenticated GET requests. Post-auth flags (Secure, HttpOnly, SameSite) could not be verified.",
        "• **Input Reflection & XSS Inconclusive:** Reflection probing was suspended upon reaching subtask iteration limits; no malicious payloads were transmitted.",
        "• **Rate Limiting Inconclusive:** A single dummy attempt gave HTTP 401 without 429/Retry-After. Progressive throttling cannot be conclusively confirmed from one request.",
        "• **Zero Destructive Impact:** No brute-forcing, password spraying, SQL injection fuzzing, or DoS testing was conducted."
    ]
    id_lim = [
        "• **Batasan Alur Linear 1 Putaran:** Dilakukan dengan pedoman bebas macet ketat (maksimal 1 percobaan per tool, tanpa retry, tanpa crawling dalam).",
        "• **Flag Cookie Sesi Belum Teruji:** Header `Set-Cookie` tidak muncul pada GET awal. Flag pasca-login (Secure, HttpOnly, SameSite) belum dapat dinilai.",
        "• **Uji Reflected XSS Belum Tuntas:** Probe parameter reflection terhenti oleh limit iterasi; tidak ada payload eksploitatif yang dievaluasi.",
        "• **Rate Limiting Belum Konklusif:** Satu percobaan dummy menghasilkan HTTP 401 tanpa header 429. Mekanisme lock-out membutuhkan uji multi-request terotorisasi.",
        "• **Bebas Dampak Destruktif:** Tidak dilakukan brute-force, password spraying, injeksi SQL merusak, atau uji kelumpuhan sistem (DoS)."
    ]
    add_bilingual_section(doc, en_lim, id_lim)

    # -------------------------------------------------------------
    # 9. REMEDIATION ROADMAP & 10. CONCLUSION
    # -------------------------------------------------------------
    add_section_h1("9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN")
    en_road = [
        "**1. Decommission or Proxy Plaintext HTTP Port 1627** — Priority: **HIGH**\nRebind internal BIMS service to `127.0.0.1:1627` and enforce access through an authoritative HTTPS reverse proxy. Enforce host firewall rules blocking cross-VLAN traffic and rotate credentials used across internal tests.",
        "**2. Normalize Security Headers at Edge Reverse Proxy** — Priority: **MEDIUM**\nConsolidate security headers in Nginx configuration. Remove duplicates and enforce single authoritative directives (`X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`). Use `proxy_hide_header`.",
        "**3. Harden Content Security Policy (CSP)** — Priority: **MEDIUM**\nRemove `'unsafe-inline'` from script-src and style-src. Adopt cryptographic nonces or SHA-256 hashes.",
        "**4. Enforce Session Cookie Flags Post-Login** — Priority: **LOW / MEDIUM**\nEnsure all cookies issued upon successful authentication include `Secure; HttpOnly; SameSite=Lax`."
    ]
    id_road = [
        "**1. Tutup atau Alihkan Layanan HTTP Plaintext Port 1627** — Prioritas: **HIGH**\nUbah binding BIMS internal ke `127.0.0.1:1627` dan wajibkan seluruh akses melalui reverse proxy HTTPS. Terapkan firewall host untuk memblokir akses langsung antar-VLAN serta lakukan rotasi kredensial pengguna internal.",
        "**2. Normalisasi Header Keamanan pada Reverse Proxy** — Prioritas: **MEDIUM**\nSatukan konfigurasi header pada Nginx. Hapus nilai duplikat dan tetapkan satu kebijakan tegas (`X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`). Gunakan `proxy_hide_header`.",
        "**3. Perketat Content Security Policy (CSP)** — Prioritas: **MEDIUM**\nHapus `'unsafe-inline'` pada direktif script-src dan style-src. Terapkan mekanisme nonce atau hash SHA-256.",
        "**4. Terapkan Flag Cookie Sesi Pasca-Login** — Prioritas: **LOW / MEDIUM**\nPastikan cookie sesi yang diterbitkan setelah login memuat atribut `Secure; HttpOnly; SameSite=Lax`."
    ]
    add_bilingual_section(doc, en_road, id_road)

    add_section_h1("10. CONCLUSION / KESIMPULAN")
    en_conc = [
        "Within the executed linear single-pass scope, the **BIMS / Rekapitulasi Budget FR - Estate** application demonstrates effective perimeter security controls on its public HTTPS interface (valid wildcard TLS, HSTS, and 401 auth rejection). However, exposing an unencrypted HTTP/1.0 login interface directly on internal IP `10.110.1.9:1627` introduces a critical transport flaw (**F-01: High**) that bypasses transport encryption and leaves authentication credentials vulnerable to internal network interception.",
        "Remediation must prioritize closing or proxying port 1627 behind HTTPS, followed by normalizing duplicate security headers and hardening the Content Security Policy to achieve comprehensive enterprise production posture."
    ]
    id_conc = [
        "Dalam cakupan pengujian linear satu putaran yang dilakukan, sistem **BIMS / Rekapitulasi Budget FR - Estate** menunjukkan pertahanan perimeter yang efektif pada interface HTTPS publiknya (sertifikat wildcard TLS valid, HSTS, dan penolakan 401 auth). Namun, ketersediaan antarmuka login HTTP/1.0 tanpa enkripsi langsung pada IP internal `10.110.1.9:1627` memunculkan kerentanan transport kritis (**F-01: High**) yang mengabaikan enkripsi lalu lintas data dan membuka celah penyadapan kredensial.",
        "Remediasi harus memprioritaskan penutupan atau pengalihan port 1627 ke jalur HTTPS, disusul dengan normalisasi header keamanan ganda serta pengetatan Content Security Policy demi mencapai postur keamanan produksi enterprise yang tangguh."
    ]
    add_bilingual_section(doc, en_conc, id_conc)

    # Formal Sign-off
    sign_table = doc.add_table(rows=1, cols=3)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False
    col3_w = Inches(2.5)
    
    sign_items = [
        "Report Prepared By:\nCyber Security Assessment Division\nLentera Teknologi",
        "Classification:\nCONFIDENTIAL — INTERNAL ONLY\nZero Defect Assessment Standard",
        "Document Verification:\nECC Gate 1-5 Compliant\nDate: 18 Oktober 2026"
    ]
    for k, item in enumerate(sign_items):
        cell = sign_table.cell(0, k)
        cell.width = col3_w
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        lines = item.split('\n')
        r0 = p.add_run(lines[0] + "\n")
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(8.0)
        r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r1 = p.add_run("\n".join(lines[1:]))
        r1.font.name = "Arial"
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    set_table_borders(sign_table, color="CBD5E1", sz="4")
    
    doc.save(output_path)
    print(f"[OK] Report DOCX successfully generated at: {output_path}")

if __name__ == '__main__':
    out_docx = sys.argv[1] if len(sys.argv) > 1 else "/home/kristian.admin/.gemini/antigravity-cli/brain/18c205a4-661a-4e83-9dfb-8f26c11d7987/BIMS_REKAP_BUDGET_FR_PENETRATION_TESTING_REPORT.docx"
    generate_docx(out_docx)
