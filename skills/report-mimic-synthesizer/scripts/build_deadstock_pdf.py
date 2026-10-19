#!/usr/bin/env python3
"""
build_deadstock_pdf.py
Generates an executive, bilingual PDF publication for the Dashboard Deadstock
(First Resources Group) Penetration Testing Report, matching the Lentera Teknologi
pentest report format.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 36
MARGIN_Y = 40
PRINTABLE_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)

class NumberedCanvas(canvas.Canvas):
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
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0f172a"))
            self.drawString(MARGIN_X, PAGE_HEIGHT - 28, "LENTERA TEKNOLOGI")
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(MARGIN_X + 90, PAGE_HEIGHT - 28, "|   Dashboard Deadstock   —   Internal Pentest Report")
            
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(MARGIN_X, PAGE_HEIGHT - 32, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 32)

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
            'OrgHeader', fontName='Helvetica-Bold', fontSize=11, leading=14,
            textColor=colors.HexColor('#0284c7'), alignment=TA_LEFT, spaceAfter=4
        ),
        'DocTitle': ParagraphStyle(
            'DocTitle', fontName='Helvetica-Bold', fontSize=18, leading=22,
            textColor=colors.HexColor('#0f172a'), alignment=TA_LEFT, spaceAfter=3
        ),
        'DocSub': ParagraphStyle(
            'DocSub', fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=colors.HexColor('#475569'), alignment=TA_LEFT, spaceAfter=12
        ),
        'SectionH1': ParagraphStyle(
            'SectionH1', fontName='Helvetica-Bold', fontSize=12, leading=15,
            textColor=colors.HexColor('#0f172a'), spaceBefore=12, spaceAfter=6, keepWithNext=True
        ),
        'SectionH2': ParagraphStyle(
            'SectionH2', fontName='Helvetica-Bold', fontSize=10, leading=13,
            textColor=colors.HexColor('#1e293b'), spaceBefore=8, spaceAfter=4, keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', fontName='Helvetica', fontSize=8, leading=11,
            textColor=colors.HexColor('#1e293b'), alignment=TA_JUSTIFY, spaceAfter=4
        ),
        'ColHeaderEn': ParagraphStyle(
            'ColHeaderEn', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=colors.HexColor('#0369a1'), alignment=TA_LEFT
        ),
        'ColHeaderId': ParagraphStyle(
            'ColHeaderId', fontName='Helvetica-Bold', fontSize=8.5, leading=11,
            textColor=colors.HexColor('#047857'), alignment=TA_LEFT
        ),
        'TableHead': ParagraphStyle(
            'TableHead', fontName='Helvetica-Bold', fontSize=7.5, leading=10,
            textColor=colors.HexColor('#0f172a'), alignment=TA_LEFT
        ),
        'TableHeadCenter': ParagraphStyle(
            'TableHeadCenter', fontName='Helvetica-Bold', fontSize=7.5, leading=10,
            textColor=colors.HexColor('#0f172a'), alignment=TA_CENTER
        ),
        'TableCell': ParagraphStyle(
            'TableCell', fontName='Helvetica', fontSize=7.5, leading=10,
            textColor=colors.HexColor('#1e293b'), alignment=TA_LEFT
        ),
        'TerminalText': ParagraphStyle(
            'TerminalText', fontName='Courier', fontSize=6.5, leading=8.5,
            textColor=colors.HexColor('#f8fafc')
        ),
        'BadgeLow': ParagraphStyle(
            'BadgeLow', fontName='Helvetica-Bold', fontSize=7.5, leading=9,
            textColor=colors.HexColor('#1e40af'), alignment=TA_CENTER
        ),
        'BadgeInfo': ParagraphStyle(
            'BadgeInfo', fontName='Helvetica-Bold', fontSize=7.5, leading=9,
            textColor=colors.HexColor('#334155'), alignment=TA_CENTER
        )
    }
    return styles

def build_bilingual_table(en_html, id_html, styles, en_title="English", id_title="Bahasa Indonesia"):
    col_w = PRINTABLE_WIDTH / 2.0
    header_data = [
        [Paragraph(f"<b>{en_title}</b>", styles['ColHeaderEn']), Paragraph(f"<b>{id_title}</b>", styles['ColHeaderId'])]
    ]
    content_data = [
        [Paragraph(en_html, styles['Body']), Paragraph(id_html, styles['Body'])]
    ]
    t = Table(header_data + content_data, colWidths=[col_w, col_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e0f2fe')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#d1fae5')),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#f8fafc')),
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
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
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
        output_path, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_Y, bottomMargin=MARGIN_Y
    )
    styles = get_styles()
    story = []

    # COVER / HEADER
    story.append(Paragraph("LENTERA TEKNOLOGI — CYBER SECURITY ASSESSMENT SERVICE", styles['OrgHeader']))
    story.append(Paragraph("Dashboard Deadstock / First Resources (FR) Group", styles['DocTitle']))
    story.append(Paragraph("INTERNAL WEB PENETRATION TESTING REPORT — 19 OKTOBER 2026", styles['DocSub']))

    meta_data = [
        [Paragraph("<b>Target System</b>", styles['TableHead']), Paragraph("Dashboard Deadstock — <code>https://deadstock.first-resources.com</code> / <code>10.110.1.9:1100</code>", styles['TableCell'])],
        [Paragraph("<b>DNS / Routing</b>", styles['TableHead']), Paragraph("CNAME <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code> (Infrastructure Masking)", styles['TableCell'])],
        [Paragraph("<b>Assessment Scope</b>", styles['TableHead']), Paragraph("Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran)", styles['TableCell'])],
        [Paragraph("<b>Attacker / Audit Node</b>", styles['TableHead']), Paragraph("Internal Workstation Node (Linux Security Subsystem / RFC1918 Scope)", styles['TableCell'])],
        [Paragraph("<b>Access Level Tested</b>", styles['TableHead']), Paragraph("Unauthenticated Passive Recon, Network Probing, & Application Response Baseline", styles['TableCell'])],
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

    # 1. EXECUTIVE SUMMARY
    story.append(Paragraph("1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF", styles['SectionH1']))
    en_exec = (
        "On 19 October 2026, a focused, non-destructive internal web penetration test was conducted against the "
        "<b>Dashboard Deadstock</b> application across two endpoints: the primary domain <code>https://deadstock.first-resources.com</code> "
        "(resolving via CNAME to <code>10.100.2.64</code>) and the direct internal instance <code>http://10.110.1.9:1100</code>.<br/><br/>"
        "Testing operated under a linear, single-pass OWASP Top 10 methodology with strict zero-retry rules. "
        "Perimeter HTTPS defenses were verified to be solid, with valid commercial Sectigo TLS 1.3 encryption, active HSTS "
        "(<code>max-age=86400</code>), anti-clickjacking (<code>X-Frame-Options: SAMEORIGIN</code>), and MIME-type enforcement.<br/><br/>"
        "The primary observations identified are <b>F-01: Security Header Asymmetry on Port 1100 (Low)</b> and <b>F-02: Framework Disclosure "
        "(X-Powered-By: Express, Informational)</b>. An active port scan wrapper reached timeout (exit 124) and was recorded transparently "
        "as an information boundary.<br/><br/>"
        "<b>Overall Assessment:</b> Evidence confirms <b>1 Low-Risk Finding</b> and <b>1 Informational Observation</b>. Advanced authenticated "
        "categories remain unverified due to scope constraints."
    )
    id_exec = (
        "Pada 19 Oktober 2026 dilakukan pengujian penetrasi web internal non-destruktif terhadap sistem "
        "<b>Dashboard Deadstock</b> pada dua jalur akses: domain HTTPS utama <code>https://deadstock.first-resources.com</code> "
        "(ter-resolve via CNAME ke <code>10.100.2.64</code>) dan instans server internal langsung <code>http://10.110.1.9:1100</code>.<br/><br/>"
        "Pengujian menerapkan alur linear satu putaran bebas macet sesuai standar OWASP Top 10. "
        "Pertahanan perimeter HTTPS terverifikasi kuat dengan enkripsi TLS 1.3 komersial Sectigo valid, HSTS aktif "
        "(<code>max-age=86400</code>), proteksi anti-clickjacking, dan penegakan tipe konten.<br/><br/>"
        "Temuan utama mencakup <b>F-01: Asimetri Header Keamanan pada Port 1100 (Low)</b> dan <b>F-02: Pengungkapan Framework "
        "(X-Powered-By: Express, Informational)</b>. Scan port Nmap mengalami batas waktu (exit 124) dan dicatat transparan "
        "sebagai batas informasi tanpa klaim port palsu.<br/><br/>"
        "<b>Kesimpulan Umum:</b> Hasil mendukung <b>1 Temuan Berisiko Rendah (Low)</b> dan <b>1 Observasi Informasional</b>. "
        "Kategori terautentikasi ditandai belum teruji sesuai batasan 1 putaran."
    )
    story.append(build_bilingual_table(en_exec, id_exec, styles))
    story.append(Spacer(1, 10))

    # 2. TARGET SYSTEM & PARAMETERS
    story.append(Paragraph("2. TARGET SYSTEM & ASSESSMENT PARAMETERS", styles['SectionH1']))
    en_params = (
        "<b>Target 1 (Public Hostname):</b> <code>https://deadstock.first-resources.com</code><br/>"
        "• DNS CNAME: <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code><br/>"
        "• Transport / Web Stack: Nginx Reverse Proxy, TLSv1.3 with <code>TLS_AES_256_GCM_SHA384</code><br/>"
        "• Certificate: <code>*.first-resources.com</code> (Sectigo CA DV R36, valid 2026-06-29 to 2027-01-13)<br/><br/>"
        "<b>Target 2 (Internal Direct Service):</b> <code>http://10.110.1.9:1100</code><br/>"
        "• Network Type: Direct RFC1918 IPv4 Private Address (No PTR/DNS)<br/>"
        "• Web Stack: <code>nginx/1.22.1</code> + Node.js / Express (<code>X-Powered-By: Express</code>)<br/>"
        "• Application Title: Dashboard Deadstock (First Resources Group)<br/><br/>"
        "<b>Engagement Boundary:</b> Isolated evaluation strictly for the Dashboard Deadstock application."
    )
    id_params = (
        "<b>Target 1 (Hostname Publik):</b> <code>https://deadstock.first-resources.com</code><br/>"
        "• DNS CNAME: <code>lkt-infra.first-resources.com</code> &rarr; A <code>10.100.2.64</code><br/>"
        "• Transport / Stack: Nginx Reverse Proxy, TLSv1.3 dengan <code>TLS_AES_256_GCM_SHA384</code><br/>"
        "• Sertifikat: <code>*.first-resources.com</code> (Sectigo CA DV R36, aktif 2026-06-29 s/d 2027-01-13)<br/><br/>"
        "<b>Target 2 (Layanan Internal Langsung):</b> <code>http://10.110.1.9:1100</code><br/>"
        "• Tipe Jaringan: Alamat Privat IPv4 RFC1918 Langsung (Tanpa PTR/DNS)<br/>"
        "• Stack Web: <code>nginx/1.22.1</code> + Node.js / Express (<code>X-Powered-By: Express</code>)<br/>"
        "• Judul Aplikasi: Dashboard Deadstock (First Resources Group)<br/><br/>"
        "<b>Batasan Engagement:</b> Evaluasi terisolasi khusus untuk ruang lingkup aplikasi Dashboard Deadstock."
    )
    story.append(build_bilingual_table(en_params, id_params, styles))
    story.append(Spacer(1, 10))

    # 3. METHODOLOGY
    story.append(Paragraph("3. TESTING METHODOLOGY / METODOLOGI", styles['SectionH1']))
    en_meth = (
        "<b>1. Passive Reconnaissance:</b> DNS resolution via dig, CNAME mapping, httpx status check, and whatweb tech fingerprinting.<br/>"
        "<b>2. Targeted Network Scan:</b> Nmap scan (-sT --top-ports 100 -p1100 -T2). Process timed out at 180s (exit 124) and was recorded transparently without retry.<br/>"
        "<b>3. Application Response Probing:</b> Single-pass GET requests capturing headers and 2 KiB body samples across both targets into <code>app_responses.txt</code>.<br/>"
        "<b>4. TLS & Header Auditing:</b> OpenSSL s_client TLS 1.3 verification, HSTS validation, framing inspection, and asymmetry mapping.<br/>"
        "<b>5. Evidence Synthesis:</b> Separation of factual evidence from tooling artifacts and untested OWASP categories."
    )
    id_meth = (
        "<b>1. Reconnaissance Pasif:</b> Resolusi DNS via dig, pemetaan CNAME, validasi status via httpx, dan fingerprinting teknologi via whatweb.<br/>"
        "<b>2. Scan Jaringan Terarah:</b> Nmap (-sT --top-ports 100 -p1100 -T2). Proses mencapai batas 180s (exit 124) dan dicatat transparan tanpa pengulangan.<br/>"
        "<b>3. Analisis Respons Aplikasi:</b> Permintaan GET satu kali menangkap header dan sampel body 2 KiB pada kedua target ke <code>app_responses.txt</code>.<br/>"
        "<b>4. Audit TLS & Header:</b> Verifikasi OpenSSL s_client TLS 1.3, validasi HSTS, inspeksi framing, dan pemetaan asimetri header.<br/>"
        "<b>5. Sintesis Bukti:</b> Pemisahan tegas antara temuan nyata, keterbatasan alat, dan kategori OWASP yang belum teruji."
    )
    story.append(build_bilingual_table(en_meth, id_meth, styles))
    story.append(Spacer(1, 10))

    # 4. RISK MATRIX & FINDINGS OVERVIEW
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
            Paragraph("<b>Security Header Asymmetry & Unhardened HTTP Port 1100</b><br/><i>Asimetri Header Keamanan & Ketiadaan Hardening Port 1100 HTTP</i>", styles['TableCell']),
            Paragraph("<b>LOW</b>", styles['BadgeLow']),
            Paragraph("Configuration Flaw (CWE-16/1021)<br/><i>Kelemahan Konfigurasi</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>F-02</b>", styles['TableCell']),
            Paragraph("<b>Backend Framework & Server Version Disclosure</b><br/><i>Pengungkapan Framework Backend & Versi Server (X-Powered-By: Express)</i>", styles['TableCell']),
            Paragraph("<b>INFO</b>", styles['BadgeInfo']),
            Paragraph("Technology Exposure (CWE-200)<br/><i>Eksposur Informasi</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-01</b>", styles['TableCell']),
            Paragraph("<b>Network Port Scan Execution Timeout (Exit 124)</b><br/><i>Batas Waktu Eksekusi Scan Port Nmap (Exit 124)</i>", styles['TableCell']),
            Paragraph("<b>INFO</b>", styles['BadgeInfo']),
            Paragraph("Scope Limitation Recording<br/><i>Catatan Keterbatasan Informasi</i>", styles['TableCell'])
        ],
        [
            Paragraph("<b>O-02</b>", styles['TableCell']),
            Paragraph("<b>Incomplete Local Environment TLS Trust Store (Verify Code 21)</b><br/><i>Ketidaklengkapan Trust Store TLS Lokal (Verify Code 21)</i>", styles['TableCell']),
            Paragraph("<b>INFO</b>", styles['BadgeInfo']),
            Paragraph("Local Client Artifact<br/><i>Artefak Lingkungan Penguji</i>", styles['TableCell'])
        ],
    ]
    matrix_table = Table(matrix_data, colWidths=[45, 230, 65, PRINTABLE_WIDTH - 340])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#eff6ff')), # Tint Low
        ('BACKGROUND', (0, 2), (-1, -1), colors.white),
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

    # 5. DETAILED FINDINGS BREAKDOWN
    story.append(PageBreak())
    story.append(Paragraph("5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN", styles['SectionH1']))

    # F-01
    story.append(Paragraph("F-01: Security Header Asymmetry & Unhardened HTTP Port 1100", styles['SectionH2']))
    en_f01 = (
        "<b>Risk Rating:</b> LOW &nbsp;|&nbsp; <b>CWE:</b> CWE-16 / CWE-1021 &nbsp;|&nbsp; <b>Status:</b> Verified Flaw<br/><br/>"
        "<b>Impact:</b> Direct access to <code>http://10.110.1.9:1100</code> omits baseline defensive headers "
        "(Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, CSP). Although no cleartext credential form was "
        "observed on the sampled payload, leaving the internal socket accessible without hardening creates potential exposure.<br/><br/>"
        "<b>Detailed Narrative:</b> Probing confirmed that the HTTPS reverse proxy correctly applies defensive headers, but direct "
        "internal connections to port 1100 receive plain caching headers only. This asymmetry indicates defenses exist solely at "
        "the outer edge proxy.<br/><br/>"
        "<b>Recommended Remediation:</b><br/>"
        "1. Bind port 1100 strictly to <code>127.0.0.1:1100</code>, forcing all traffic via HTTPS reverse proxy.<br/>"
        "2. If direct access is required, inject standard security headers directly in Express/Nginx.<br/>"
        "3. Enforce automatic HTTP 301 redirection to HTTPS."
    )
    id_f01 = (
        "<b>Risk Rating:</b> LOW &nbsp;|&nbsp; <b>CWE:</b> CWE-16 / CWE-1021 &nbsp;|&nbsp; <b>Status:</b> Kelemahan Terverifikasi<br/><br/>"
        "<b>Dampak:</b> Akses langsung ke <code>http://10.110.1.9:1100</code> tidak menyertakan header pertahanan standar "
        "(HSTS, X-Frame-Options, X-Content-Type-Options, CSP). Kendati tidak teramati adanya form login berpassword pada sampel 2 KiB, "
        "ketiadaan proteksi pada socket internal membuka potensi risiko.<br/><br/>"
        "<b>Deskripsi Rinci:</b> Hasil audit membuktikan reverse proxy HTTPS menerapkan header keamanan dengan baik, namun akses langsung "
        "ke port 1100 hanya menghasilkan header cache. Asimetri ini menunjukkan proteksi hanya berada di lapisan luar reverse proxy.<br/><br/>"
        "<b>Rekomendasi Perbaikan:</b><br/>"
        "1. Batasi binding port 1100 hanya ke <code>127.0.0.1:1100</code> dan alihkan seluruh trafik via reverse proxy HTTPS.<br/>"
        "2. Pasang header keamanan standar langsung pada konfigurasi Express/Nginx backend bila akses langsung dibutuhkan.<br/>"
        "3. Terapkan pengalihan otomatis 301 ke HTTPS."
    )
    story.append(build_bilingual_table(en_f01, id_f01, styles))
    story.append(Spacer(1, 4))
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
    story.append(build_terminal_block(term_f01, styles))
    story.append(Spacer(1, 10))

    # F-02
    story.append(Paragraph("F-02: Backend Framework & Server Version Disclosure", styles['SectionH2']))
    en_f02 = (
        "<b>Risk Rating:</b> INFORMATIONAL &nbsp;|&nbsp; <b>CWE:</b> CWE-200 &nbsp;|&nbsp; <b>Status:</b> Verified Exposure<br/><br/>"
        "<b>Impact:</b> Responses from port 1100 reveal <code>X-Powered-By: Express</code> and <code>Server: nginx/1.22.1</code>. "
        "While not an exploitable vulnerability alone, it aids attackers in fingerprinting the stack.<br/><br/>"
        "<b>Remediation:</b> Declare <code>app.disable('x-powered-by')</code> in Express and set <code>server_tokens off;</code> in Nginx."
    )
    id_f02 = (
        "<b>Risk Rating:</b> INFORMATIONAL &nbsp;|&nbsp; <b>CWE:</b> CWE-200 &nbsp;|&nbsp; <b>Status:</b> Eksposur Terverifikasi<br/><br/>"
        "<b>Dampak:</b> Respons port 1100 mengekspos <code>X-Powered-By: Express</code> dan <code>Server: nginx/1.22.1</code>. "
        "Walaupun bukan celah langsung, informasi ini mempermudah pemetaan teknologi target oleh penyerang.<br/><br/>"
        "<b>Rekomendasi Perbaikan:</b> Tambahkan <code>app.disable('x-powered-by')</code> pada Express dan <code>server_tokens off;</code> pada Nginx."
    )
    story.append(build_bilingual_table(en_f02, id_f02, styles))
    story.append(Spacer(1, 10))

    # 6. OBSERVATIONS & 7. VERIFIED CONTROLS
    story.append(PageBreak())
    story.append(Paragraph("6. ADDITIONAL SECURITY OBSERVATIONS & TELEMETRY", styles['SectionH1']))
    en_obs = (
        "<b>O-01 (Port Scan Timeout):</b> Subtask 194 Nmap scan reached the 180-second terminal harness limit (exit 124) due to "
        "conservative -T2 timing over 2 hosts. In compliance with anti-loop rules, it was logged to <code>recon_errors.txt</code> without retry.<br/><br/>"
        "<b>O-02 (Local TLS Verify-21):</b> OpenSSL returned verify code 21 due to absent intermediate CA bundle on the tester workstation. "
        "The public Sectigo certificate is legitimately valid through January 2027."
    )
    id_obs = (
        "<b>O-01 (Batas Waktu Scan Port):</b> Subtask 194 Nmap mencapai batas waktu 180s (exit 124) akibat profil waktu -T2 pada 2 target. "
        "Sesuai protokol anti-loop, kejadian dicatat pada <code>recon_errors.txt</code> tanpa perulangan.<br/><br/>"
        "<b>O-02 (TLS Verify-21 Lokal):</b> OpenSSL menghasilkan verify code 21 akibat belum tersinkronisasinya intermediate CA pada workstation penguji. "
        "Sertifikat publik Sectigo terbukti valid dan resmi hingga Januari 2027."
    )
    story.append(build_bilingual_table(en_obs, id_obs, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("7. VERIFIED CONTROLS & NEGATIVE TEST RESULTS / KONTROL TERVERIFIKASI", styles['SectionH1']))
    ctrl_data = [
        [
            Paragraph("<b>Security Parameter & Verified Control (English)</b>", styles['TableHead']),
            Paragraph("<b>Hasil Verifikasi & Kontrol Keamanan (Bahasa Indonesia)</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>TLS 1.3 Cryptography:</b> Modern TLSv1.3 negotiated with cipher <code>TLS_AES_256_GCM_SHA384</code> and X25519 key exchange.", styles['TableCell']),
            Paragraph("<b>Kriptografi TLS 1.3:</b> TLSv1.3 modern ternegosiasi dengan cipher kuat <code>TLS_AES_256_GCM_SHA384</code> dan pertukaran kunci X25519.", styles['TableCell'])
        ],
        [
            Paragraph("<b>HSTS Enforcement:</b> Strict-Transport-Security header active on HTTPS with <code>max-age=86400</code>.", styles['TableCell']),
            Paragraph("<b>Penerapan HSTS:</b> Header Strict-Transport-Security aktif pada HTTPS dengan parameter durasi <code>max-age=86400</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Anti-Clickjacking Framing:</b> <code>X-Frame-Options: SAMEORIGIN</code> enforced on public HTTPS endpoint.", styles['TableCell']),
            Paragraph("<b>Kebijakan Anti-Clickjacking:</b> Header <code>X-Frame-Options: SAMEORIGIN</code> aktif pada HTTPS mencegah framing ilegal.", styles['TableCell'])
        ],
        [
            Paragraph("<b>MIME Sniffing Defense:</b> <code>X-Content-Type-Options: nosniff</code> enforced on HTTPS.", styles['TableCell']),
            Paragraph("<b>Proteksi MIME Sniffing:</b> Header <code>X-Content-Type-Options: nosniff</code> aktif pada HTTPS menolak sniffing tipe konten.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Infrastructure Masking:</b> DNS CNAME routes to <code>lkt-infra.first-resources.com</code> (10.100.2.64), isolating backend IP.", styles['TableCell']),
            Paragraph("<b>Masking Infrastruktur:</b> CNAME DNS mengarah ke <code>lkt-infra.first-resources.com</code> (10.100.2.64), menyamarkan IP backend langsung.", styles['TableCell'])
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

    # 8. LIMITATIONS & UNTESTED ITEMS
    story.append(Paragraph("8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN", styles['SectionH1']))
    en_lim = (
        "• <b>Linear Single-Pass Constraint:</b> Adhered to strict non-destructive parameters (max 1 probe per tool, no retries, no crawling).<br/>"
        "• <b>Network Service Gap:</b> Nmap timed out at 180s; open port and service version mapping across the host remains incomplete.<br/>"
        "• <b>Body Sampling Threshold:</b> Body capture was constrained to a 2 KiB sample size; hidden form inputs were not audited.<br/>"
        "• <b>Authentication Untested:</b> No login sessions, cookie flags, or CORS handling were evaluated.<br/>"
        "• <b>Advanced OWASP Categories:</b> Broken Access Control (A01), Injection (A03), and Components (A06) were not audited.<br/>"
        "• <b>Zero Destructive Impact:</b> No brute-forcing, SQL injection fuzzing, or DoS testing was conducted."
    )
    id_lim = (
        "• <b>Batasan Alur Linear 1 Putaran:</b> Pengujian mengikuti batasan non-destruktif ketat (maksimal 1 percobaan per alat, tanpa retry, tanpa crawling).<br/>"
        "• <b>Keterbatasan Scan Jaringan:</b> Nmap mengalami timeout pada 180 detik; pemetaan seluruh port dan versi layanan belum lengkap.<br/>"
        "• <b>Batas Sampel Body:</b> Sampel HTML dibatasi hingga 2 KiB; elemen form tersembunyi tidak diinspeksi.<br/>"
        "• <b>Autentikasi Belum Teruji:</b> Tidak ada sesi login, flag cookie, atau kebijakan CORS yang dievaluasi.<br/>"
        "• <b>Kategori OWASP Lanjutan:</b> Broken Access Control (A01), Injeksi (A03), dan Komponen Usang (A06) belum diaudit.<br/>"
        "• <b>Bebas Uji Destruktif:</b> Tidak dilakukan brute-force, fuzzing SQL, atau pengujian denial-of-service."
    )
    story.append(build_bilingual_table(en_lim, id_lim, styles))
    story.append(Spacer(1, 10))

    # 9. REMEDIATION ROADMAP & 10. CONCLUSION
    story.append(PageBreak())
    story.append(Paragraph("9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN", styles['SectionH1']))
    en_road = (
        "<b>1. Harden and Restrict Internal HTTP Port 1100</b> — Priority: <b>LOW / MEDIUM</b><br/>"
        "Rebind internal service on <code>10.110.1.9</code> to <code>127.0.0.1:1100</code> and enforce all access through the HTTPS reverse proxy.<br/><br/>"
        "<b>2. Suppress Technology Signatures</b> — Priority: <b>INFORMATIONAL</b><br/>"
        "Declare <code>app.disable('x-powered-by')</code> in Express and configure <code>server_tokens off;</code> in Nginx.<br/><br/>"
        "<b>3. Investigate Nmap Scan Timeout</b> — Priority: <b>INFORMATIONAL</b><br/>"
        "Analyze network rate limiting or drop rules causing the 180s Nmap timeout; conduct optimized -T4 scans.<br/><br/>"
        "<b>4. Synchronize CA Trust Stores & Phase-2 Audit</b> — Priority: <b>INFORMATIONAL</b><br/>"
        "Install intermediate CAs in local trust stores and schedule authenticated Phase-2 testing for OWASP logic."
    )
    id_road = (
        "<b>1. Hardening dan Isolasi Port 1100 HTTP Internal</b> — Prioritas: <b>LOW / MEDIUM</b><br/>"
        "Ubah binding layanan internal ke <code>127.0.0.1:1100</code> dan alihkan seluruh akses melalui reverse proxy HTTPS.<br/><br/>"
        "<b>2. Sembunyikan Informasi Framework</b> — Prioritas: <b>INFORMATIONAL</b><br/>"
        "Tambahkan <code>app.disable('x-powered-by')</code> pada Express dan <code>server_tokens off;</code> pada Nginx.<br/><br/>"
        "<b>3. Investigasi Timeout Scan Port Nmap</b> — Prioritas: <b>INFORMATIONAL</b><br/>"
        "Analisis latency atau filter firewall yang menyebabkan timeout 180s; lakukan pemindaian terarah dengan profil -T4.<br/><br/>"
        "<b>4. Sinkronisasi Trust Store CA & Asesmen Lanjutan</b> — Prioritas: <b>INFORMATIONAL</b><br/>"
        "Pasang intermediate CA pada workstation lokal dan jadwalkan pengujian terautentikasi untuk memeriksa logika OWASP."
    )
    story.append(build_bilingual_table(en_road, id_road, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("10. CONCLUSION / KESIMPULAN", styles['SectionH1']))
    en_conc = (
        "Within the executed linear single-pass scope, the <b>Dashboard Deadstock</b> application exhibits a robust external security posture "
        "on its primary HTTPS domain, featuring modern TLS 1.3 cryptography, active HSTS enforcement, and anti-clickjacking framing controls. "
        "No high or critical severity vulnerabilities were demonstrated within the unauthenticated test boundary.<br/><br/>"
        "Defensive optimizations should focus on hardening internal port 1100 to mirror edge policies, suppressing framework banners, "
        "and planning credentialed assessments for post-login workflows."
    )
    id_conc = (
        "Dalam batasan pengujian linear satu putaran yang dilakukan, aplikasi <b>Dashboard Deadstock</b> menunjukkan postur keamanan eksternal yang tangguh "
        "pada domain HTTPS utamanya, didukung enkripsi TLS 1.3 modern, penerapan HSTS aktif, serta kontrol anti-clickjacking yang baik. "
        "Tidak ditemukan kerentanan berisiko tinggi (High) maupun kritis (Critical) pada batasan pengujian tanpa autentikasi ini.<br/><br/>"
        "Optimasi difokuskan pada hardening port 1100 internal agar sejajar dengan kebijakan reverse proxy, penghapusan header framework, "
        "dan persiapan audit terautentikasi untuk alur kerja pasca-login."
    )
    story.append(build_bilingual_table(en_conc, id_conc, styles))
    story.append(Spacer(1, 15))

    # Sign-off Box
    sign_data = [
        [
            Paragraph("<b>Report Prepared By:</b><br/>Cyber Security Assessment Division<br/>Lentera Teknologi", styles['TableCell']),
            Paragraph("<b>Classification:</b><br/>CONFIDENTIAL — INTERNAL ONLY<br/>Zero Defect Assessment Standard", styles['TableCell']),
            Paragraph("<b>Document Verification:</b><br/>ECC Gate 1-5 Compliant<br/>Date: 19 Oktober 2026", styles['TableCell'])
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
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "/home/kristian.admin/.gemini/antigravity-cli/brain/18c205a4-661a-4e83-9dfb-8f26c11d7987/DEADSTOCK_DASHBOARD_FR_PENETRATION_TESTING_REPORT.pdf"
    generate_pdf(out_pdf)
