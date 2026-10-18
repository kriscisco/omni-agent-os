#!/usr/bin/env python3
"""
build_bims_pdf.py
Compiles the BIMS / Rekapitulasi Budget FR - Estate Penetration Testing Report
into an executive, bilingual PDF publication matching the Lentera Teknologi
pentest report format.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 36
MARGIN_Y = 40
PRINTABLE_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' along
    with running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # Top Running Header (Pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0f172a"))
            self.drawString(MARGIN_X, PAGE_HEIGHT - 28, "LENTERA TEKNOLOGI")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(MARGIN_X + 90, PAGE_HEIGHT - 28, "|   BIMS / Rekapitulasi Budget FR - Estate   —   Internal Pentest Report")
            
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(MARGIN_X, PAGE_HEIGHT - 32, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 32)

        # Bottom Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(MARGIN_X, 32, PAGE_WIDTH - MARGIN_X, 32)

        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#991b1b"))
        self.drawString(MARGIN_X, 22, "CONFIDENTIAL")
        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(MARGIN_X + 68, 22, "— Internal Security Assessment Report | Non-Destructive OWASP Single-Pass")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN_X, 22, page_str)
        self.restoreState()


def get_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'OrgHeader': ParagraphStyle(
            'OrgHeader',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0284c7'),
            alignment=TA_LEFT,
            spaceAfter=4
        ),
        'DocTitle': ParagraphStyle(
            'DocTitle',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_LEFT,
            spaceAfter=3
        ),
        'DocSub': ParagraphStyle(
            'DocSub',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#475569'),
            alignment=TA_LEFT,
            spaceAfter=12
        ),
        'SectionH1': ParagraphStyle(
            'SectionH1',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        ),
        'SectionH2': ParagraphStyle(
            'SectionH2',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_JUSTIFY,
            spaceAfter=4
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold',
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        ),
        'ColHeaderEn': ParagraphStyle(
            'ColHeaderEn',
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#0369a1'),
            alignment=TA_LEFT
        ),
        'ColHeaderId': ParagraphStyle(
            'ColHeaderId',
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#047857'),
            alignment=TA_LEFT
        ),
        'TableHead': ParagraphStyle(
            'TableHead',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_LEFT
        ),
        'TableHeadCenter': ParagraphStyle(
            'TableHeadCenter',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#0f172a'),
            alignment=TA_CENTER
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            fontName='Helvetica',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_LEFT
        ),
        'TableCellCenter': ParagraphStyle(
            'TableCellCenter',
            fontName='Helvetica',
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_CENTER
        ),
        'TerminalText': ParagraphStyle(
            'TerminalText',
            fontName='Courier',
            fontSize=6.5,
            leading=8.5,
            textColor=colors.HexColor('#f8fafc')
        ),
        'BadgeHigh': ParagraphStyle(
            'BadgeHigh',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor('#991b1b'),
            alignment=TA_CENTER
        ),
        'BadgeMed': ParagraphStyle(
            'BadgeMed',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor('#92400e'),
            alignment=TA_CENTER
        ),
        'BadgeLow': ParagraphStyle(
            'BadgeLow',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor('#1e40af'),
            alignment=TA_CENTER
        ),
        'BadgeInfo': ParagraphStyle(
            'BadgeInfo',
            fontName='Helvetica-Bold',
            fontSize=7.5,
            leading=9,
            textColor=colors.HexColor('#334155'),
            alignment=TA_CENTER
        )
    }
    return styles

def build_bilingual_table(en_html, id_html, styles, en_title="English", id_title="Bahasa Indonesia"):
    col_w = PRINTABLE_WIDTH / 2.0
    
    header_data = [
        [
            Paragraph(f"<b>{en_title}</b>", styles['ColHeaderEn']),
            Paragraph(f"<b>{id_title}</b>", styles['ColHeaderId'])
        ]
    ]
    
    content_data = [
        [
            Paragraph(en_html, styles['Body']),
            Paragraph(id_html, styles['Body'])
        ]
    ]
    
    tbl_data = header_data + content_data
    
    t = Table(tbl_data, colWidths=[col_w, col_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e0f2fe')), # Soft Sky Blue
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#d1fae5')), # Soft Mint Green
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#f8fafc')), # Crisp Slate 50
        ('BACKGROUND', (1, 1), (1, 1), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def build_terminal_block(text, styles):
    lines = [f"{line}" for line in text.strip().split("\n")]
    formatted = "<br/>".join(lines).replace(" ", "&nbsp;")
    p = Paragraph(formatted, styles['TerminalText'])
    
    t = Table([[p]], colWidths=[PRINTABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')), # Slate 900
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#334155')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def generate_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_Y,
        bottomMargin=MARGIN_Y
    )
    
    styles = get_styles()
    story = []
    
    # -------------------------------------------------------------
    # COVER / HEADER BLOCK
    # -------------------------------------------------------------
    story.append(Paragraph("LENTERA TEKNOLOGI — CYBER SECURITY ASSESSMENT SERVICE", styles['OrgHeader']))
    story.append(Paragraph("BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate", styles['DocTitle']))
    story.append(Paragraph("INTERNAL WEB PENETRATION TESTING REPORT — 18 OKTOBER 2026", styles['DocSub']))
    
    meta_data = [
        [Paragraph("<b>Target System</b>", styles['TableHead']), Paragraph("Rekapitulasi Budget FR - Estate (BIMS) — <code>https://rekapbudget-estate.first-resources.com</code> / <code>10.110.1.9:1627</code>", styles['TableCell'])],
        [Paragraph("<b>DNS / Routing</b>", styles['TableHead']), Paragraph("CNAME <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code> (Reverse Proxy)", styles['TableCell'])],
        [Paragraph("<b>Assessment Scope</b>", styles['TableHead']), Paragraph("Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran)", styles['TableCell'])],
        [Paragraph("<b>Attacker / Audit Node</b>", styles['TableHead']), Paragraph("Internal Workstation Node (Linux Security Subsystem / RFC1918 Scope)", styles['TableCell'])],
        [Paragraph("<b>Access Level Tested</b>", styles['TableHead']), Paragraph("Unauthenticated Access & Controlled Dummy Credential Authentication Probe", styles['TableCell'])],
        [Paragraph("<b>Classification</b>", styles['TableHead']), Paragraph("<b>CONFIDENTIAL — INTERNAL ENTERPRISE SECURITY ASSESSMENT</b>", styles['TableCell'])],
    ]
    meta_table = Table(meta_data, colWidths=[120, PRINTABLE_WIDTH - 120])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 1. EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    story.append(Paragraph("1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF", styles['SectionH1']))
    en_exec = (
        "On 18 October 2026, a focused, non-destructive internal web penetration test was conducted against "
        "the <b>BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate</b> application. "
        "Assessment targeted both the public HTTPS hostname (<code>https://rekapbudget-estate.first-resources.com</code> "
        "resolving to <code>10.100.2.64</code>) and the direct internal instance (<code>http://10.110.1.9:1627</code>).<br/><br/>"
        "Testing operated under a linear, single-pass OWASP Top 10 methodology designed to avoid system loops, deep recursion, "
        "or service denial. The principal high-risk finding is <b>F-01: Plaintext HTTP Transport on Internal Login Endpoint (Port 1627)</b>. "
        "Server <code>10.110.1.9:1627</code> serves an unencrypted HTTP/1.0 interface with an active login form (<code>POST /masuk</code>), "
        "exposing credentials and session tokens to internal network eavesdropping and MitM interception.<br/><br/>"
        "Two configuration anomalies were identified: <b>F-02: Permissive CSP (unsafe-inline)</b> and <b>F-03: Redundant Security Headers</b>. "
        "Perimeter defenses on HTTPS demonstrated valid wildcard Sectigo TLS certificates, HSTS, and 401 dummy auth rejection.<br/><br/>"
        "<b>Overall Assessment:</b> Evidence supports <b>1 High-Risk finding</b> and <b>2 Configuration Weaknesses</b>. Post-login cookie flags "
        "and IDOR remain unverified due to single-pass constraints."
    )
    id_exec = (
        "Pada 18 Oktober 2026 dilakukan pengujian penetrasi web internal non-destruktif terhadap sistem "
        "<b>BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate</b>. Pengujian mencakup "
        "hostname publik (<code>https://rekapbudget-estate.first-resources.com</code> ter-resolve ke <code>10.100.2.64</code>) "
        "dan instans internal langsung (<code>http://10.110.1.9:1627</code>).<br/><br/>"
        "Pengujian menerapkan alur linear satu putaran bebas macet tanpa brute-force atau crawling rekursif. "
        "Temuan utama berisiko tinggi adalah <b>F-01: Transport Plaintext HTTP pada Endpoint Login Internal (Port 1627)</b>. "
        "Host <code>10.110.1.9:1627</code> menjalankan layanan HTTP/1.0 tanpa enkripsi (<code>Server: RBFR</code>) yang menyajikan form login "
        "(<code>POST /masuk</code>), membuka celah penyadapan kredensial dan sesi di jaringan lokal.<br/><br/>"
        "Ditemukan pula dua kelemahan konfigurasi: <b>F-02: CSP Permisif (unsafe-inline)</b> dan <b>F-03: Duplikasi Header Keamanan</b>. "
        "Sisi perimeter HTTPS terverifikasi kuat dengan sertifikat wildcard Sectigo valid, HSTS aktif, serta penolakan login dummy 401.<br/><br/>"
        "<b>Kesimpulan Umum:</b> Hasil mendukung <b>1 Temuan High</b> dan <b>2 Kelemahan Konfigurasi</b>. Atribut cookie sesi dan "
        "IDOR ditandai belum teruji akibat limitasi iterasi 1 putaran."
    )
    story.append(build_bilingual_table(en_exec, id_exec, styles))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 2. TARGET SYSTEM & ASSESSMENT PARAMETERS
    # -------------------------------------------------------------
    story.append(Paragraph("2. TARGET SYSTEM & ASSESSMENT PARAMETERS", styles['SectionH1']))
    en_params = (
        "<b>Target 1 (Public Hostname):</b> <code>https://rekapbudget-estate.first-resources.com</code><br/>"
        "• DNS Resolution: CNAME <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code><br/>"
        "• Transport / Web Stack: Nginx Reverse Proxy, HTTP/2 over TLS 1.3/1.2<br/>"
        "• Certificate: <code>*.first-resources.com</code> (Sectigo Public Server Authentication CA DV R36)<br/>"
        "• Validity Period: 2026-06-29 to 2027-01-13<br/><br/>"
        "<b>Target 2 (Internal Direct Service):</b> <code>http://10.110.1.9:1627</code><br/>"
        "• Network Type: Direct RFC1918 IPv4 Private Address (No PTR/DNS)<br/>"
        "• Web Stack: HTTP/1.0 Plaintext (Server banner: <code>RBFR</code>)<br/>"
        "• Application Title: Rekapitulasi Budget FR - Estate (Identical BIMS application)<br/><br/>"
        "<b>Engagement Boundary:</b> Isolated evaluation strictly for the BIMS system scope."
    )
    id_params = (
        "<b>Target 1 (Hostname Publik):</b> <code>https://rekapbudget-estate.first-resources.com</code><br/>"
        "• Resolusi DNS: CNAME <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code><br/>"
        "• Transport / Stack: Nginx Reverse Proxy, HTTP/2 melalui TLS 1.3/1.2<br/>"
        "• Sertifikat: <code>*.first-resources.com</code> (Sectigo Public Server Authentication CA DV R36)<br/>"
        "• Masa Berlaku: 2026-06-29 hingga 2027-01-13<br/><br/>"
        "<b>Target 2 (Layanan Internal Langsung):</b> <code>http://10.110.1.9:1627</code><br/>"
        "• Tipe Jaringan: Alamat Privat IPv4 RFC1918 Langsung (Tanpa PTR/DNS)<br/>"
        "• Stack Web: HTTP/1.0 Plaintext (Banner server: <code>RBFR</code>)<br/>"
        "• Judul Aplikasi: Rekapitulasi Budget FR - Estate (Aplikasi BIMS identik)<br/><br/>"
        "<b>Batasan Engagement:</b> Evaluasi terisolasi khusus untuk ruang lingkup sistem BIMS."
    )
    story.append(build_bilingual_table(en_params, id_params, styles))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 3. METHODOLOGY
    # -------------------------------------------------------------
    story.append(Paragraph("3. TESTING METHODOLOGY / METODOLOGI", styles['SectionH1']))
    en_meth = (
        "<b>1. Passive Reconnaissance:</b> DNS resolution, HTTP-to-HTTPS redirect validation, TLS chain verification, "
        "and metadata inspection (<code>/robots.txt</code>, <code>/.well-known/security.txt</code>).<br/>"
        "<b>2. Targeted TCP Enumeration:</b> Rapid single-pass scan via Nmap (<code>-sT -sV -sC -T4 --top-ports 1000 -p1627</code>) "
        "against host <code>10.110.1.9</code> without UDP flooding or disruptive probes.<br/>"
        "<b>3. OWASP Web Analysis:</b> Non-destructive audit of login endpoint (<code>/masuk</code>), transport security verification, "
        "safe dummy credential probing, security header analysis (CSP, HSTS, X-Frame-Options), and cookie inspection.<br/>"
        "<b>4. Evidence Classification:</b> Strict segregation of confirmed exploitable risks vs configuration anomalies vs untested limits."
    )
    id_meth = (
        "<b>1. Reconnaissance Pasif:</b> Resolusi DNS, validasi redirect HTTP-ke-HTTPS, verifikasi rantai TLS, "
        "dan pemeriksaan metadata (<code>/robots.txt</code>, <code>/.well-known/security.txt</code>).<br/>"
        "<b>2. Enumerasi TCP Terarah:</b> Pemindaian satu putaran cepat via Nmap (<code>-sT -sV -sC -T4 --top-ports 1000 -p1627</code>) "
        "pada host <code>10.110.1.9</code> tanpa UDP scan maupun probe agresif.<br/>"
        "<b>3. Analisis Web OWASP:</b> Audit non-destruktif endpoint login (<code>/masuk</code>), verifikasi keamanan transport, "
        "pengujian aman kredensial dummy, inspeksi security headers (CSP, HSTS, X-Frame-Options), dan inspeksi cookie.<br/>"
        "<b>4. Klasifikasi Bukti:</b> Pemisahan ketat antara risiko nyata terverifikasi, anomali konfigurasi, dan batasan belum teruji."
    )
    story.append(build_bilingual_table(en_meth, id_meth, styles))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 4. RISK MATRIX & FINDINGS OVERVIEW
    # -------------------------------------------------------------
    story.append(Paragraph("4. RISK MATRIX & FINDINGS OVERVIEW / MATRIKS RISIKO & TEMUAN", styles['SectionH1']))
    
    matrix_data = [
        [
            Paragraph("<b>Finding ID</b>", styles['TableHead']),
            Paragraph("<b>Security Issue / Isu Keamanan</b>", styles['TableHead']),
            Paragraph("<b>Severity</b>", styles['TableHeadCenter']),
            Paragraph("<b>Status / Verification Note</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>F-01</b>", styles['TableCell']),
            Paragraph("<b>Plaintext HTTP Transport on Internal Login Endpoint</b><br/><i>Transport HTTP Plaintext pada Endpoint Login (10.110.1.9:1627)</i>", styles['TableCell']),
            Paragraph("<b>HIGH</b>", styles['BadgeHigh']),
            Paragraph("Verified Vulnerability (CWE-319)<br/><i>Terverifikasi Nyata</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>F-02</b>", styles['TableCell']),
            Paragraph("<b>Permissive Content Security Policy with unsafe-inline</b><br/><i>Kebijakan CSP Permisif Mengizinkan unsafe-inline</i>", styles['TableCell']),
            Paragraph("<b>MEDIUM</b>", styles['BadgeMed']),
            Paragraph("Configuration Weakness (CWE-1021/79)<br/><i>Kelemahan Konfigurasi</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>F-03</b>", styles['TableCell']),
            Paragraph("<b>Redundant & Conflicting Security Headers from Proxy Layer</b><br/><i>Duplikasi dan Konflik Header Keamanan Akibat Layering Proxy</i>", styles['TableCell']),
            Paragraph("<b>LOW</b>", styles['BadgeLow']),
            Paragraph("Configuration Inconsistency (CWE-16)<br/><i>Inkonsistensi Konfigurasi</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-01</b>", styles['TableCell']),
            Paragraph("<b>Web Server & Backend Tech Stack Banner Disclosure</b><br/><i>Pengungkapan Banner Layanan Server (nginx, Server: RBFR)</i>", styles['TableCell']),
            Paragraph("<b>INFO</b>", styles['BadgeInfo']),
            Paragraph("Operational Hygiene Observation<br/><i>Observasi Higiene Operasional</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-02</b>", styles['TableCell']),
            Paragraph("<b>Metadata Path Redirect & TLS Validation Anomalies</b><br/><i>Anomali Redirect Metadata & Error Validasi TLS (curl 60 / 35)</i>", styles['TableCell']),
            Paragraph("<b>INFO</b>", styles['BadgeInfo']),
            Paragraph("Network Telemetry Recording<br/><i>Catatan Telemetri Jaringan</i>", styles['TableCell'])
        ],
    ]
    matrix_table = Table(matrix_data, colWidths=[45, 230, 65, PRINTABLE_WIDTH - 340])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fff1f2')), # Tint High
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fffbeb')), # Tint Medium
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#eff6ff')), # Tint Low
        ('BACKGROUND', (0, 4), (-1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 5. DETAILED FINDINGS BREAKDOWN
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN", styles['SectionH1']))
    
    # Finding F-01
    story.append(Paragraph("F-01: Plaintext HTTP Transport on Internal Login Endpoint (Port 1627)", styles['SectionH2']))
    en_f01 = (
        "<b>Risk Rating:</b> HIGH &nbsp;|&nbsp; <b>CWE:</b> CWE-319 &nbsp;|&nbsp; <b>Status:</b> Confirmed Verified<br/><br/>"
        "<b>Impact:</b><br/>"
        "The application at <code>http://10.110.1.9:1627</code> runs an unencrypted HTTP/1.0 service serving an active "
        "login form (<code>POST /masuk</code>). Because traffic lacks Transport Layer Security (TLS), user/admin credentials "
        "and session cookies can be intercepted via ARP spoofing, promiscuous monitoring, or MitM attacks within the internal network.<br/><br/>"
        "<b>Detailed Narrative:</b><br/>"
        "Nmap scan revealed TCP port 1627 is open (<code>Server: RBFR</code>). Initial HTTPS probes failed with "
        "<code>curl: (35) wrong version number</code>. HTTP/1.0 GET returned a 3,995-byte HTML payload with login form "
        "(username, password). A safe dummy credential probe produced <code>HTTP 401 Unauthorized</code>, proving the auth gateway is live.<br/><br/>"
        "<b>Recommended Remediation:</b><br/>"
        "1. Rebind BIMS service to <code>127.0.0.1:1627</code> and enforce access through an HTTPS reverse proxy.<br/>"
        "2. Block direct cross-VLAN inbound access to port 1627 using host-level firewall rules.<br/>"
        "3. Force immediate HTTP 301 redirection to HTTPS if port 1627 remains temporarily active.<br/>"
        "4. Rotate all user credentials previously entered via this endpoint."
    )
    id_f01 = (
        "<b>Risk Rating:</b> HIGH &nbsp;|&nbsp; <b>CWE:</b> CWE-319 &nbsp;|&nbsp; <b>Status:</b> Terverifikasi Nyata<br/><br/>"
        "<b>Dampak:</b><br/>"
        "Layanan pada <code>http://10.110.1.9:1627</code> beroperasi pada HTTP/1.0 tanpa enkripsi dan menyajikan form login aktif "
        "(<code>POST /masuk</code>). Karena tidak ada proteksi TLS, kredensial pengguna/admin dan cookie sesi berisiko disadap "
        "melalui network sniffing, ARP poisoning, atau serangan MitM pada jaringan lokal RFC1918.<br/><br/>"
        "<b>Deskripsi Rinci:</b><br/>"
        "Scan Nmap menemukan port TCP 1627 terbuka (<code>Server: RBFR</code>). Probe HTTPS gagal dengan "
        "<code>curl: (35) wrong version number</code>. Permintaan HTTP/1.0 GET menghasilkan respons 3.995 byte memuat form login "
        "(username, password). Uji kirim kredensial dummy menghasilkan <code>HTTP 401 Unauthorized</code>, membuktikan endpoint autentikasi aktif.<br/><br/>"
        "<b>Rekomendasi Perbaikan:</b><br/>"
        "1. Batasi binding BIMS hanya ke <code>127.0.0.1:1627</code> dan wajibkan akses via reverse proxy HTTPS.<br/>"
        "2. Blokir akses langsung antar-VLAN menuju port 1627 dengan firewall host (iptables).<br/>"
        "3. Terapkan redirect 301 otomatis ke HTTPS bila port 1627 tetap dibuka sementara.<br/>"
        "4. Rotasi kata sandi seluruh staf yang pernah login melalui endpoint IP plaintext tersebut."
    )
    story.append(build_bilingual_table(en_f01, id_f01, styles))
    story.append(Spacer(1, 4))
    
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
    story.append(build_terminal_block(term_f01, styles))
    story.append(Spacer(1, 10))
    
    # Finding F-02
    story.append(Paragraph("F-02: Permissive Content Security Policy with unsafe-inline Directives", styles['SectionH2']))
    en_f02 = (
        "<b>Risk Rating:</b> MEDIUM &nbsp;|&nbsp; <b>CWE:</b> CWE-1021 / CWE-79 &nbsp;|&nbsp; <b>Status:</b> Verified Config Flaw<br/><br/>"
        "<b>Impact:</b><br/>"
        "Both endpoints emit a Content Security Policy containing <code>script-src 'unsafe-inline'</code> and "
        "<code>style-src 'unsafe-inline'</code>. This disables modern browser protection against Cross-Site Scripting (XSS), "
        "allowing injected inline scripts to execute if an unsanitized reflection vector exists.<br/><br/>"
        "<b>Detailed Narrative:</b><br/>"
        "Header audits confirmed permissive CSP settings. Reflected XSS probing was not completed due to single-pass iteration limits. "
        "The issue is classified as a verified configuration flaw rather than a demonstrated exploit.<br/><br/>"
        "<b>Recommended Remediation:</b><br/>"
        "Remove <code>'unsafe-inline'</code>, implement cryptographic nonces (<code>'nonce-...'</code>), and perform authenticated XSS audit."
    )
    id_f02 = (
        "<b>Risk Rating:</b> MEDIUM &nbsp;|&nbsp; <b>CWE:</b> CWE-1021 / CWE-79 &nbsp;|&nbsp; <b>Status:</b> Kelemahan Konfigurasi Terverifikasi<br/><br/>"
        "<b>Dampak:</b><br/>"
        "Kedua target menyajikan header CSP yang memuat <code>script-src 'unsafe-inline'</code> dan <code>style-src 'unsafe-inline'</code>. "
        "Hal ini meniadakan perlindungan utama browser terhadap Cross-Site Scripting (XSS), sehingga script berbahaya dapat dieksekusi "
        "bila ditemukan titik injeksi input.<br/><br/>"
        "<b>Deskripsi Rinci:</b><br/>"
        "Pemeriksaan header membuktikan CSP permisif. Pengujian reflected XSS terhenti oleh batas iterasi satu putaran. Isu ini diklasifikasikan "
        "sebagai kelemahan konfigurasi nyata, bukan eksploitasi terbukti.<br/><br/>"
        "<b>Rekomendasi Perbaikan:</b><br/>"
        "Hapus <code>'unsafe-inline'</code>, gunakan cryptographic nonce (<code>'nonce-...'</code>), dan lakukan uji penetrasi terotorisasi lanjutan."
    )
    story.append(build_bilingual_table(en_f02, id_f02, styles))
    story.append(Spacer(1, 4))
    term_f02 = "Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; frame-ancestors 'none'"
    story.append(build_terminal_block(term_f02, styles))
    story.append(Spacer(1, 10))
    
    # Finding F-03
    story.append(Paragraph("F-03: Redundant and Conflicting Security Headers via Reverse Proxy Layering", styles['SectionH2']))
    en_f03 = (
        "<b>Risk Rating:</b> LOW &nbsp;|&nbsp; <b>CWE:</b> CWE-16 &nbsp;|&nbsp; <b>Status:</b> Configuration Inconsistency Confirmed<br/><br/>"
        "<b>Impact:</b><br/>"
        "HTTPS responses emit duplicated and contradictory security headers: <code>X-Frame-Options: DENY</code> and "
        "<code>SAMEORIGIN</code> simultaneously, duplicate <code>Referrer-Policy</code>, and duplicated <code>X-Content-Type-Options</code>. "
        "Browsers may interpret conflicting headers unpredictably, potentially disabling clickjacking defenses.<br/><br/>"
        "<b>Remediation:</b> Designate the edge Nginx reverse proxy as the authoritative header injector; suppress backend duplicates."
    )
    id_f03 = (
        "<b>Risk Rating:</b> LOW &nbsp;|&nbsp; <b>CWE:</b> CWE-16 &nbsp;|&nbsp; <b>Status:</b> Inkonsistensi Konfigurasi Terverifikasi<br/><br/>"
        "<b>Dampak:</b><br/>"
        "Respons HTTPS menyajikan header keamanan ganda yang saling bertentangan: <code>X-Frame-Options: DENY</code> dan "
        "<code>SAMEORIGIN</code> secara bersamaan, duplikasi <code>Referrer-Policy</code>, serta <code>X-Content-Type-Options</code> ganda. "
        "Browser dapat memproses konflik secara acak dan berpotensi membatalkan proteksi anti-clickjacking.<br/><br/>"
        "<b>Rekomendasi Perbaikan:</b> Tetapkan edge reverse proxy Nginx sebagai pengendali header tunggal; bersihkan header duplikat dari backend."
    )
    story.append(build_bilingual_table(en_f03, id_f03, styles))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 6. OBSERVATIONS & 7. VERIFIED CONTROLS
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("6. ADDITIONAL SECURITY OBSERVATIONS & TELEMETRY", styles['SectionH1']))
    en_obs = (
        "<b>O-01 (Server Banner Disclosure):</b> The public endpoint exposes <code>Server: nginx</code> while the internal endpoint exposes "
        "<code>Server: RBFR</code>. Although specific build versions are not displayed, disclosing software names aids attacker fingerprinting.<br/><br/>"
        "<b>O-02 (Metadata Routing & TLS Errors):</b> <code>/robots.txt</code> and <code>/.well-known/security.txt</code> trigger HTTP 303 "
        "redirects to <code>/masuk</code> on port 1627. Strict TLS validation on hostname produced <code>curl (60)</code> due to local trust bundle limits."
    )
    id_obs = (
        "<b>O-01 (Pengungkapan Banner Layanan):</b> Endpoint publik mengekspos <code>Server: nginx</code> sedangkan endpoint internal mengekspos "
        "<code>Server: RBFR</code>. Kendati versi build spesifik tidak terlihat, informasi ini mempermudah pemetaan teknologi target.<br/><br/>"
        "<b>O-02 (Routing Metadata & Error TLS):</b> Path <code>/robots.txt</code> dan <code>/.well-known/security.txt</code> dialihkan via HTTP 303 "
        "ke <code>/masuk</code> pada port 1627. Validasi TLS strict pada hostname memunculkan error <code>curl (60)</code> akibat trust store lokal."
    )
    story.append(build_bilingual_table(en_obs, id_obs, styles))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("7. VERIFIED CONTROLS & NEGATIVE TEST RESULTS / KONTROL TERVERIFIKASI", styles['SectionH1']))
    ctrl_data = [
        [
            Paragraph("<b>Security Parameter & Control (English)</b>", styles['TableHead']),
            Paragraph("<b>Hasil Verifikasi Lapangan (Bahasa Indonesia)</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Host Network Attack Surface:</b> Nmap scan on host 10.110.1.9 across top-1000 ports plus port 1627 confirmed that only TCP/1627 is open.", styles['TableCell']),
            Paragraph("<b>Permukaan Serangan Host:</b> Pemindaian Nmap pada 10.110.1.9 mengonfirmasi hanya port 1627 yang terbuka. Tidak ada port manajemen (SSH, RDP, DB) yang terekspos.", styles['TableCell'])
        ],
        [
            Paragraph("<b>HTTP-to-HTTPS Redirection:</b> Hostname <code>rekapbudget-estate.first-resources.com</code> enforces HTTP 301 Moved Permanently redirect to HTTPS.", styles['TableCell']),
            Paragraph("<b>Pengalihan HTTP ke HTTPS:</b> Hostname publik secara benar menerapkan pengalihan 301 dari HTTP biasa ke koneksi aman HTTPS.", styles['TableCell'])
        ],
        [
            Paragraph("<b>HSTS Implementation:</b> Strict-Transport-Security active with <code>max-age=15552000</code> and <code>includeSubDomains</code>.", styles['TableCell']),
            Paragraph("<b>Penerapan HSTS:</b> Header HSTS aktif pada HTTPS dengan durasi 180 hari (15552000 detik) mencakup seluruh subdomain.", styles['TableCell'])
        ],
        [
            Paragraph("<b>TLS Certificate Legitimacy:</b> Valid commercial Sectigo wildcard certificate (<code>*.first-resources.com</code>) active through January 2027.", styles['TableCell']),
            Paragraph("<b>Validitas Sertifikat TLS:</b> Menggunakan sertifikat resmi Sectigo wildcard valid dengan masa aktif hingga 13 Januari 2027.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Authentication Rejection:</b> Dummy POST probe to <code>/masuk</code> returned <code>HTTP 401 Unauthorized</code> without error bypass.", styles['TableCell']),
            Paragraph("<b>Penolakan Autentikasi Dummy:</b> Percobaan kredensial palsu pada <code>/masuk</code> menghasilkan respons 401 Unauthorized yang valid.", styles['TableCell'])
        ],
    ]
    ctrl_table = Table(ctrl_data, colWidths=[PRINTABLE_WIDTH / 2.0, PRINTABLE_WIDTH / 2.0])
    ctrl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(ctrl_table)
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 8. LIMITATIONS & UNTESTED ITEMS
    # -------------------------------------------------------------
    story.append(Paragraph("8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN", styles['SectionH1']))
    en_lim = (
        "• <b>Linear Single-Pass Constraint:</b> Conducted under strict anti-loop execution guidelines (max 1 probe per tool, no retries, no deep recursion).<br/>"
        "• <b>Session Cookie Flags Unverified:</b> No <code>Set-Cookie</code> header observed on unauthenticated GET requests. Post-auth flags (Secure, HttpOnly, SameSite) could not be verified.<br/>"
        "• <b>Input Reflection & XSS Inconclusive:</b> Reflection probing was suspended upon reaching subtask iteration limits; no malicious payloads were transmitted.<br/>"
        "• <b>Rate Limiting Inconclusive:</b> A single dummy attempt gave HTTP 401 without 429/Retry-After. Progressive throttling cannot be conclusively confirmed from one request.<br/>"
        "• <b>Zero Destructive Impact:</b> No brute-forcing, password spraying, SQL injection fuzzing, or DoS testing was conducted."
    )
    id_lim = (
        "• <b>Batasan Alur Linear 1 Putaran:</b> Dilakukan dengan pedoman bebas macet ketat (maksimal 1 percobaan per tool, tanpa retry, tanpa crawling dalam).<br/>"
        "• <b>Flag Cookie Sesi Belum Teruji:</b> Header <code>Set-Cookie</code> tidak muncul pada GET awal. Flag pasca-login (Secure, HttpOnly, SameSite) belum dapat dinilai.<br/>"
        "• <b>Uji Reflected XSS Belum Tuntas:</b> Probe parameter reflection terhenti oleh limit iterasi; tidak ada payload eksploitatif yang dievaluasi.<br/>"
        "• <b>Rate Limiting Belum Konklusif:</b> Satu percobaan dummy menghasilkan HTTP 401 tanpa header 429. Mekanisme lock-out membutuhkan uji multi-request terotorisasi.<br/>"
        "• <b>Bebas Dampak Destruktif:</b> Tidak dilakukan brute-force, password spraying, injeksi SQL merusak, atau uji kelumpuhan sistem (DoS)."
    )
    story.append(build_bilingual_table(en_lim, id_lim, styles))
    story.append(Spacer(1, 10))
    
    # -------------------------------------------------------------
    # 9. REMEDIATION ROADMAP & 10. CONCLUSION
    # -------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN", styles['SectionH1']))
    en_road = (
        "<b>1. Decommission or Proxy Plaintext HTTP Port 1627</b> — Priority: <b>HIGH</b><br/>"
        "Rebind internal BIMS service to <code>127.0.0.1:1627</code> and enforce access through an authoritative HTTPS reverse proxy. "
        "Enforce host firewall rules blocking cross-VLAN traffic and rotate credentials used across internal tests.<br/><br/>"
        "<b>2. Normalize Security Headers at Edge Reverse Proxy</b> — Priority: <b>MEDIUM</b><br/>"
        "Consolidate security headers in Nginx configuration. Remove duplicates and enforce single authoritative directives "
        "(<code>X-Frame-Options: DENY</code>, <code>Referrer-Policy: strict-origin-when-cross-origin</code>). Use <code>proxy_hide_header</code>.<br/><br/>"
        "<b>3. Harden Content Security Policy (CSP)</b> — Priority: <b>MEDIUM</b><br/>"
        "Remove <code>'unsafe-inline'</code> from script-src and style-src. Adopt cryptographic nonces or SHA-256 hashes.<br/><br/>"
        "<b>4. Enforce Session Cookie Flags Post-Login</b> — Priority: <b>LOW / MEDIUM</b><br/>"
        "Ensure all cookies issued upon successful authentication include <code>Secure; HttpOnly; SameSite=Lax</code>."
    )
    id_road = (
        "<b>1. Tutup atau Alihkan Layanan HTTP Plaintext Port 1627</b> — Prioritas: <b>HIGH</b><br/>"
        "Ubah binding BIMS internal ke <code>127.0.0.1:1627</code> dan wajibkan seluruh akses melalui reverse proxy HTTPS. "
        "Terapkan firewall host untuk memblokir akses langsung antar-VLAN serta lakukan rotasi kredensial pengguna internal.<br/><br/>"
        "<b>2. Normalisasi Header Keamanan pada Reverse Proxy</b> — Prioritas: <b>MEDIUM</b><br/>"
        "Satukan konfigurasi header pada Nginx. Hapus nilai duplikat dan tetapkan satu kebijakan tegas "
        "(<code>X-Frame-Options: DENY</code>, <code>Referrer-Policy: strict-origin-when-cross-origin</code>). Gunakan <code>proxy_hide_header</code>.<br/><br/>"
        "<b>3. Perketat Content Security Policy (CSP)</b> — Prioritas: <b>MEDIUM</b><br/>"
        "Hapus <code>'unsafe-inline'</code> pada direktif script-src dan style-src. Terapkan mekanisme nonce atau hash SHA-256.<br/><br/>"
        "<b>4. Terapkan Flag Cookie Sesi Pasca-Login</b> — Prioritas: <b>LOW / MEDIUM</b><br/>"
        "Pastikan cookie sesi yang diterbitkan setelah login memuat atribut <code>Secure; HttpOnly; SameSite=Lax</code>."
    )
    story.append(build_bilingual_table(en_road, id_road, styles))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("10. CONCLUSION / KESIMPULAN", styles['SectionH1']))
    en_conc = (
        "Within the executed linear single-pass scope, the <b>BIMS / Rekapitulasi Budget FR - Estate</b> application demonstrates "
        "effective perimeter security controls on its public HTTPS interface (valid wildcard TLS, HSTS, and 401 auth rejection). "
        "However, exposing an unencrypted HTTP/1.0 login interface directly on internal IP <code>10.110.1.9:1627</code> introduces "
        "a critical transport flaw (<b>F-01: High</b>) that bypasses transport encryption and leaves authentication credentials "
        "vulnerable to internal network interception.<br/><br/>"
        "Remediation must prioritize closing or proxying port 1627 behind HTTPS, followed by normalizing duplicate security headers "
        "and hardening the Content Security Policy to achieve comprehensive enterprise production posture."
    )
    id_conc = (
        "Dalam cakupan pengujian linear satu putaran yang dilakukan, sistem <b>BIMS / Rekapitulasi Budget FR - Estate</b> menunjukkan "
        "pertahanan perimeter yang efektif pada interface HTTPS publiknya (sertifikat wildcard TLS valid, HSTS, dan penolakan 401 auth). "
        "Namun, ketersediaan antarmuka login HTTP/1.0 tanpa enkripsi langsung pada IP internal <code>10.110.1.9:1627</code> memunculkan "
        "kerentanan transport kritis (<b>F-01: High</b>) yang mengabaikan enkripsi lalu lintas data dan membuka celah penyadapan kredensial.<br/><br/>"
        "Remediasi harus memprioritaskan penutupan atau pengalihan port 1627 ke jalur HTTPS, disusul dengan normalisasi header keamanan ganda "
        "serta pengetatan Content Security Policy demi mencapai postur keamanan produksi enterprise yang tangguh."
    )
    story.append(build_bilingual_table(en_conc, id_conc, styles))
    story.append(Spacer(1, 15))
    
    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Report Prepared By:</b><br/>Cyber Security Assessment Division<br/>Lentera Teknologi", styles['TableCell']),
            Paragraph("<b>Classification:</b><br/>CONFIDENTIAL — INTERNAL ONLY<br/>Zero Defect Assessment Standard", styles['TableCell']),
            Paragraph("<b>Document Verification:</b><br/>ECC Gate 1-5 Compliant<br/>Date: 18 Oktober 2026", styles['TableCell'])
        ]
    ]
    sign_table = Table(sign_data, colWidths=[PRINTABLE_WIDTH / 3.0] * 3)
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sign_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Report PDF successfully generated at: {output_path}")

if __name__ == '__main__':
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "/home/kristian.admin/.gemini/antigravity-cli/brain/18c205a4-661a-4e83-9dfb-8f26c11d7987/BIMS_REKAP_BUDGET_FR_PENETRATION_TESTING_REPORT.pdf"
    generate_pdf(out_pdf)
