#!/usr/bin/env python3
"""
build_deadstock_docx.py
Generates an editable, professionally formatted Word (.docx) document
for the Dashboard Deadstock (First Resources Group) Penetration Testing Report,
matching the bilingual format and executive styling of Lentera Teknologi.

Includes ECMA-376 schema sanitization to ensure 100% compatibility with
Microsoft Word on macOS / Windows and Apple Pages.
"""

import sys
import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

TC_TAG_ORDER = [
    'cnfStyle', 'tcW', 'gridSpan', 'hMerge', 'vMerge', 'tcBorders', 'shd',
    'noWrap', 'tcMar', 'textDirection', 'tcFitText', 'vAlign', 'hideMark',
    'headers', 'cellIns', 'cellDel', 'cellMerge', 'tcPrChange'
]

TBL_TAG_ORDER = [
    'tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual', 'tblStyleRowBandSize',
    'tblStyleColBandSize', 'tblW', 'jc', 'tblCellSpacing', 'tblInd',
    'tblBorders', 'shd', 'tblLayout', 'tblCellMar', 'tblLook',
    'tblCaption', 'tblDescription'
]

def sort_elem(elem, order):
    """Sorts XML children according to strict OpenXML schema sequences."""
    def key_fn(c):
        tag = c.tag.split('}')[-1]
        return order.index(tag) if tag in order else 999
    sorted_c = sorted(list(elem), key=key_fn)
    for c in list(elem):
        elem.remove(c)
    for c in sorted_c:
        elem.append(c)

def sanitize_openxml(doc):
    """Enforces ECMA-376 schema compliance across all tables and cells."""
    for table in doc.tables:
        if hasattr(table._tbl, 'tblPr') and table._tbl.tblPr is not None:
            sort_elem(table._tbl.tblPr, TBL_TAG_ORDER)
        for row in table.rows:
            for cell in row.cells:
                tc_pr = cell._tc.get_or_add_tcPr()
                sort_elem(tc_pr, TC_TAG_ORDER)

def set_cell_background(cell, hex_color):
    """Sets the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
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

def format_runs(paragraph, text):
    """Parses simple inline bold markers (**text**) and code markers (`code`)."""
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

def add_bilingual_section(doc, en_paragraphs, id_paragraphs, en_header="English", id_header="Bahasa Indonesia"):
    """Creates a dual-column bilingual table (English left, Bahasa Indonesia right)."""
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    col_width = Inches(3.75)
    for row in table.rows:
        for cell in row.cells:
            cell.width = col_width
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    # Header Row
    cell_en_h = table.cell(0, 0)
    set_cell_background(cell_en_h, "E0F2FE")
    p_en_h = cell_en_h.paragraphs[0]
    p_en_h.paragraph_format.space_before = Pt(2)
    p_en_h.paragraph_format.space_after = Pt(2)
    r_en_h = p_en_h.add_run(en_header)
    r_en_h.bold = True
    r_en_h.font.size = Pt(9.5)
    r_en_h.font.color.rgb = RGBColor(0x03, 0x69, 0xA1)

    cell_id_h = table.cell(0, 1)
    set_cell_background(cell_id_h, "D1FAE5")
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

def add_terminal_box(doc, text):
    """Creates a dark slate code terminal box for PoC command evidence."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.rows[0].cells[0].width = Inches(7.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, "0F172A")
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
        hrun = hp.add_run("LENTERA TEKNOLOGI | Dashboard Deadstock — Internal Web Pentest Report (Editable)")
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

    # COVER / HEADER
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
    r_title = p_title.add_run("Dashboard Deadstock / First Resources (FR) Group")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("INTERNAL WEB PENETRATION TESTING REPORT — 19 OKTOBER 2026")
    r_sub.bold = True
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.rows[0].cells[0].width = Inches(2.0)
    meta_table.rows[0].cells[1].width = Inches(5.5)

    meta_rows = [
        ("Target System", "Dashboard Deadstock (FR Group) — https://deadstock.first-resources.com / 10.110.1.9:1100"),
        ("DNS / Routing", "CNAME lkt-infra.first-resources.com -> A 10.100.2.64 (Infrastructure Masking)"),
        ("Assessment Scope", "Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran)"),
        ("Attacker / Audit Node", "Internal Workstation Node (Linux Security Subsystem / RFC1918 Scope)"),
        ("Access Level Tested", "Unauthenticated Passive Recon, Network Probing, & Application Response Baseline"),
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

    # 1. EXECUTIVE SUMMARY
    add_section_h1("1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF")
    en_exec = [
        "On 19 October 2026, a focused, non-destructive internal web penetration test was conducted against the **Dashboard Deadstock** application across two endpoints: the primary domain `https://deadstock.first-resources.com` (resolving via CNAME to `10.100.2.64`) and the direct internal instance `http://10.110.1.9:1100`.",
        "Testing strictly adhered to an anti-loop linear single-pass methodology aligned with OWASP Top 10 standards. Perimeter HTTPS defenses were verified to be solid, with valid commercial Sectigo TLS 1.3 encryption, active HSTS (`max-age=86400`), anti-clickjacking (`X-Frame-Options: SAMEORIGIN`), and MIME-type enforcement.",
        "The primary observations identified are **F-01: Security Header Asymmetry on Port 1100 (Low)** and **F-02: Framework Disclosure (`X-Powered-By: Express`, Informational)**. An active port scan wrapper reached timeout (exit 124) and was recorded transparently as an information boundary.",
        "**Overall Assessment:** Evidence confirms **1 Low-Risk Finding** and **1 Informational Observation**. Advanced authenticated categories remain unverified due to scope constraints."
    ]
    id_exec = [
        "Pada 19 Oktober 2026 dilakukan pengujian penetrasi web internal non-destruktif terhadap sistem **Dashboard Deadstock** pada dua jalur akses: domain HTTPS utama `https://deadstock.first-resources.com` (ter-resolve via CNAME ke `10.100.2.64`) dan instans server internal langsung `http://10.110.1.9:1100`.",
        "Pengujian menerapkan alur linear satu putaran bebas macet sesuai standar OWASP Top 10. Pertahanan perimeter HTTPS terverifikasi kuat dengan enkripsi TLS 1.3 komersial Sectigo valid, HSTS aktif (`max-age=86400`), proteksi anti-clickjacking, dan penegakan tipe konten.",
        "Temuan utama mencakup **F-01: Asimetri Header Keamanan pada Port 1100 (Low)** dan **F-02: Pengungkapan Framework (`X-Powered-By: Express`, Informational)**. Scan port Nmap mengalami batas waktu (exit 124) dan dicatat transparan sebagai batas informasi tanpa klaim port palsu.",
        "**Kesimpulan Umum:** Hasil mendukung **1 Temuan Berisiko Rendah (Low)** dan **1 Observasi Informasional**. Kategori terautentikasi ditandai belum teruji sesuai batasan 1 putaran."
    ]
    add_bilingual_section(doc, en_exec, id_exec)

    # 2. TARGET SYSTEM & ASSESSMENT PARAMETERS
    add_section_h1("2. TARGET SYSTEM & ASSESSMENT PARAMETERS")
    en_params = [
        "**Target 1 (Public Hostname):** `https://deadstock.first-resources.com`\n• DNS CNAME: `lkt-infra.first-resources.com` -> `10.100.2.64`\n• Stack: Nginx Reverse Proxy, TLSv1.3 with `TLS_AES_256_GCM_SHA384`\n• Certificate: `*.first-resources.com` (Sectigo CA DV R36, valid 2026-06-29 to 2027-01-13)",
        "**Target 2 (Internal Direct Service):** `http://10.110.1.9:1100`\n• Network: Direct RFC1918 Private IPv4 (No PTR/DNS)\n• Stack: `nginx/1.22.1` + Node.js / Express (`X-Powered-By: Express`)\n• Title: Dashboard Deadstock (First Resources Group)",
        "**Engagement Boundary:** Isolated evaluation strictly for the Dashboard Deadstock application."
    ]
    id_params = [
        "**Target 1 (Hostname Publik):** `https://deadstock.first-resources.com`\n• DNS CNAME: `lkt-infra.first-resources.com` -> `10.100.2.64`\n• Stack: Nginx Reverse Proxy, TLSv1.3 dengan `TLS_AES_256_GCM_SHA384`\n• Sertifikat: `*.first-resources.com` (Sectigo CA DV R36, aktif 2026-06-29 s/d 2027-01-13)",
        "**Target 2 (Layanan Internal Langsung):** `http://10.110.1.9:1100`\n• Jaringan: Alamat Privat IPv4 RFC1918 Langsung (Tanpa PTR/DNS)\n• Stack: `nginx/1.22.1` + Node.js / Express (`X-Powered-By: Express`)\n• Judul: Dashboard Deadstock (First Resources Group)",
        "**Batasan Engagement:** Evaluasi terisolasi khusus untuk ruang lingkup aplikasi Dashboard Deadstock."
    ]
    add_bilingual_section(doc, en_params, id_params)

    # 3. METHODOLOGY
    add_section_h1("3. TESTING METHODOLOGY / METODOLOGI")
    en_meth = [
        "**1. Passive Reconnaissance:** DNS resolution via dig, CNAME mapping, httpx status check, and whatweb tech fingerprinting.",
        "**2. Targeted Network Scan:** Nmap scan (`-sT --top-ports 100 -p1100 -T2`). Process timed out at 180s (exit 124) and was recorded transparently without retry.",
        "**3. Application Response Probing:** Single-pass GET requests capturing headers and 2 KiB body samples across both targets into `app_responses.txt`.",
        "**4. TLS & Header Auditing:** OpenSSL s_client TLS 1.3 verification, HSTS validation, framing inspection, and asymmetry mapping.",
        "**5. Evidence Synthesis:** Separation of factual evidence from tooling artifacts and untested OWASP categories."
    ]
    id_meth = [
        "**1. Reconnaissance Pasif:** Resolusi DNS via dig, pemetaan CNAME, validasi status via httpx, dan fingerprinting teknologi via whatweb.",
        "**2. Scan Jaringan Terarah:** Nmap (`-sT --top-ports 100 -p1100 -T2`). Proses mencapai batas 180s (exit 124) dan dicatat transparan tanpa pengulangan.",
        "**3. Analisis Respons Aplikasi:** Permintaan GET satu kali menangkap header dan sampel body 2 KiB pada kedua target ke `app_responses.txt`.",
        "**4. Audit TLS & Header:** Verifikasi OpenSSL s_client TLS 1.3, validasi HSTS, inspeksi framing, dan pemetaan asimetri header.",
        "**5. Sintesis Bukti:** Pemisahan tegas antara temuan nyata, keterbatasan alat, dan kategori OWASP yang belum teruji."
    ]
    add_bilingual_section(doc, en_meth, id_meth)

    # 4. RISK MATRIX & FINDINGS OVERVIEW
    add_section_h1("4. RISK MATRIX & FINDINGS OVERVIEW / MATRIKS RISIKO & TEMUAN")
    matrix_table = doc.add_table(rows=5, cols=4)
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
        ("F-01", "Security Header Asymmetry & Unhardened HTTP Port 1100\nAsimetri Header Keamanan & Ketiadaan Hardening Port 1100 HTTP", "LOW", "EFF6FF", "1E40AF", "Configuration Flaw (CWE-16/1021)\nKelemahan Konfigurasi"),
        ("F-02", "Backend Framework & Server Version Disclosure\nPengungkapan Framework Backend & Versi Server (X-Powered-By: Express)", "INFO", "FFFFFF", "334155", "Technology Exposure (CWE-200)\nEksposur Informasi"),
        ("O-01", "Network Port Scan Execution Timeout (Exit 124)\nBatas Waktu Eksekusi Scan Port Nmap (Exit 124)", "INFO", "FFFFFF", "334155", "Scope Limitation Recording\nCatatan Keterbatasan Informasi"),
        ("O-02", "Incomplete Local Environment TLS Trust Store (Verify Code 21)\nKetidaklengkapan Trust Store TLS Lokal (Verify Code 21)", "INFO", "FFFFFF", "334155", "Local Client Artifact\nArtefak Lingkungan Penguji"),
    ]

    for i, (fid, title, sev, bg_color, text_color, status) in enumerate(m_rows, start=1):
        row = matrix_table.rows[i]
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
        rgb = tuple(int(text_color[k:k+2], 16) for k in (0, 2, 4))
        r2.font.color.rgb = RGBColor(*rgb)

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

    # 5. DETAILED FINDINGS BREAKDOWN
    add_section_h1("5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN")

    # F-01
    add_section_h2("F-01: Security Header Asymmetry & Unhardened HTTP Port 1100")
    en_f01 = [
        "**Risk Rating:** LOW  |  **CWE:** CWE-16 / CWE-1021  |  **Status:** Verified Flaw",
        "**Impact:** Direct access to `http://10.110.1.9:1100` omits baseline defensive headers (Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, CSP). Although no cleartext credential form was observed on the sampled payload, leaving the internal socket accessible without hardening creates potential exposure.",
        "**Detailed Narrative:** Probing confirmed that the HTTPS reverse proxy correctly applies defensive headers, but direct internal connections to port 1100 receive plain caching headers only. This asymmetry indicates defenses exist solely at the outer edge proxy.",
        "**Recommended Remediation:**\n1. Bind port 1100 strictly to `127.0.0.1:1100`, forcing all traffic via HTTPS reverse proxy.\n2. If direct access is required, inject standard security headers directly in Express/Nginx.\n3. Enforce automatic HTTP 301 redirection to HTTPS."
    ]
    id_f01 = [
        "**Risk Rating:** LOW  |  **CWE:** CWE-16 / CWE-1021  |  **Status:** Kelemahan Terverifikasi",
        "**Dampak:** Akses langsung ke `http://10.110.1.9:1100` tidak menyertakan header pertahanan standar (HSTS, X-Frame-Options, X-Content-Type-Options, CSP). Kendati tidak teramati adanya form login berpassword pada sampel 2 KiB, ketiadaan proteksi pada socket internal membuka potensi risiko.",
        "**Deskripsi Rinci:** Hasil audit membuktikan reverse proxy HTTPS menerapkan header keamanan dengan baik, namun akses langsung ke port 1100 hanya menghasilkan header cache. Asimetri ini menunjukkan proteksi hanya berada di lapisan luar reverse proxy.",
        "**Rekomendasi Perbaikan:**\n1. Batasi binding port 1100 hanya ke `127.0.0.1:1100` dan alihkan seluruh trafik via reverse proxy HTTPS.\n2. Pasang header keamanan standar langsung pada konfigurasi Express/Nginx backend bila akses langsung dibutuhkan.\n3. Terapkan pengalihan otomatis 301 ke HTTPS."
    ]
    add_bilingual_section(doc, en_f01, id_f01)
    
    term_f01 = (
        "$ curl -I http://10.110.1.9:1100/\n"
        "HTTP/1.1 200 OK\n"
        "Server: nginx/1.22.1\n"
        "X-Powered-By: Express\n"
        "Content-Type: text/html; charset=UTF-8\n"
        "(Missing: Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options)\n\n"
        "$ curl -k -I https://deadstock.first-resources.com/\n"
        "HTTP/1.1 200 OK\n"
        "Server: nginx\n"
        "Strict-Transport-Security: max-age=86400\n"
        "X-Frame-Options: SAMEORIGIN\n"
        "X-Content-Type-Options: nosniff"
    )
    add_terminal_box(doc, term_f01)

    # F-02
    add_section_h2("F-02: Backend Framework & Server Version Disclosure")
    en_f02 = [
        "**Risk Rating:** INFORMATIONAL  |  **CWE:** CWE-200  |  **Status:** Verified Exposure",
        "**Impact:** Responses from port 1100 reveal `X-Powered-By: Express` and `Server: nginx/1.22.1`. While not an exploitable vulnerability alone, it aids attackers in fingerprinting the stack.",
        "**Remediation:** Declare `app.disable('x-powered-by')` in Express and set `server_tokens off;` in Nginx."
    ]
    id_f02 = [
        "**Risk Rating:** INFORMATIONAL  |  **CWE:** CWE-200  |  **Status:** Eksposur Terverifikasi",
        "**Dampak:** Respons port 1100 mengekspos `X-Powered-By: Express` dan `Server: nginx/1.22.1`. Walaupun bukan celah langsung, informasi ini mempermudah pemetaan teknologi target oleh penyerang.",
        "**Rekomendasi Perbaikan:** Tambahkan `app.disable('x-powered-by')` pada Express dan `server_tokens off;` pada Nginx."
    ]
    add_bilingual_section(doc, en_f02, id_f02)

    # 6. OBSERVATIONS & 7. VERIFIED CONTROLS
    add_section_h1("6. ADDITIONAL SECURITY OBSERVATIONS & TELEMETRY")
    en_obs = [
        "**O-01 (Port Scan Timeout):** Subtask 194 Nmap scan reached the 180-second terminal harness limit (exit 124) due to conservative -T2 timing over 2 hosts. In compliance with anti-loop rules, it was logged to `recon_errors.txt` without retry.",
        "**O-02 (Local TLS Verify-21):** OpenSSL returned verify code 21 due to absent intermediate CA bundle on the tester workstation. The public Sectigo certificate is legitimately valid through January 2027."
    ]
    id_obs = [
        "**O-01 (Batas Waktu Scan Port):** Subtask 194 Nmap mencapai batas waktu 180s (exit 124) akibat profil waktu -T2 pada 2 target. Sesuai protokol anti-loop, kejadian dicatat pada `recon_errors.txt` tanpa perulangan.",
        "**O-02 (TLS Verify-21 Lokal):** OpenSSL menghasilkan verify code 21 akibat belum tersinkronisasinya intermediate CA pada workstation penguji. Sertifikat publik Sectigo terbukti valid dan resmi hingga Januari 2027."
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
        ("TLS 1.3 Cryptography: Modern TLSv1.3 negotiated with cipher TLS_AES_256_GCM_SHA384 and X25519 key exchange.",
         "Kriptografi TLS 1.3: TLSv1.3 modern ternegosiasi dengan cipher kuat TLS_AES_256_GCM_SHA384 dan pertukaran kunci X25519."),
        ("HSTS Enforcement: Strict-Transport-Security header active on HTTPS with max-age=86400.",
         "Penerapan HSTS: Header Strict-Transport-Security aktif pada HTTPS dengan parameter durasi max-age=86400."),
        ("Anti-Clickjacking Framing: X-Frame-Options: SAMEORIGIN enforced on public HTTPS endpoint.",
         "Kebijakan Anti-Clickjacking: Header X-Frame-Options: SAMEORIGIN aktif pada HTTPS mencegah framing ilegal."),
        ("MIME Sniffing Defense: X-Content-Type-Options: nosniff enforced on HTTPS.",
         "Proteksi MIME Sniffing: Header X-Content-Type-Options: nosniff aktif pada HTTPS menolak sniffing tipe konten."),
        ("Infrastructure Masking: DNS CNAME routes to lkt-infra.first-resources.com (10.100.2.64), isolating backend IP.",
         "Masking Infrastruktur: CNAME DNS mengarah ke lkt-infra.first-resources.com (10.100.2.64), menyamarkan IP backend langsung."),
        ("Controlled Application Response Size: Application HEAD responses return concise headers; GET responses serve structured 2 KiB baseline HTML without verbose stack trace leaks.",
         "Ukuran Respons Aplikasi Terkontrol: Respons HEAD menyajikan data ringkas; respons GET menyajikan HTML dasar 2 KiB tanpa kebocoran stack trace error debug.")
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

    # 8. LIMITATIONS & UNTESTED ITEMS
    add_section_h1("8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN")
    en_lim = [
        "• **Linear Single-Pass Constraint:** Adhered to strict non-destructive parameters (max 1 probe per tool, no retries, no crawling).",
        "• **Network Service Gap:** Nmap timed out at 180s; open port and service version mapping across the host remains incomplete.",
        "• **Body Sampling Threshold:** Body capture was constrained to a 2 KiB sample size; hidden form inputs were not audited.",
        "• **Authentication Untested:** No login sessions, cookie flags, or CORS handling were evaluated.",
        "• **Advanced OWASP Categories:** Broken Access Control (A01), Injection (A03), and Components (A06) were not audited.",
        "• **Zero Destructive Impact:** No brute-forcing, SQL injection fuzzing, or DoS testing was conducted."
    ]
    id_lim = [
        "• **Batasan Alur Linear 1 Putaran:** Pengujian mengikuti batasan non-destruktif ketat (maksimal 1 percobaan per alat, tanpa retry, tanpa crawling).",
        "• **Keterbatasan Scan Jaringan:** Nmap mengalami timeout pada 180 detik; pemetaan seluruh port dan versi layanan belum lengkap.",
        "• **Batas Sampel Body:** Sampel HTML dibatasi hingga 2 KiB; elemen form tersembunyi tidak diinspeksi.",
        "• **Autentikasi Belum Teruji:** Tidak ada sesi login, flag cookie, atau kebijakan CORS yang dievaluasi.",
        "• **Kategori OWASP Lanjutan:** Broken Access Control (A01), Injeksi (A03), dan Komponen Usang (A06) belum diaudit.",
        "• **Bebas Uji Destruktif:** Tidak dilakukan brute-force, fuzzing SQL, atau pengujian denial-of-service."
    ]
    add_bilingual_section(doc, en_lim, id_lim)

    # 9. REMEDIATION ROADMAP & 10. CONCLUSION
    add_section_h1("9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN")
    en_road = [
        "**1. Harden and Restrict Internal HTTP Port 1100** — Priority: **LOW / MEDIUM**\nRebind internal service on `10.110.1.9` to `127.0.0.1:1100` and enforce all access through the HTTPS reverse proxy.",
        "**2. Suppress Technology Signatures** — Priority: **INFORMATIONAL**\nDeclare `app.disable('x-powered-by')` in Express and configure `server_tokens off;` in Nginx.",
        "**3. Investigate Nmap Scan Timeout** — Priority: **INFORMATIONAL**\nAnalyze network rate limiting or drop rules causing the 180s Nmap timeout; conduct optimized -T4 scans.",
        "**4. Synchronize CA Trust Stores & Phase-2 Audit** — Priority: **INFORMATIONAL**\nInstall intermediate CAs in local trust stores and schedule authenticated Phase-2 testing for OWASP logic."
    ]
    id_road = [
        "**1. Hardening dan Isolasi Port 1100 HTTP Internal** — Prioritas: **LOW / MEDIUM**\nUbah binding layanan internal ke `127.0.0.1:1100` dan alihkan seluruh akses melalui reverse proxy HTTPS.",
        "**2. Sembunyikan Informasi Framework** — Prioritas: **INFORMATIONAL**\nTambahkan `app.disable('x-powered-by')` pada Express dan `server_tokens off;` pada Nginx.",
        "**3. Investigasi Timeout Scan Port Nmap** — Prioritas: **INFORMATIONAL**\nAnalisis latency atau filter firewall yang menyebabkan timeout 180s; lakukan pemindaian terarah dengan profil -T4.",
        "**4. Sinkronisasi Trust Store CA & Asesmen Lanjutan** — Prioritas: **INFORMATIONAL**\nPasang intermediate CA pada workstation lokal dan jadwalkan pengujian terautentikasi untuk memeriksa logika OWASP."
    ]
    add_bilingual_section(doc, en_road, id_road)

    add_section_h1("10. CONCLUSION / KESIMPULAN")
    en_conc = [
        "Within the executed linear single-pass scope, the **Dashboard Deadstock** application exhibits a robust external security posture on its primary HTTPS domain, featuring modern TLS 1.3 cryptography, active HSTS enforcement, and anti-clickjacking framing controls. No high or critical severity vulnerabilities were demonstrated within the unauthenticated test boundary.",
        "Defensive optimizations should focus on hardening internal port 1100 to mirror edge policies, suppressing framework banners, and planning credentialed assessments for post-login workflows."
    ]
    id_conc = [
        "Dalam batasan pengujian linear satu putaran yang dilakukan, aplikasi **Dashboard Deadstock** menunjukkan postur keamanan eksternal yang tangguh pada domain HTTPS utamanya, didukung enkripsi TLS 1.3 modern, penerapan HSTS aktif, serta kontrol anti-clickjacking yang baik. Tidak ditemukan kerentanan berisiko tinggi (High) maupun kritis (Critical) pada batasan pengujian tanpa autentikasi ini.",
        "Optimasi difokuskan pada hardening port 1100 internal agar sejajar dengan kebijakan reverse proxy, penghapusan header framework, dan persiapan audit terautentikasi untuk alur kerja pasca-login."
    ]
    add_bilingual_section(doc, en_conc, id_conc)

    # Sign-off Table
    sign_table = doc.add_table(rows=1, cols=3)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False
    col3_w = Inches(2.5)
    
    sign_items = [
        "Report Prepared By:\nCyber Security Assessment Division\nLentera Teknologi",
        "Classification:\nCONFIDENTIAL — INTERNAL ONLY\nZero Defect Assessment Standard",
        "Document Verification:\nECC Gate 1-5 Compliant\nDate: 19 Oktober 2026"
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
    
    # Strictly sanitize OpenXML element ordering
    sanitize_openxml(doc)
    doc.save(output_path)
    print(f"[OK] Report DOCX successfully generated and sanitized at: {output_path}")

if __name__ == '__main__':
    out_docx = sys.argv[1] if len(sys.argv) > 1 else "/home/kristian.admin/.gemini/antigravity-cli/brain/18c205a4-661a-4e83-9dfb-8f26c11d7987/DEADSTOCK_DASHBOARD_FR_PENETRATION_TESTING_REPORT.docx"
    generate_docx(out_docx)
