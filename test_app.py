from flask import Flask
import subprocess
import smtplib
from email.mime.text import MIMEText
import pytest
import sys

# =====================================================
# 1️⃣  FLASK APPLICATION
# =====================================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask CI/CD Pipeline!"

@app.route("/about")
def about():
    return "About Page"

@app.route("/api/status")
def status():
    return "ok"

# =====================================================
# 2️⃣  PYTEST TEST CASES (IN SAME FILE)
# =====================================================

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello from Flask CI/CD Pipeline!" in response.data

def test_about():
    client = app.test_client()
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About Page" in response.data

def test_api_status():
    client = app.test_client()
    response = client.get("/api/status")
    assert response.status_code == 200
    assert b"ok" in response.data

# =====================================================
# 3️⃣  EMAIL SETTINGS
# =====================================================

YOUR_EMAIL = "gokuleo2002@gmail.com"
APP_PASSWORD = "euku ktct aifm cdhd "    # Gmail App Password
TO_EMAIL = "gokulnathravikumar8888@gmail.com"

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "❌ Test Failed - Flask CI/CD Pipeline"
    msg["From"] = YOUR_EMAIL
    msg["To"] = TO_EMAIL

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("📧 Email sent!")
    except Exception as e:
        print("Email sending error:", e)

# =====================================================
# 4️⃣  RUN TESTS + EMAIL IF FAIL
# =====================================================

def run_tests():
    print("\n⚙️  Running Test Cases...\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", __file__],
        capture_output=True, text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("❌ Tests FAILED! Sending email...")
        send_email(result.stdout + "\n" + result.stderr)
    else:
        print("✔ All tests PASSED!")
        send_email("all tests passed successfully!")

# =====================================================
# 5️⃣  MAIN ENTRY POINT
# =====================================================

if __name__ == "__main__":
    run_tests()
