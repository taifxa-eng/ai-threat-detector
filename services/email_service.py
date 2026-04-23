import smtplib
from email.mime.text import MIMEText
from config.settings import settings


def send_login_alert(username: str, success: bool):
    status = "SUCCESS ✅" if success else "FAILED ❌"

    subject = "AI Threat Detector - Login Alert"

    body = f"""
    Login Attempt Detected:

    Username: {username}
    Status: {status}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.ADMIN_EMAIL
    msg["To"] = settings.ADMIN_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()

        server.login(settings.ADMIN_EMAIL, "lglu krcx qahi jqdp")

        server.send_message(msg)