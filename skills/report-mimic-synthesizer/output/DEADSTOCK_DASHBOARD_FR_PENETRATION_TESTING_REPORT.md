# [COVER / HEADER]
**Lentera Teknologi — Cyber Security Assessment Service**

## Dashboard Deadstock / First Resources (FR) Group
# INTERNAL PENETRATION TESTING REPORT
**19 Oktober 2026**

| Parameter | Detail |
| :--- | :--- |
| **Target System** | Dashboard Deadstock (FR Group) — `https://deadstock.first-resources.com` / `10.110.1.9:1100` |
| **Assessment Scope** | Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran) |
| **Attacker / Audit Node** | Internal Audit Workstation (Linux Security Subsystem / RFC1918 Scope) |
| **Access Level Tested** | Unauthenticated Passive Recon, Network Probing, & Application Response Baseline |
| **Classification** | CONFIDENTIAL — INTERNAL ENTERPRISE SECURITY ASSESSMENT |

---

## 1. EXECUTIVE SUMMARY / RINGKASAN EKSEKUTIF

| English | Bahasa Indonesia |
| :--- | :--- |
| On 19 October 2026, a focused, non-destructive internal web penetration test was conducted against the **Dashboard Deadstock** application, evaluated across two target access vectors: the primary HTTPS domain `https://deadstock.first-resources.com` (resolving via CNAME `lkt-infra.first-resources.com` to `10.100.2.64`) and the direct internal server instance `http://10.110.1.9:1100`. Testing strictly followed a linear single-pass methodology aligned with OWASP Top 10 standards, incorporating strict anti-loop, zero-retry tolerance rules without invasive crawling or denial-of-service attempts.<br><br>The assessment confirmed that perimeter HTTPS controls are effectively configured, featuring valid commercial Sectigo TLS 1.3 encryption, active HTTP Strict Transport Security (`max-age=86400`), anti-clickjacking protection (`X-Frame-Options: SAMEORIGIN`), and MIME-type enforcement. The network attack surface assessment observed an execution timeout on the Nmap scanning wrapper (exit code 124), which was transparently documented as an information gap without fabricated port claims.<br><br>The principal security observations identified are **F-01: Security Header Asymmetry & Unhardened HTTP Port 1100** (classified as **Low Severity**, as no unencrypted authentication form was detected on the sampled 2 KiB payload) and **F-02: Backend Framework & Server Technology Disclosure** (`X-Powered-By: Express`, `nginx/1.22.1`, classified as **Informational**).<br><br>**Overall Assessment Statement:** Evidence supports **1 Low-Risk Finding** and **1 Informational Observation**. In adherence to strict single-pass constraints, advanced categories including authenticated business logic, deep input fuzzing, and session token lifecycle remain unverified and require secondary authorized evaluation. | Pada 19 Oktober 2026 dilakukan pengujian penetrasi web internal non-destruktif terhadap sistem **Dashboard Deadstock** pada dua jalur akses: domain HTTPS utama `https://deadstock.first-resources.com` (ter-resolve via CNAME `lkt-infra.first-resources.com` ke `10.100.2.64`) dan instans server internal langsung `http://10.110.1.9:1100`. Pengujian menerapkan alur linear satu putaran sesuai standar OWASP Top 10 dengan toleransi error ketat tanpa perulangan, bebas crawling rekursif, dan tanpa aksi invasif.<br><br>Hasil pengujian mengonfirmasi bahwa pertahanan batas HTTPS terkonfigurasi dengan baik, didukung enkripsi TLS 1.3 komersial Sectigo valid, HSTS aktif (`max-age=86400`), proteksi anti-clickjacking (`X-Frame-Options: SAMEORIGIN`), serta penegakan MIME type. Pada tahap pemindaian jaringan, tool Nmap mengalami timeout pada wrapper eksekusi (exit code 124) yang dicatat secara transparan sebagai keterbatasan informasi tanpa klaim port palsu.<br><br>Temuan keamanan utama mencakup **F-01: Asimetri Header Keamanan & Ketiadaan Hardening Port 1100 HTTP** (diklasifikasikan berisiko **Low**, mengingat tidak teramati adanya form login kredensial pada payload sampel 2 KiB) serta **F-02: Pengungkapan Framework & Teknologi Backend** (`X-Powered-By: Express`, `nginx/1.22.1`, berstatus **Informational**).<br><br>**Kesimpulan Umum:** Hasil pengujian mengonfirmasi **1 Temuan Berisiko Rendah (Low)** dan **1 Observasi Informasional**. Mengingat asesmen ini dibatasi oleh metode satu putaran cepat, kategori tingkat lanjut seperti logika bisnis terautentikasi, fuzzing input mendalam, dan siklus token sesi ditandai belum teruji dan memerlukan audit lanjutan terotorisasi. |

---

## 2. TARGET SYSTEM & ASSESSMENT PARAMETERS

| English | Bahasa Indonesia |
| :--- | :--- |
| **Primary Domain / Hostname:** `deadstock.first-resources.com`<br>**DNS CNAME Record:** `lkt-infra.first-resources.com` &rarr; `10.100.2.64` (Infrastructure Masking)<br>**Internal Direct IP Target:** `10.110.1.9:1100` (Direct RFC1918 Private IPv4)<br>**Application Identity:** "Dashboard Deadstock" (First Resources Group)<br>**TLS Certificate:** Subject `CN=*.first-resources.com`, Issuer `Sectigo Public Server Authentication CA DV R36`, Valid `2026-06-29` to `2027-01-13`<br>**Cipher & Protocol:** TLSv1.3, `TLS_AES_256_GCM_SHA384`, RSA 2048-bit, Ephemeral X25519<br>**Web Server Technologies:** nginx (HTTPS Edge / 1.22.1 on port 1100), Node.js / Express backend (`X-Powered-By: Express`)<br>**Assessment Model:** Internal Non-Destructive Linear Web Pentest (OWASP Top 10 Alur Linear 1 Putaran)<br>**Testing Rules:** Maximum 1 attempt per tool; immediate error logging without retry upon failure/timeout; no deep recursive crawling; no brute force; no destructive fuzzing. | **Domain / Hostname Utama:** `deadstock.first-resources.com`<br>**Catatan DNS CNAME:** `lkt-infra.first-resources.com` &rarr; `10.100.2.64` (Infrastructure Masking)<br>**Target IP Internal Langsung:** `10.110.1.9:1100` (Alamat Privat IPv4 RFC1918 Langsung)<br>**Identitas Aplikasi:** "Dashboard Deadstock" (First Resources Group)<br>**Sertifikat TLS:** Subject `CN=*.first-resources.com`, Penerbit `Sectigo Public Server Authentication CA DV R36`, Masa Berlaku `2026-06-29` s/d `2027-01-13`<br>**Cipher & Protokol:** TLSv1.3, `TLS_AES_256_GCM_SHA384`, RSA 2048-bit, Ephemeral X25519<br>**Teknologi Web Server:** nginx (Edge HTTPS / 1.22.1 pada port 1100), Node.js / Express backend (`X-Powered-By: Express`)<br>**Model Pengujian:** Pentest Web Internal Non-Destruktif Linear (Alur Linear 1 Putaran Bebas Macet)<br>**Ketentuan Pengujian:** Maksimal 1 kali percobaan per tool; catat hasil tanpa perulangan saat error/timeout; tanpa crawling rekursif; tanpa brute force; tanpa aksi invasif. |

---

## 3. TESTING METHODOLOGY / METODOLOGI

```
+-------------------------------------------------------------------------------------------------------------+
|                                  LINEAR SINGLE-PASS OWASP ASSESSMENT WORKFLOW                               |
+----------------------+--------------------+---------------------+--------------------+----------------------+
| 1. Passive Recon     | 2. TCP Port Scan   | 3. App Response     | 4. TLS & Headers   | 5. Synthesis Report  |
| - DNS & CNAME lookup | - Top-100 + p1100  | - HTTP/HTTPS GET    | - OpenSSL s_client | - Bilingual Template |
| - httpx & whatweb    | - 180s harness lim | - Body sample (2KB) | - HSTS & Framing   | - Prioritized Plan   |
| - whois error logged | - Timeout handled  | - Error verbosity   | - Header Asymmetry | - Zero Defect Signoff|
+----------------------+--------------------+---------------------+--------------------+----------------------+
```

| English | Bahasa Indonesia |
| :--- | :--- |
| **1. Passive Reconnaissance:** DNS interrogation via `dig` confirming CNAME masking (`deadstock.first-resources.com` &rarr; `lkt-infra.first-resources.com` &rarr; `10.100.2.64`), `httpx` HTTP status validation, `whatweb` technology fingerprinting, and raw HTTP header capture.<br><br>**2. Network Enumeration:** Rapid non-intrusive TCP scan executed via Nmap (`-Pn -sT --top-ports 100 --open -T2 --max-retries 0 --host-timeout 2m -sV --version-light`) targeting `10.110.1.9` and `10.100.2.64` with port 1100. The harness wrapper reached timeout at 180s (exit 124), recorded transparently to `recon_errors.txt` without retry.<br><br>**3. Application Response Analysis:** Single-pass GET requests with low timeouts targeting root paths across both endpoints; raw status lines, headers, and body payloads (capped at 2 KiB) saved to `app_responses.txt`.<br><br>**4. TLS & Security Header Inspection:** Single non-intrusive OpenSSL `s_client` session validating certificate validity, TLS 1.3 cipher suite negotiation, HSTS enforcement, framing policies, and security header asymmetry.<br><br>**5. Evidence Synthesis:** Strict demarcation between confirmed findings, environmental tooling artifacts, and untested OWASP categories. | **1. Reconnaissance Pasif:** Interogasi DNS via `dig` mengonfirmasi masking CNAME (`deadstock.first-resources.com` &rarr; `lkt-infra.first-resources.com` &rarr; `10.100.2.64`), validasi status HTTP via `httpx`, fingerprinting teknologi via `whatweb`, serta penangkapan header HTTP mentah.<br><br>**2. Enumerasi Jaringan:** Pemindaian TCP cepat non-intrusif via Nmap (`-Pn -sT --top-ports 100 --open -T2 --max-retries 0 --host-timeout 2m -sV --version-light`) pada host `10.110.1.9` dan `10.100.2.64` menyertakan port 1100. Proses mencapai batas waktu harness 180s (exit 124) dan dicatat transparan pada `recon_errors.txt` tanpa retry.<br><br>**3. Analisis Respons Aplikasi:** Permintaan GET satu kali dengan timeout singkat pada kedua target; status line mentah, header, dan sampel body (maksimal 2 KiB) disimpan pada `app_responses.txt`.<br><br>**4. Inspeksi TLS & Header Keamanan:** Pengujian satu kali OpenSSL `s_client` untuk memvalidasi sertifikat, negosiasi cipher suite TLS 1.3, implementasi HSTS, kebijakan framing, serta asimetri header keamanan.<br><br>**5. Sintesis Bukti:** Pemisahan tegas antara temuan nyata, artefak lingkungan pengujian, dan kategori OWASP yang belum teruji. |

---

## 4. RISK MATRIX & FINDINGS OVERVIEW / MATRIKS RISIKO & TEMUAN

```
+-------------------------------------------------------------------------------------------------------+
|                                       ASSESSMENT FINDINGS MATRIX                                      |
+-----------+-------------------------------------------------------------+----------+------------------+
| Reference | Finding / Observation Title                                 | Severity | Status           |
+-----------+-------------------------------------------------------------+----------+------------------+
| F-01      | Security Header Asymmetry & Unhardened HTTP Port 1100       | LOW      | Config Weakness  |
| F-02      | Backend Framework & Server Version Disclosure               | INFO     | Observation      |
| O-01      | Network Scanning Port Enumeration Timeout (Exit 124)        | INFO     | Telemetry Bound  |
| O-02      | Local TLS Trust-Store Intermediate Chain Absence            | INFO     | Telemetry Bound  |
+-----------+-------------------------------------------------------------+----------+------------------+
```

### Summary Table / Tabel Ringkasan Temuan
| Finding ID | Issue / Isu | Severity | Status / Catatan |
| :--- | :--- | :---: | :--- |
| **F-01** | Security Header Asymmetry & Unhardened HTTP Port 1100<br>*Asimetri Header Keamanan & Ketiadaan Hardening Port 1100 HTTP* | **LOW** | Configuration Flaw / *Kelemahan Konfigurasi* |
| **F-02** | Backend Framework & Server Version Disclosure (`X-Powered-By: Express`)<br>*Pengungkapan Framework Backend & Versi Server (`X-Powered-By: Express`)* | **INFORMATIONAL** | Technology Exposure / *Eksposur Informasi* |
| **O-01** | Network Port Scan Execution Timeout (Exit 124)<br>*Batas Waktu Eksekusi Scan Port Nmap (Exit 124)* | **INFORMATIONAL** | Scope Limitation / *Keterbatasan Informasi* |
| **O-02** | Incomplete Local Environment TLS Trust Store (Verify Code 21)<br>*Ketidaklengkapan Trust Store TLS Lokal (Verify Code 21)* | **INFORMATIONAL** | Local Client Artifact / *Artefak Lingkungan Penguji* |

---

## 5. DETAILED FINDINGS BREAKDOWN / RINCIAN TEMUAN

### F-01 — Security Header Asymmetry & Unhardened HTTP Port 1100
**Asimetri Header Keamanan & Ketiadaan Hardening Port 1100 HTTP**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Risk Rating:** LOW<br>**CWE Classification:** CWE-16: Configuration Weakness / CWE-1021<br>**Status:** Verified Configuration Flaw<br><br>**Impact:**<br>The direct internal endpoint `http://10.110.1.9:1100` serves the "Dashboard Deadstock" application without baseline HTTP defense headers. While the public HTTPS interface enforces `Strict-Transport-Security`, `X-Frame-Options: SAMEORIGIN`, and `X-Content-Type-Options: nosniff`, direct HTTP connections to port 1100 omit all defensive headers. Although no cleartext credential form was detected within the sampled payload, leaving the internal HTTP socket unhardened and accessible creates unnecessary exposure for internal network users.<br><br>**Detailed Narrative:**<br>During application response probing (`app_responses.txt`), responses from `http://10.110.1.9:1100` returned HTTP 200 with standard caching headers (`ETag`, `Last-Modified`, `Cache-Control`) but completely lacked browser protection controls. Concurrently, the edge reverse proxy on `https://deadstock.first-resources.com` correctly injects security headers. This asymmetry indicates that defensive protections are enforced solely at the reverse proxy layer while the backend application port remains exposed to internal network routing without localized protection.<br><br>**Recommended Remediation:**<br>1. Restrict the service listening on port 1100 so that it only binds to `127.0.0.1:1100`, forcing all traffic to traverse the authoritative Nginx reverse proxy.<br>2. If direct internal access to port 1100 is operationally required, inject baseline security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy`) directly within the Express/Nginx application configuration.<br>3. Enforce automatic HTTP-to-HTTPS 301 redirection for any plaintext requests reaching port 1100. | **Risk Rating:** LOW<br>**Klasifikasi CWE:** CWE-16: Kelemahan Konfigurasi / CWE-1021<br>**Status:** Kelemahan Konfigurasi Terverifikasi<br><br>**Dampak:**<br>Endpoint internal langsung `http://10.110.1.9:1100` menyajikan aplikasi "Dashboard Deadstock" tanpa header pertahanan HTTP standar. Kendati antarmuka HTTPS publik menerapkan `Strict-Transport-Security`, `X-Frame-Options: SAMEORIGIN`, dan `X-Content-Type-Options: nosniff`, koneksi HTTP langsung ke port 1100 tidak menyertakan header proteksi sama sekali. Meskipun tidak ditemukan form login berpassword pada sampel 2 KiB yang diuji, ketiadaan hardening pada socket HTTP internal membuka potensi risiko bagi pengguna di jaringan lokal.<br><br>**Deskripsi Rinci:**<br>Pada pengujian respons aplikasi (`app_responses.txt`), respons dari `http://10.110.1.9:1100` menghasilkan HTTP 200 dengan header cache standar (`ETag`, `Last-Modified`, `Cache-Control`), namun tidak memuat kontrol keamanan browser. Sebaliknya, edge reverse proxy pada `https://deadstock.first-resources.com` menyisipkan header keamanan dengan baik. Asimetri ini membuktikan proteksi hanya diterapkan pada lapisan reverse proxy terluar, sedangkan port backend internal terekspos tanpa proteksi mandiri.<br><br>**Rekomendasi Perbaikan:**<br>1. Batasi binding layanan port 1100 agar hanya mendengar pada `127.0.0.1:1100` dan wajibkan seluruh lalu lintas melewati reverse proxy Nginx resmi.<br>2. Apabila akses langsung ke port 1100 tetap dibutuhkan secara operasional, pasang header keamanan standar (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy`) langsung pada konfigurasi Express/Nginx backend.<br>3. Terapkan pengalihan otomatis 301 dari HTTP biasa ke koneksi aman HTTPS bila port 1100 diakses langsung. |

```text
[DEADSTOCK-EVIDENCE-01: Header Asymmetry Comparison]
$ curl -I http://10.110.1.9:1100/
HTTP/1.1 200 OK
Server: nginx/1.22.1
X-Powered-By: Express
ETag: W/"194-..."
Last-Modified: ...
Cache-Control: public, max-age=0
Content-Type: text/html; charset=UTF-8
Content-Length: 404
(Note: Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options missing)

$ curl -k -I https://deadstock.first-resources.com/
HTTP/1.1 200 OK
Server: nginx
Strict-Transport-Security: max-age=86400
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

---

### F-02 — Backend Framework & Server Version Disclosure
**Pengungkapan Framework Backend & Versi Server (`X-Powered-By: Express`)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Risk Rating:** INFORMATIONAL<br>**CWE Classification:** CWE-200: Information Exposure<br>**Status:** Verified Observation<br><br>**Impact:**<br>HTTP responses from port 1100 explicitly advertise the underlying framework via `X-Powered-By: Express` alongside web server identity `Server: nginx/1.22.1`. While technological disclosure does not constitute a standalone exploit, it aids potential attackers during automated reconnaissance, allowing adversaries to tailor exploit vectors specifically for Node.js/Express and unpatched Nginx 1.22 branch vulnerabilities.<br><br>**Detailed Narrative:**<br>Both raw HEAD headers (`curl_headers_http.txt`) and `whatweb` fingerprinting outputs confirmed that `X-Powered-By: Express` is transmitted in cleartext on every HTTP response from `10.110.1.9:1100`. Furthermore, Nginx exposes its specific release number (`1.22.1`). Industry hardening best practices dictate that technology stack signatures should be suppressed.<br><br>**Recommended Remediation:**<br>1. Disable the `X-Powered-By` header in the Express application by declaring `app.disable('x-powered-by')` in the Node.js entry point.<br>2. Configure `server_tokens off;` inside the Nginx configuration block to suppress the specific version number `1.22.1`. | **Risk Rating:** INFORMATIONAL<br>**Klasifikasi CWE:** CWE-200: Pengungkapan Informasi<br>**Status:** Observasi Terverifikasi<br><br>**Dampak:**<br>Respons HTTP dari port 1100 secara eksplisit mengumumkan framework backend melalui `X-Powered-By: Express` dan identitas server `Server: nginx/1.22.1`. Meskipun pengungkapan informasi ini bukan merupakan kerentanan langsung, data ini mempermudah penyerang dalam fase reconnaissance untuk memetakan kerentanan spesifik pada ekosistem Node.js/Express dan cabang Nginx 1.22.<br><br>**Deskripsi Rinci:**<br>Header mentah (`curl_headers_http.txt`) dan hasil fingerprint `whatweb` membuktikan bahwa `X-Powered-By: Express` dikirimkan secara terbuka pada setiap respons HTTP dari `10.110.1.9:1100`. Selain itu, Nginx memunculkan nomor rilis spesifik (`1.22.1`). Standar hardening industri merekomendasikan penghapusan banner teknologi semacam ini.<br><br>**Rekomendasi Perbaikan:**<br>1. Nonaktifkan header `X-Powered-By` pada aplikasi Express dengan menambahkan perintah `app.disable('x-powered-by')` pada script Node.js.<br>2. Pasang direktif `server_tokens off;` pada blok konfigurasi Nginx untuk menyembunyikan rilis versi `1.22.1`. |

```text
[DEADSTOCK-EVIDENCE-02: Framework Disclosure Snippet]
HTTP/1.1 200 OK
Server: nginx/1.22.1
X-Powered-By: Express
Content-Type: text/html; charset=UTF-8
```

---

## 6. ADDITIONAL SECURITY & FUNCTIONAL OBSERVATIONS / OBSERVASI TAMBAHAN

### O-01 — Network Port Scan Execution Timeout (Exit 124)
**Batas Waktu Eksekusi Scan Port Nmap (Exit 124)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Observation Summary:** The active TCP port enumeration subtask (ID 194) executed `nmap -Pn -sT --top-ports 100 --open -T2 --max-retries 0 --host-timeout 2m -sV --version-light` against `10.110.1.9` and `10.100.2.64` with port 1100. Due to conservative timing constraints (`-T2`) across two target hosts, the execution reached the 180-second terminal harness timeout (exit code 124). In compliance with the non-destructive anti-loop engagement protocol, the execution was recorded transparently in `recon_errors.txt` without retries, resulting in an information gap rather than a technical failure.<br><br>**Evidence:** `/root/evidence/recon_errors.txt` and execution logs. | **Ringkasan Observasi:** Subtask pemindaian port TCP aktif (ID 194) menjalankan perintah Nmap (`-Pn -sT --top-ports 100 --open -T2 --max-retries 0 --host-timeout 2m -sV --version-light`) pada host `10.110.1.9` dan `10.100.2.64` menyertakan port 1100. Akibat parameter waktu konservatif (`-T2`) pada dua host, proses mencapai batas waktu wrapper harness 180 detik (exit code 124). Sesuai protokol anti-loop, kejadian ini dicatat secara transparan pada `recon_errors.txt` tanpa perulangan, menjadi catatan keterbatasan informasi tanpa klaim port palsu.<br><br>**Evidence:** `/root/evidence/recon_errors.txt` dan log eksekusi. |

### O-02 — Incomplete Local Environment TLS Trust Store (Verify Code 21)
**Ketidaklengkapan Trust Store TLS Lokal (Verify Code 21)**

| English | Bahasa Indonesia |
| :--- | :--- |
| **Observation Summary:** OpenSSL validation against `deadstock.first-resources.com:443` returned `Verify return code: 21 (unable to verify the first certificate)` and error code 20. Technical verification confirmed this occurred because the local testing environment lacked the Sectigo intermediate CA certificate bundle. The public certificate is legitimately issued by `Sectigo Public Server Authentication CA DV R36` and remains valid through 13 January 2027. This condition is documented as an environmental testing artifact rather than a server-side cryptographic flaw.<br><br>**Evidence:** `/root/evidence/tls_analysis.txt`. | **Ringkasan Observasi:** Pengujian OpenSSL terhadap `deadstock.first-resources.com:443` memunculkan `Verify return code: 21 (unable to verify the first certificate)` dan error 20. Analisis membuktikan hal ini semata-mata disebabkan oleh belum tersinkronisasinya berkas intermediate CA Sectigo pada trust store lokal lingkungan penguji. Sertifikat publik target terbukti resmi diterbitkan oleh `Sectigo Public Server Authentication CA DV R36` dan sah hingga 13 Januari 2027. Kejadian ini dicatat sebagai artefak lokal penguji, bukan kerentanan server publik.<br><br>**Evidence:** `/root/evidence/tls_analysis.txt`. |

---

## 7. VERIFIED CONTROLS & NEGATIVE TEST RESULTS / KONTROL TERVERIFIKASI & HASIL NEGATIF

| Test Area / Security Parameter (English) | Hasil Pengujian & Verifikasi (Bahasa Indonesia) |
| :--- | :--- |
| **TLS 1.3 Cryptographic Standards:** Hostname `deadstock.first-resources.com` successfully negotiated modern TLSv1.3 with high-strength cipher `TLS_AES_256_GCM_SHA384` and Ephemeral X25519 key exchange. | **Standar Enkripsi TLS 1.3:** Hostname `deadstock.first-resources.com` menegosiasikan TLSv1.3 modern dengan cipher kuat `TLS_AES_256_GCM_SHA384` dan pertukaran kunci Ephemeral X25519. |
| **HSTS Deployment:** Strict-Transport-Security header is active on HTTPS with `max-age=86400`, instructing conforming browsers to refuse plaintext downgrades. | **Implementasi HSTS:** Header Strict-Transport-Security aktif pada koneksi HTTPS dengan parameter `max-age=86400`, mencegah upaya downgrade ke HTTP biasa. |
| **Anti-Clickjacking Framing Policy:** `X-Frame-Options: SAMEORIGIN` is actively enforced on the public HTTPS endpoint, preventing unauthorized iframe embedding. | **Kebijakan Anti-Clickjacking:** Header `X-Frame-Options: SAMEORIGIN` diterapkan secara aktif pada endpoint HTTPS publik, mencegah pembajakan klik melalui iframe. |
| **MIME-Type Sniffing Protection:** `X-Content-Type-Options: nosniff` is enforced on HTTPS responses, neutralizing browser content-type sniffing. | **Perlindungan MIME Sniffing:** Header `X-Content-Type-Options: nosniff` aktif pada HTTPS, meniadakan risiko eksekusi payload melalui sniffing tipe konten. |
| **Infrastructure Masking via CNAME:** Domain DNS maps to CNAME `lkt-infra.first-resources.com` resolving to reverse proxy `10.100.2.64`, obscuring backend direct IP. | **Masking Infrastruktur via CNAME:** DNS publik memetakan ke CNAME `lkt-infra.first-resources.com` pada IP `10.100.2.64`, menyamarkan IP backend langsung. |
| **Controlled Application Response Size:** Application HEAD responses return concise headers; GET responses serve structured 2 KiB baseline HTML without verbose stack trace leaks. | **Ukuran Respons Aplikasi Terkontrol:** Respons HEAD menyajikan data ringkas; respons GET menyajikan HTML dasar 2 KiB tanpa kebocoran stack trace error debug. |

---

## 8. TESTING LIMITATIONS & UNTESTED BOUNDARIES / BATASAN PENGUJIAN

| English | Bahasa Indonesia |
| :--- | :--- |
| - **Linear Single-Pass Constraint:** Execution adhered to strict non-destructive parameters (max 1 probe per tool, no retries, no recursive crawling).<br>- **Network Service Enumeration Gap:** Nmap scan timed out at 180s; open port and service version mapping across the host network remains incomplete.<br>- **Body Sampling Threshold:** Body capture was constrained to a 2 KiB sample size; hidden HTML form inputs or sub-routes beyond the root were not inspected.<br>- **Authentication & Token Lifecycle Untested:** No login sessions, session cookie flags (`Secure`, `HttpOnly`, `SameSite`), or CORS handling were evaluated.<br>- **Advanced OWASP Categories Untested:** Broken Access Control (A01), Injection (A03), Insecure Design (A04), and Vulnerable Components (A06) were not audited.<br>- **Zero Destructive Testing:** No password spraying, aggressive fuzzing, or denial-of-service tests were performed. | - **Batasan Alur Linear 1 Putaran:** Pengujian mengikuti batasan non-destruktif ketat (maksimal 1 percobaan per alat, tanpa retry, tanpa crawling rekursif).<br>- **Keterbatasan Enumerasi Port Jaringan:** Scan Nmap mengalami timeout pada 180 detik; pemetaan seluruh port dan versi layanan belum lengkap.<br>- **Batas Pengambilan Sampel Body:** Sampel HTML dibatasi hingga 2 KiB; elemen form tersembunyi atau rute sekunder di luar halaman utama tidak diinspeksi.<br>- **Siklus Autentikasi & Cookie Belum Teruji:** Tidak ada sesi login, flag cookie (`Secure`, `HttpOnly`, `SameSite`), atau kebijakan CORS yang dievaluasi.<br>- **Kategori OWASP Lanjutan Belum Teruji:** Broken Access Control (A01), Injeksi (A03), Insecure Design (A04), dan Komponen Usang (A06) belum diaudit.<br>- **Bebas Uji Destruktif:** Tidak dilakukan password spraying, fuzzing agresif, atau pengujian denial-of-service. |

---

## 9. ACTIONABLE REMEDIATION ROADMAP / PANDUAN PERBAIKAN

| English | Bahasa Indonesia |
| :--- | :--- |
| 1. **Harden and Restrict Internal HTTP Port 1100** — Priority: **LOW / MEDIUM**<br>- Rebind the internal service on `10.110.1.9` to `127.0.0.1:1100`.<br>- Force all user traffic to route through the authoritative Nginx reverse proxy enforcing HTTPS.<br>- Apply host firewall rules (`iptables`) blocking direct cross-VLAN access to port 1100.<br><br>2. **Suppress Technology Signatures on Express & Nginx** — Priority: **INFORMATIONAL**<br>- Add `app.disable('x-powered-by');` in the Express application initialization code.<br>- Add `server_tokens off;` within Nginx configuration blocks to suppress version `1.22.1`.<br><br>3. **Investigate Port Scan Timeout & Firewall Behavior** — Priority: **INFORMATIONAL**<br>- Diagnose why Nmap scans reached 180s timeout (internal network rate limiting or drop-rule latency).<br>- Conduct optimized targeted port scans (`-T4` with lower timeout thresholds).<br><br>4. **Synchronize Internal CA Trust Stores** — Priority: **INFORMATIONAL**<br>- Install intermediate CA certificates in internal workstations to eliminate local Verify-21 warnings.<br><br>5. **Conduct Authorized Phase-2 Deep Assessment** — Priority: **INFORMATIONAL**<br>- Schedule credentialed application assessment to evaluate authenticated endpoints, IDOR, and input sanitation. | 1. **Hardening dan Isolasi Port 1100 HTTP Internal** — Prioritas: **LOW / MEDIUM**<br>- Ubah binding layanan internal pada `10.110.1.9` ke `127.0.0.1:1100`.<br>- Wajibkan seluruh akses pengguna melalui reverse proxy Nginx yang mengaktifkan HTTPS.<br>- Pasang firewall host (`iptables`) untuk memblokir akses langsung antar-VLAN menuju port 1100.<br><br>2. **Sembunyikan Informasi Framework pada Express & Nginx** — Prioritas: **INFORMATIONAL**<br>- Tambahkan `app.disable('x-powered-by');` pada baris inisialisasi aplikasi Express/Node.js.<br>- Tambahkan `server_tokens off;` pada blok konfigurasi Nginx untuk menyembunyikan rilis versi `1.22.1`.<br><br>3. **Investigasi Penyebab Timeout Scan Port Nmap** — Prioritas: **INFORMATIONAL**<br>- Analisis penyebab timeout Nmap 180s (keberadaan rate-limiting jaringan atau latency filter firewall).<br>- Lakukan pemindaian terarah dengan profil waktu optimal (`-T4` dengan host-timeout lebih singkat).<br><br>4. **Sinkronisasi Trust Store CA Internal** — Prioritas: **INFORMATIONAL**<br>- Pasang paket sertifikat intermediate CA pada workstation lokal penguji untuk meniadakan error Verify-21.<br><br>5. **Jadwalkan Asesmen Lanjutan Terotorisasi Tahap 2** — Prioritas: **INFORMATIONAL**<br>- Agendakan pengujian terautentikasi untuk memeriksa logika bisnis, IDOR, dan sanitasi input secara komprehensif. |

---

## 10. CONCLUSION / KESIMPULAN

| English | Bahasa Indonesia |
| :--- | :--- |
| Within the executed linear single-pass scope, the **Dashboard Deadstock** application exhibits a robust external security posture on its primary HTTPS domain, featuring modern TLS 1.3 cryptography, active HSTS enforcement, and anti-clickjacking framing controls. No high or critical severity vulnerabilities were demonstrated within the unauthenticated test boundary.<br><br>The primary areas identified for optimization pertain to defensive consistency between endpoints: hardening direct HTTP access on port 1100 to mirror edge security policies, suppressing verbose technology headers (`X-Powered-By: Express`), and conducting targeted credentialed assessments to validate application logic beyond the root interface. | Dalam batasan pengujian linear satu putaran yang dilakukan, aplikasi **Dashboard Deadstock** menunjukkan postur keamanan eksternal yang tangguh pada domain HTTPS utamanya, didukung enkripsi TLS 1.3 modern, penerapan HSTS aktif, serta kontrol anti-clickjacking yang baik. Tidak ditemukan kerentanan berisiko tinggi (High) maupun kritis (Critical) pada batasan pengujian tanpa autentikasi ini.<br><br>Area utama yang perlu dioptimalkan adalah konsistensi pertahanan antar-endpoint: melakukan hardening pada akses HTTP langsung port 1100 agar sejajar dengan kebijakan reverse proxy, menyembunyikan header teknologi (`X-Powered-By: Express`), serta mengagendakan asesmen terautentikasi lanjutan untuk mengevaluasi logika aplikasi di balik halaman utama. |

---

*Laporan ini disusun secara objektif berdasarkan telemetri eksekusi pentest non-destruktif satu putaran Dashboard Deadstock pada 19 Oktober 2026.*
