# [COVER / HEADER]
**Lentera Teknologi — Cyber Security Assessment Service**

## BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate
# INTERNAL PENETRATION TESTING REPORT
**18 Oktober 2026**

| Parameter | Detail |
| :--- | :--- |
| **Target System** | Rekapitulasi Budget FR - Estate (BIMS) — `https://rekapbudget-estate.first-resources.com` / `10.110.1.9:1627` |
| **Assessment Scope** | Internal Non-Destructive Web Application Assessment (OWASP Top 10 Linear Single-Pass) |
| **Attacker / Tester Node** | `10.100.2.64` / Internal Audit Terminal (Linux Security Workstation) |
| **Access Levels** | Unauthenticated Access & Dummy Credential Auth Probing |
| **Classification** | CONFIDENTIAL — INTERNAL SECURITY ASSESSMENT |

---

## 1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF

| English | Bahasa Indonesia |
| :--- | :--- |
| On 18 October 2026, a focused, non-destructive internal web application penetration test was conducted against **BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate**, evaluated across two target endpoints: the public-facing hostname `https://rekapbudget-estate.first-resources.com` (resolving via CNAME to `10.100.2.64`) and the direct internal server instance `http://10.110.1.9:1627`. Testing strictly followed a linear single-pass methodology aligned with OWASP Top 10 web security standards, incorporating passive reconnaissance, targeted TCP port enumeration, and non-intrusive HTTP/TLS/transport analysis without deep crawling or recursive fuzzing.<br><br>The principal high-risk finding identified is **F-01: Plaintext HTTP Transport on Internal Login Endpoint (Port 1627)**. Server `10.110.1.9:1627` operates an unencrypted HTTP/1.0 service (`Server: RBFR`) exposing an active login interface (`POST /masuk`). Any administrative or staff credentials transmitted across this channel are subject to eavesdropping, sniffing, and man-in-the-middle (MitM) interception within the internal RFC1918 network.<br><br>Additional configuration weaknesses include **F-02: Permissive Content Security Policy with `unsafe-inline`** and **F-03: Redundant & Conflicting Security Headers** resulting from proxy/application layering (`X-Frame-Options` and `Referrer-Policy` duplicates). Conversely, verified positive security controls were confirmed on the HTTPS hostname, including valid wildcard TLS certificates (Sectigo CA), standard HTTP-to-HTTPS 301 redirection, strict HSTS implementation, and accurate HTTP 401 rejections against unauthorized authentication attempts.<br><br>**Overall Assessment Statement:** The evidence supports **1 High-Severity Finding** and **2 Configuration Weaknesses / Indications**. Because this engagement operated under a strict single-pass, non-destructive scope with iteration cut-offs, elements such as post-login cookie flags (`Secure`/`HttpOnly`), reflected XSS validation, and internal IDOR/business logic remain unverified and require secondary authorized testing. | Pada 18 Oktober 2026 dilakukan pengujian penetrasi web non-destruktif terfokus terhadap sistem **BIMS (Budget Information Management System) / Rekapitulasi Budget FR - Estate** pada dua jalur akses: hostname `https://rekapbudget-estate.first-resources.com` (ter-resolve via CNAME ke `10.100.2.64`) dan instans server internal langsung `http://10.110.1.9:1627`. Pengujian menerapkan alur linear satu putaran sesuai standar OWASP Top 10, mencakup pengintaian pasif, pemindaian port TCP terarah, dan analisis transport HTTP/TLS tanpa crawling rekursif maupun brute force.<br><br>Temuan utama berisiko tinggi yang terverifikasi adalah **F-01: Transport Plaintext HTTP pada Endpoint Login Internal (Port 1627)**. Host `10.110.1.9:1627` menjalankan layanan HTTP/1.0 tanpa enkripsi (`Server: RBFR`) yang melayani form login (`POST /masuk`). Kredensial dan data sesi yang dikirimkan melalui endpoint ini berisiko disadap atau dimanipulasi melalui traffic sniffing pada segmen jaringan internal RFC1918.<br><br>Observasi konfigurasi tambahan mencakup **F-02: Kebijakan CSP Permisif (`unsafe-inline`)** dan **F-03: Duplikasi Header Keamanan yang Berkonflik** akibat layering reverse proxy/aplikasi (duplikasi `X-Frame-Options` dan `Referrer-Policy`). Sebaliknya, kontrol keamanan positif terkonfirmasi pada hostname HTTPS mencakup sertifikat TLS wildcard valid (Sectigo CA), pengalihan 301 HTTP-ke-HTTPS, penegakan HSTS, serta penolakan HTTP 401 yang valid terhadap upaya login dummy.<br><br>**Kesimpulan Umum:** Hasil pengujian mengonfirmasi **1 Temuan Berisiko High** dan **2 Kelemahan Konfigurasi/Indikasi**. Mengingat asesmen ini dibatasi oleh metode satu putaran bebas macet dengan limit iterasi, item lanjutan seperti atribut flag cookie (`Secure`/`HttpOnly`), uji tuntas reflected XSS, serta IDOR/logika bisnis terautentikasi ditandai sebagai 'belum teruji' dan direkomendasikan untuk uji lanjutan terotorisasi. |

---

## 2. TARGET SYSTEM & ASSESSMENT PARAMETERS

| English | Bahasa Indonesia |
| :--- | :--- |
| **Primary Domain / Hostname:** `rekapbudget-estate.first-resources.com`<br>**DNS CNAME Record:** `lkt-infra.first-resources.com` &rarr; `10.100.2.64`<br>**Internal Direct IP Target:** `10.110.1.9:1627` (No PTR/DNS, RFC1918 Private IPv4)<br>**Application Identity:** BIMS (Budget Information Management System) — "Rekapitulasi Budget FR - Estate" (FR Group)<br>**TLS Certificate:** Subject `CN=*.first-resources.com`, Issuer `Sectigo Public Server Authentication CA DV R36`, Valid `2026-06-29` to `2027-01-13`<br>**Web Server Technologies:** nginx (Reverse Proxy / HTTPS), RBFR Custom Service (Port 1627 HTTP/1.0)<br>**Assessment Model:** Internal Non-Destructive Linear Web Pentest (One-Pass Anti-Loop Execution)<br>**Testing Rules:** Maximum 1 attempt per tool/technique; immediate progression upon error/timeout without retry; no deep crawling; no password spraying / brute force; no UDP flood. | **Domain / Hostname Utama:** `rekapbudget-estate.first-resources.com`<br>**Catatan DNS CNAME:** `lkt-infra.first-resources.com` &rarr; `10.100.2.64`<br>**Target IP Internal Langsung:** `10.110.1.9:1627` (Tanpa PTR/DNS, Alamat Privat IPv4 RFC1918)<br>**Identitas Aplikasi:** BIMS (Budget Information Management System) — "Rekapitulasi Budget FR - Estate" (FR Group)<br>**Sertifikat TLS:** Subject `CN=*.first-resources.com`, Penerbit `Sectigo Public Server Authentication CA DV R36`, Masa Berlaku `2026-06-29` s/d `2027-01-13`<br>**Teknologi Web Server:** nginx (Reverse Proxy / HTTPS), RBFR Custom Service (Port 1627 HTTP/1.0)<br>**Model Pengujian:** Pentest Web Internal Non-Destruktif Linear (Eksekusi 1 Putaran Bebas Macet)<br>**Ketentuan Pengujian:** Maksimal 1 kali percobaan per tool; catat hasil saat error/timeout tanpa perulangan; tanpa crawling mendalam; tanpa brute force; tanpa UDP flood. |

---

## 3. TESTING METHODOLOGY / METODOLOGI

```
+-------------------------------------------------------------------------------------------------------------+
|                                  LINEAR SINGLE-PASS OWASP ASSESSMENT WORKFLOW                               |
+----------------------+--------------------+---------------------+--------------------+----------------------+
| 1. Passive Recon     | 2. TCP Port Scan   | 3. OWASP Web Audit  | 4. Evidence Matrix | 5. Synthesis Report  |
| - DNS & CNAME lookup | - Top-1000 + p1627 | - Login (/masuk)    | - Verified Findings| - Bilingual Template |
| - TLS & Cert checks  | - Service banner   | - CSP & Sec Headers | - Config Anomalies | - Prioritized Plan   |
| - HTTP Status/Redir  | - 10.110.1.9 check | - Plaintext Risk    | - Untested Bounds  | - Zero Defect Signoff|
+----------------------+--------------------+---------------------+--------------------+----------------------+
```

| English | Bahasa Indonesia |
| :--- | :--- |
| **Reconnaissance:** DNS mapping (`rekapbudget-estate.first-resources.com` &rarr; `lkt-infra.first-resources.com` &rarr; `10.100.2.64`), HTTPS/HTTP redirection verification, TLS handshake validation, inspection of robots/security metadata, and web stack identification.<br><br>**Network Enumeration:** Non-intrusive TCP scan against host `10.110.1.9` targeting top-1000 common ports plus service port `1627` using Nmap version and safe script detection (`-sT -sV -sC -T4`).<br><br>**Web Application Assessment (OWASP Top 10):** Evaluation of `/masuk` login mechanism, session transport encryption across both targets, dummy authentication probing for rate-limiting signals, inspection of security headers (`CSP`, `HSTS`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`), and identification of duplicate policy layering.<br><br>**Evidence Handling:** Rigorous segregation between confirmed exploitable risks, unverified configuration indications, and out-of-scope/untested items to eliminate false positives. | **Reconnaissance:** Pemetaan DNS (`rekapbudget-estate.first-resources.com` &rarr; `lkt-infra.first-resources.com` &rarr; `10.100.2.64`), verifikasi redirect HTTPS/HTTP, validasi handshake TLS, pemeriksaan metadata robots/security, serta identifikasi tech-stack.<br><br>**Enumerasi Jaringan:** Pemindaian TCP non-intrusif pada host `10.110.1.9` mencakup 1000 port umum dan port layanan `1627` menggunakan Nmap versi dan skrip aman (`-sT -sV -sC -T4`).<br><br>**Asesmen Aplikasi Web (OWASP Top 10):** Evaluasi form login `/masuk`, enkripsi transport sesi pada kedua target, pengujian kredensial dummy untuk mendeteksi sinyal rate-limiting, inspeksi header keamanan (`CSP`, `HSTS`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`), dan pemetaan konfigurasi proxy berlapis.<br><br>**Penanganan Evidence:** Pemisahan tegas antara risiko terverifikasi, indikasi konfigurasi yang belum terbukti dieksploitasi, dan batasan cakupan yang tidak teruji untuk mencegah false positive. |

---

## 4. RISK MATRIX & FINDINGS OVERVIEW / MATRIKS RISIKO & TEMUAN

```
+-------------------------------------------------------------------------------------------------------+
|                                       ASSESSMENT FINDINGS MATRIX                                      |
+-----------+-------------------------------------------------------------+----------+------------------+
| Reference | Finding / Observation Title                                 | Severity | Status           |
+-----------+-------------------------------------------------------------+----------+------------------+
| F-01      | Unencrypted Plaintext HTTP Login Service on Port 1627       | HIGH     | Verified Finding |
| F-02      | Permissive Content Security Policy (unsafe-inline Allowed)  | MEDIUM   | Config Weakness  |
| F-03      | Redundant & Conflicting Security Headers from Proxy Layer   | LOW      | Config Weakness  |
| O-01      | Server Banner & Custom Application Identity Disclosure      | INFO     | Observation      |
| O-02      | Metadata Endpoints Redirection & Validation Anomalies       | INFO     | Observation      |
+-----------+-------------------------------------------------------------+----------+------------------+
```

### Summary Table / Tabel Ringkasan Temuan
| Finding ID | Issue / Isu | Severity | Status / Catatan |
| :--- | :--- | :---: | :--- |
| **F-01** | Unencrypted Plaintext HTTP Transport on Internal Login Endpoint<br>*Transport HTTP Plaintext Tanpa Enkripsi pada Endpoint Login Internal* | **HIGH** | Verified Risk / *Terverifikasi Nyata* |
| **F-02** | Permissive Content Security Policy with `unsafe-inline` Directives<br>*Kebijakan CSP Permisif Mengizinkan Direktif unsafe-inline* | **MEDIUM** | Configuration Weakness / *Kelemahan Konfigurasi* |
| **F-03** | Redundant and Conflicting Security Headers via Reverse Proxy Layering<br>*Duplikasi dan Konflik Header Keamanan Akibat Layering Proxy* | **LOW** | Configuration Inconsistency / *Inkonsistensi Konfigurasi* |
| **O-01** | Server Banner Disclosure (`nginx`, `Server: RBFR`)<br>*Pengungkapan Banner Layanan Server (`nginx`, `Server: RBFR`)* | **INFORMATIONAL** | Operational Hygiene / *Higiene Operasional* |
| **O-02** | Metadata Path Redirect & TLS Validation Errors (curl 60 / curl 35)<br>*Anomali Redirect Metadata & Error Validasi TLS (curl 60 / curl 35)* | **INFORMATIONAL** | Network Telemetry / *Telemetri Jaringan* |

---

## 5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN

### F-01 — Unencrypted Plaintext HTTP Login Service on Port 1627
**Transport HTTP Plaintext Tanpa Enkripsi pada Endpoint Login Internal (10.110.1.9:1627)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Risk Rating:** HIGH<br>**CWE Classification:** CWE-319: Cleartext Transmission of Sensitive Information<br>**Status:** Confirmed / Verified Finding<br><br>**Impact:**<br>The service hosted on internal IP `10.110.1.9:1627` provides an unencrypted HTTP/1.0 interface serving the identical BIMS ("Rekapitulasi Budget FR - Estate") login form (`POST /masuk`). Because traffic transmitted to this socket lacks Transport Layer Security (TLS/SSL), any employee or administrative credentials (usernames, passwords) and authenticated session cookies transmitted across this channel can be captured via passive ARP/network sniffing, compromised switch ports, or lateral man-in-the-middle positioning within the corporate internal network.<br><br>**Detailed Narrative:**<br>Network scanning via `nmap -sT -sV -sC -T4 --top-ports 1000 -p1627 10.110.1.9` identified that TCP port `1627` is open, presenting `Server: RBFR`. Attempting to connect via HTTPS resulted in `curl: (35) error:0A00010B:SSL routines::wrong version number`, confirming that port 1627 is strictly an unencrypted HTTP service. When queried with HTTP/1.0, the server returns an HTTP 200 response with a 3,995-byte HTML payload containing an active HTML form (`<form method="post" action="/masuk">`) featuring `username` and `password` input fields. An authentication probe with dummy credentials produced an immediate `HTTP 401 Unauthorized`, validating that the endpoint is an active authentication gateway.<br><br>**Recommended Remediation:**<br>1. Immediately bind the internal BIMS service to listen only on `localhost` (`127.0.0.1:1627`) and route all traffic exclusively through an authoritative reverse proxy (e.g., Nginx) enforcing HTTPS/TLS 1.3.<br>2. Block direct external and cross-VLAN network access to port 1627 via host-level firewalls (`iptables`/`nftables`) and perimeter ACLs.<br>3. If direct HTTP access on port 1627 is required for legacy operational reasons, enforce an automatic HTTP `301 Moved Permanently` redirect to `https://rekapbudget-estate.first-resources.com/masuk`.<br>4. Issue mandatory credential and session token rotation for all internal users who may have previously logged in through this plaintext IP endpoint. | **Risk Rating:** HIGH<br>**Klasifikasi CWE:** CWE-319: Pengiriman Informasi Sensitif Tanpa Enkripsi<br>**Status:** Terverifikasi / Temuan Nyata<br><br>**Dampak:**<br>Layanan pada IP internal `10.110.1.9:1627` menyediakan antarmuka HTTP/1.0 tanpa enkripsi yang menyajikan form login aplikasi BIMS ("Rekapitulasi Budget FR - Estate") yang identik (`POST /masuk`). Karena lalu lintas ke port ini tidak dilindungi TLS/SSL, seluruh kredensial akun pengguna/administrator (username, password) dan cookie sesi yang dikirimkan dapat disadap melalui sniffing jaringan internal, port mirroring, atau serangan Man-in-the-Middle (MitM) di jaringan privat.<br><br>**Deskripsi Rinci:**<br>Pemindaian jaringan melalui `nmap -sT -sV -sC -T4 --top-ports 1000 -p1627 10.110.1.9` mengidentifikasi port TCP `1627` terbuka dengan banner `Server: RBFR`. Upaya inisiasi koneksi HTTPS menghasilkan `curl: (35) error:0A00010B:SSL routines::wrong version number`, membuktikan bahwa port 1627 murni beroperasi pada HTTP plaintext. Permintaan GET menghasilkan response HTTP 200 dengan payload 3.995 byte yang memuat form login aktif (`<form method="post" action="/masuk">`) dengan input field `username` dan `password`. Uji kirim kredensial dummy menghasilkan respons `HTTP 401 Unauthorized`, mengonfirmasi bahwa endpoint ini memproses autentikasi secara aktif.<br><br>**Rekomendasi Perbaikan:**<br>1. Segera batasi binding layanan BIMS internal agar hanya mendengar pada `127.0.0.1:1627` dan wajibkan seluruh akses melalui reverse proxy Nginx yang mengaktifkan TLS 1.3.<br>2. Terapkan aturan firewall (`iptables`/`nftables`) pada host dan network ACL untuk memblokir akses langsung antar-VLAN menuju port 1627.<br>3. Jika akses port 1627 tetap dibutuhkan sementara waktu, pasang aturan pengalihan otomatis HTTP `301 Moved Permanently` menuju URL HTTPS resmi.<br>4. Lakukan rotasi kredensial dan sesi bagi seluruh personil internal yang terindikasi pernah melakukan autentikasi melalui port plaintext tersebut. |

```text
[BIMS-EVIDENCE-01: Port Scan & Plaintext Transport Verification]
$ nmap -sT -sV -sC -T4 --top-ports 1000 -p1627 10.110.1.9
Starting Nmap 7.98 ( https://nmap.org )
Nmap scan report for 10.110.1.9
Host is up (0.0027s latency).
PORT     STATE SERVICE VERSION
1627/tcp open  http    RBFR custom HTTP server (HTTP/1.0)
|_http-server-header: RBFR
|_http-title: Rekapitulasi Budget FR - Estate

$ curl -i http://10.110.1.9:1627/masuk
HTTP/1.0 200 OK
Server: RBFR
Content-Type: text/html; charset=utf-8
Content-Length: 3995
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

<form method="post" action="/masuk">
  <input type="text" name="username" placeholder="Nama Pengguna" required />
  <input type="password" name="password" placeholder="Kata Sandi" required />
  <button type="submit">Masuk</button>
</form>

$ curl -k https://10.110.1.9:1627/masuk
curl: (35) error:0A00010B:SSL routines::wrong version number (HTTP-only endpoint)
```

---

### F-02 — Permissive Content Security Policy (`unsafe-inline`)
**Kebijakan Content Security Policy (CSP) Permisif Mengizinkan `unsafe-inline`**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Risk Rating:** MEDIUM<br>**CWE Classification:** CWE-1021 / CWE-79 Defense-in-Depth<br>**Status:** Configuration Weakness Verified (Exploitation Inconclusive)<br><br>**Impact:**<br>The Content Security Policy enforced on both the HTTPS domain and the internal IP contains `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'`. This setting significantly weakens the browser's defense-in-depth boundary against Cross-Site Scripting (XSS). In the event that an attacker discovers an unsanitized reflection or stored input field within the application, the CSP policy will fail to prevent the execution of inline JavaScript payloads.<br><br>**Detailed Narrative:**<br>Inspection of HTTP response headers on `https://rekapbudget-estate.first-resources.com` revealed the following CSP configuration:<br>`default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; ...`<br>While the baseline policy restricts origins, the inclusion of `'unsafe-inline'` completely negates the primary anti-injection benefit of Content Security Policy. Probe requests targeting input reflection were initiated but remained incomplete due to single-pass execution iteration limits. Thus, this issue is formally classified as a confirmed configuration flaw rather than a demonstrated XSS exploit.<br><br>**Recommended Remediation:**<br>1. Eliminate `'unsafe-inline'` from the `script-src` and `style-src` directives.<br>2. Implement cryptographically random, per-request cryptographic nonces (e.g., `'nonce-{random}'`) or SHA-256 hashes for all legitimate inline scripts and styles.<br>3. Conduct a comprehensive, authorized authenticated source-code and reflection audit to verify that all user inputs are contextually encoded prior to rendering. | **Risk Rating:** MEDIUM<br>**Klasifikasi CWE:** CWE-1021 / CWE-79 Defense-in-Depth<br>**Status:** Kelemahan Konfigurasi Terverifikasi (Eksploitasi Belum Terbukti)<br><br>**Dampak:**<br>Header Content Security Policy yang dikirimkan oleh domain HTTPS maupun IP internal memuat direktif `script-src 'unsafe-inline'` dan `style-src 'unsafe-inline'`. Konfigurasi ini melemahkan lapisan pertahanan mendalam browser terhadap serangan Cross-Site Scripting (XSS). Jika di masa depan ditemukan titik injeksi input yang tidak tersanitasi, kebijakan CSP ini tidak akan dapat mencegah eksekusi skrip berbahaya.<br><br>**Deskripsi Rinci:**<br>Pemeriksaan header HTTP pada `https://rekapbudget-estate.first-resources.com` memperlihatkan parameter CSP:<br>`default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; ...`<br>Kendati direktif awal membatasi sumber eksternal, kehadiran nilai `'unsafe-inline'` meniadakan proteksi utama CSP terhadap injeksi skrip. Pengujian input reflection sempat dijadwalkan namun tidak tuntas akibat batasan iterasi satu putaran, sehingga isu ini secara objektif dikategorikan sebagai kelemahan konfigurasi, bukan eksploitasi terbukti.<br><br>**Rekomendasi Perbaikan:**<br>1. Hapus nilai `'unsafe-inline'` dari direktif `script-src` dan `style-src`.<br>2. Terapkan mekanisme cryptographic nonce berbasis request (`'nonce-{random}'`) atau hash SHA-256 untuk skrip/style inline yang sah.<br>3. Lakukan pengujian terotorisasi lanjutan terhadap seluruh parameter input untuk memastikan implementasi context-aware encoding. |

```text
[BIMS-EVIDENCE-02: Content-Security-Policy Header Inspection]
Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; 
                         img-src 'self' data:; font-src 'self'; connect-src 'self'; 
                         frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

---

### F-03 — Redundant & Conflicting Security Headers from Proxy Layering
**Duplikasi dan Konflik Header Keamanan Akibat Layering Proxy**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Risk Rating:** LOW<br>**CWE Classification:** CWE-16: Configuration Vulnerability<br>**Status:** Configuration Inconsistency Confirmed<br><br>**Impact:**<br>Responses from the primary HTTPS hostname deliver duplicated and contradictory security headers, notably `X-Frame-Options: DENY` accompanied by `X-Frame-Options: SAMEORIGIN`. When receiving conflicting headers, different web browsers resolve precedence in divergent ways: some enforce the most restrictive directive (`DENY`), while others ignore duplicate headers entirely or fall back to legacy behavior. This inconsistency undermines clickjacking and isolation protections.<br><br>**Detailed Narrative:**<br>Header inspection on `https://rekapbudget-estate.first-resources.com` identified duplicated emissions across multiple security policies:<br>- `X-Frame-Options`: delivered as both `DENY` and `SAMEORIGIN`<br>- `Referrer-Policy`: delivered as both `no-referrer` and `strict-origin-when-cross-origin`<br>- `Permissions-Policy`: duplicated with reordered directives<br>- `X-Content-Type-Options: nosniff`: emitted twice<br>This artifact typically occurs in enterprise environments where an edge reverse proxy (Nginx) injects global security headers while the upstream backend application framework also injects its own default header set.<br><br>**Recommended Remediation:**<br>1. Designate a single authoritative layer responsible for security header injection (recommended: the edge Nginx reverse proxy).<br>2. Suppress header emission from the backend application runtime, or configure Nginx with `proxy_hide_header` to strip duplicate headers before sending responses downstream. | **Risk Rating:** LOW<br>**Klasifikasi CWE:** CWE-16: Kerentanan Konfigurasi<br>**Status:** Inkonsistensi Konfigurasi Terverifikasi<br><br>**Dampak:**<br>Respons dari hostname HTTPS utama memuat header keamanan yang terduplikasi dengan nilai yang saling bertentangan, seperti `X-Frame-Options: DENY` dan `X-Frame-Options: SAMEORIGIN` secara bersamaan. Ketika browser menerima nilai duplikat yang bertolak belakang, interpretasi browser dapat berbeda: sebagian menerapkan aturan terketat (`DENY`), sementara browser lain dapat mengabaikan header sepenuhnya sehingga membatalkan perlindungan clickjacking.<br><br>**Deskripsi Rinci:**<br>Pemeriksaan header pada `https://rekapbudget-estate.first-resources.com` memperlihatkan anomali duplikasi header:<br>- `X-Frame-Options`: muncul ganda dengan nilai `DENY` dan `SAMEORIGIN`<br>- `Referrer-Policy`: muncul ganda (`no-referrer` dan `strict-origin-when-cross-origin`)<br>- `Permissions-Policy`: duplikat dengan urutan direktif yang berbeda<br>- `X-Content-Type-Options: nosniff`: disisipkan sebanyak dua kali<br>Pola ini menunjukkan adanya layering arsitektur di mana reverse proxy Nginx menyisipkan security header secara global, sementara aplikasi backend juga menyisipkan header standarnya sendiri.<br><br>**Rekomendasi Perbaikan:**<br>1. Tetapkan satu titik kontrol otoritatif tunggal untuk penyuntikan security header (disarankan pada edge reverse proxy Nginx).<br>2. Nonaktifkan pembuatan header duplikat pada aplikasi backend, atau gunakan direktif `proxy_hide_header` pada Nginx untuk menghapus header dari backend sebelum diteruskan ke browser pengguna. |

```text
[BIMS-EVIDENCE-03: Duplicate Header Dump from HTTPS Response]
HTTP/2 200 OK
server: nginx
date: Sun, 18 Oct 2026 16:15:20 GMT
content-type: text/html; charset=utf-8
strict-transport-security: max-age=15552000; includeSubDomains
x-content-type-options: nosniff
x-content-type-options: nosniff
x-frame-options: DENY
x-frame-options: SAMEORIGIN
referrer-policy: no-referrer
referrer-policy: strict-origin-when-cross-origin
permissions-policy: camera=(), microphone=(), geolocation=()
permissions-policy: geolocation=(), camera=(), microphone=()
```

---

## 6. ADDITIONAL SECURITY & FUNCTIONAL OBSERVATIONS / OBSERVASI TAMBAHAN

### O-01 — Web Server Banner & Identity Disclosure
**Pengungkapan Banner Layanan Server (`nginx`, `Server: RBFR`)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Observation Summary:** The public HTTPS endpoint discloses `Server: nginx` while internal port 1627 discloses `Server: RBFR`. Although neither response exposes specific software patch or minor build numbers, disclosing backend service identities facilitates targeted reconnaissance and fingerprinting.<br><br>**Evidence:** Verified in HTTP headers via `curl -I` against both endpoints. | **Ringkasan Observasi:** Endpoint HTTPS publik mengekspos banner `Server: nginx` sedangkan port 1627 internal mengekspos `Server: RBFR`. Walaupun tidak memunculkan nomor patch atau build minor, pengungkapan identitas server memudahkan penyerang melakukan pemetaan teknologi spesifik.<br><br>**Evidence:** Terkonfirmasi pada header HTTP via `curl -I` pada kedua endpoint. |

### O-02 — Metadata Path Redirect & TLS Validation Anomalies
**Anomali Redirect Metadata & Error Validasi TLS (curl 60 / curl 35)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Observation Summary:** Inquiries to standard metadata paths (`/robots.txt` and `/.well-known/security.txt`) on the HTTPS domain returned an initial strict validation error (`curl: (60) SSL certificate problem: unable to get local issuer certificate`) due to the absence of the intermediate CA bundle in the testing environment's local trust store. On the plaintext port 1627, both paths triggered an unauthenticated `HTTP 303 See Other` redirect pointing to `/masuk`. HTTPS connection attempts to port 1627 produced `curl: (35) wrong version number`, confirming that the port lacks SSL/TLS capabilities entirely.<br><br>**Evidence:** `/work/recon_results/` and execution telemetries. | **Ringkasan Observasi:** Pemeriksaan path metadata standar (`/robots.txt` dan `/.well-known/security.txt`) pada domain HTTPS memunculkan error validasi lokal (`curl: (60) unable to get local issuer certificate`) akibat belum tersinkronisasinya intermediate CA pada trust store lokal penguji. Pada port 1627 plaintext, kedua path tersebut merespons dengan `HTTP 303 See Other` yang dialihkan ke `/masuk`. Upaya negosiasi HTTPS ke port 1627 menghasilkan error `curl: (35) wrong version number` yang membuktikan port tersebut murni non-TLS.<br><br>**Evidence:** `/work/recon_results/` dan telemetri eksekusi. |

---

## 7. VERIFIED CONTROLS & NEGATIVE TEST RESULTS / KONTROL TERVERIFIKASI & HASIL NEGATIF

| Test Area / Security Parameter (English) | Hasil Pengujian & Verifikasi (Bahasa Indonesia) |
| :--- | :--- |
| **Host Network Attack Surface (10.110.1.9):** Nmap scan across top-1000 ports plus port 1627 confirmed that only TCP/1627 is open. No secondary management ports (SSH, RDP, Telnet, Database) are exposed. | **Permukaan Serangan Jaringan (10.110.1.9):** Scan Nmap top-1000 port ditambah port 1627 membuktikan hanya port TCP/1627 yang terbuka. Tidak ditemukan port manajemen (SSH, RDP, Database) yang terekspos. |
| **HTTP to HTTPS Redirection:** The root HTTP endpoint for `rekapbudget-estate.first-resources.com` correctly enforces a `301 Moved Permanently` redirect to secure HTTPS. | **Pengalihan HTTP ke HTTPS:** Hostname utama secara benar menerapkan pengalihan `301 Moved Permanently` dari HTTP biasa ke koneksi aman HTTPS. |
| **HSTS Enforcement:** Strict-Transport-Security header is active on HTTPS with `max-age=15552000` (180 days) and `includeSubDomains`. | **Penegakan HSTS:** Header HSTS aktif pada HTTPS dengan parameter `max-age=15552000` (180 hari) dan mencakup seluruh subdomain. |
| **TLS Certificate Legitimacy:** Valid Sectigo wildcard certificate (`*.first-resources.com`) in place, active from June 2026 through January 2027. | **Validitas Sertifikat TLS:** Menggunakan sertifikat resmi Sectigo wildcard (`*.first-resources.com`) dengan masa berlaku aktif s/d Januari 2027. |
| **Authentication Defense Baseline:** Probing the `/masuk` login form with dummy credentials (`ratecheck_marker`) resulted in an immediate `HTTP 401 Unauthorized`, rejecting invalid logins. | **Pertahanan Autentikasi Dasar:** Uji coba kredensial dummy pada form `/masuk` menghasilkan respons `HTTP 401 Unauthorized`, menolak autentikasi ilegal. |
| **HTTP Method Restriction:** Probing HTTP `OPTIONS` on port 1627 resulted in `405 Method Not Allowed`, indicating basic method filtering. | **Restriksi Metode HTTP:** Request HTTP `OPTIONS` pada port 1627 menghasilkan `405 Method Not Allowed`, mengindikasikan filter metode HTTP aktif. |

---

## 8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN

| English | Bahasa Indonesia |
| :--- | :--- |
| - **Linear Single-Pass Execution:** Testing was executed under strict non-destructive constraints (max 1 probe per tool/technique, immediate advance upon error, no recursive crawling).<br>- **Session Cookie Flags Unverified:** Initial `GET /masuk` responses did not set session cookies. Because authentication was not completed, cookie flags (`Secure`, `HttpOnly`, `SameSite`) could not be evaluated.<br>- **Input Reflection Inconclusive:** Parameter reflection and XSS probes against login parameters were stopped prior to completion due to subtask iteration cut-offs.<br>- **Rate Limiting Inconclusive:** A single dummy login request yielded HTTP 401 without a `429 Too Many Requests` or `Retry-After` header. Whether progressive throttling or IP lockouts exist requires multi-request authorized testing.<br>- **No Destructive Testing:** No brute-force attacks, fuzzing payloads, production data alterations, or denial-of-service tests were carried out.<br>- **Important Assurance Separation:** Untested categories must not be assumed to be inherently secure. | - **Pengujian Linear Satu Putaran:** Asesmen berjalan dengan pembatasan non-destruktif ketat (maksimal 1 percobaan per alat, catat hasil tanpa retry, tanpa crawling rekursif).<br>- **Atribut Cookie Sesi Belum Teruji:** Respons `GET /masuk` awal tidak menyertakan `Set-Cookie`. Karena autentikasi tidak dituntaskan, atribut flag cookie (`Secure`, `HttpOnly`, `SameSite`) belum dapat dinilai.<br>- **Uji Injeksi Input Belum Tuntas:** Probe parameter reflection dan XSS terhenti oleh batas iterasi sistem sehingga tidak ada payload eksploitatif yang dievaluasi.<br>- **Rate Limiting Belum Konklusif:** Satu percobaan login dummy menghasilkan HTTP 401 tanpa header `429` atau `Retry-After`. Keberadaan proteksi anti-brute force memerlukan uji multi-request terotorisasi.<br>- **Bebas Tindakan Destruktif:** Tidak dilakukan password spraying, database fuzzing, penghapusan data produksi, atau pengujian denial-of-service.<br>- **Prinsip Evaluasi:** Kategori yang belum diuji tidak boleh diasumsikan telah aman secara otomatis. |

---

## 9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN

| English | Bahasa Indonesia |
| :--- | :--- |
| 1. **Decommission or Isolate Plaintext HTTP on Port 1627** — Priority: **HIGH**<br>- Rebind the internal BIMS service on `10.110.1.9` to `127.0.0.1:1627`.<br>- Force all traffic to traverse the HTTPS reverse proxy at `https://rekapbudget-estate.first-resources.com`.<br>- Apply host firewall rules (`iptables`) blocking direct cross-VLAN inbound traffic to port 1627.<br>- Conduct credential rotations for accounts utilized across internal subnet tests.<br><br>2. **Normalize Security Headers at the Edge Reverse Proxy** — Priority: **MEDIUM**<br>- Consolidate all security header definitions inside Nginx configuration blocks.<br>- Remove duplicate directives; retain a single authoritative `X-Frame-Options: DENY` and `Referrer-Policy: strict-origin-when-cross-origin`.<br>- Configure `proxy_hide_header` to strip duplicate headers emitted by upstream application servers.<br><br>3. **Harden Content Security Policy (CSP)** — Priority: **MEDIUM**<br>- Remove `'unsafe-inline'` from both `script-src` and `style-src`.<br>- Migrate inline scripts and styling to cryptographic nonces (`'nonce-...'`) or deterministic hash values.<br><br>4. **Enforce Strict Session Cookie Flags Post-Authentication** — Priority: **LOW / MEDIUM**<br>- Ensure all session tokens issued upon successful POST `/masuk` explicitly enforce `Secure; HttpOnly; SameSite=Lax` (or `Strict`).<br><br>5. **Conduct Authorized Phase-2 Deep Validation** — Priority: **INFORMATIONAL**<br>- Schedule a credentialed secondary assessment to evaluate rate limiting, IDOR, input sanitation, and backend component version patching. | 1. **Tutup atau Isolasi Layanan HTTP Plaintext Port 1627** — Prioritas: **HIGH**<br>- Ubah binding layanan BIMS pada `10.110.1.9` ke `127.0.0.1:1627`.<br>- Alihkan seluruh jalur login agar wajib melalui reverse proxy HTTPS di `https://rekapbudget-estate.first-resources.com`.<br>- Pasang firewall host (`iptables`) untuk memblokir akses langsung antar-VLAN menuju port 1627.<br>- Lakukan rotasi kata sandi untuk akun internal yang pernah digunakan pada subnet tersebut.<br><br>2. **Normalisasi Header Keamanan pada Reverse Proxy Otoritatif** — Prioritas: **MEDIUM**<br>- Satukan seluruh konfigurasi security header di dalam blok Nginx.<br>- Hapus duplikasi header; pertahankan nilai tunggal seperti `X-Frame-Options: DENY` dan `Referrer-Policy: strict-origin-when-cross-origin`.<br>- Tambahkan direktif `proxy_hide_header` pada Nginx untuk meniadakan header duplikat dari backend.<br><br>3. **Perketat Content Security Policy (CSP)** — Prioritas: **MEDIUM**<br>- Hapus nilai `'unsafe-inline'` pada `script-src` dan `style-src`.<br>- Migrasikan skrip inline ke mekanisme nonce (`'nonce-...'`) atau hash SHA-256.<br><br>4. **Terapkan Flag Cookie Sesi yang Ketat Pasca-Login** — Prioritas: **LOW / MEDIUM**<br>- Pastikan seluruh session token yang diterbitkan setelah `POST /masuk` memuat atribut `Secure; HttpOnly; SameSite=Lax` (atau `Strict`).<br><br>5. **Jadwalkan Asesmen Lanjutan Terotorisasi Tahap 2** — Prioritas: **INFORMATIONAL**<br>- Lakukan pengujian terautentikasi untuk menguji ketahanan rate-limiting, IDOR, sanitasi input, dan inventarisasi patch versi komponen backend. |

---

## 10. CONCLUSION / KESIMPULAN

| English | Bahasa Indonesia |
| :--- | :--- |
| Within the executed linear single-pass scope, the **BIMS / Rekapitulasi Budget FR - Estate** application demonstrates solid foundational perimeter defenses on its public HTTPS interface, including modern HSTS enforcement and valid commercial TLS certification. However, the exposure of an unencrypted HTTP/1.0 login interface directly on internal IP `10.110.1.9:1627` introduces a critical transport vulnerability (**F-01: High**) that bypasses transport security and leaves corporate authentication credentials vulnerable to internal network interception.<br><br>Immediate remediation must prioritize closing or proxying port 1627 behind HTTPS, followed by normalizing security headers and hardening the Content Security Policy. Addressing these action items will elevate the security posture of the BIMS estate application to enterprise production standards. | Dalam cakupan pengujian linear satu putaran yang dilakukan, sistem **BIMS / Rekapitulasi Budget FR - Estate** menunjukkan pertahanan batas (perimeter) yang baik pada interface HTTPS publiknya, termasuk penerapan HSTS dan sertifikat TLS komersial yang valid. Namun, tersedianya interface login HTTP/1.0 tanpa enkripsi pada alamat IP internal `10.110.1.9:1627` menimbulkan risiko transport signifikan (**F-01: High**) yang mengabaikan proteksi enkripsi dan membuka celah penyadapan kredensial di jaringan internal.<br><br>Langkah remediasi prioritas utama adalah menutup atau mengarahkan port 1627 ke jalur HTTPS, disusul dengan normalisasi header keamanan ganda serta pengetatan Content Security Policy. Penerapan langkah-langkah ini akan meningkatkan postur keamanan aplikasi BIMS sesuai standar produksi enterprise. |

---

*Laporan ini disusun secara objektif berdasarkan telemetri eksekusi pentest non-destruktif satu putaran BIMS FR Estate pada 18 Oktober 2026.*
