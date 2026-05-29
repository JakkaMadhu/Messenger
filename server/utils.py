import re
import socket
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_NAME, EMAIL_PASSWORD

def validate_email(email):
    """
    Validates email format using regex and performs a DNS lookup check.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format."
    
    domain = email.split('@')[-1]
    try:
        socket.gethostbyname(domain)
        return True, "Valid"
    except Exception:
        return False, "Email domain does not exist (fake email)."

def send_otp_email(to_email, otp, subject, body_template):
    """
    Generic SMTP email sender. Consolidates both password reset and registration
    OTP sending logic to eliminate duplicate SMTP setup code.
    """
    if not EMAIL_NAME or not EMAIL_PASSWORD:
        print("[WARNING] SMTP credentials missing in environment.")
        return False
        
    try:
        body_content = body_template.format(otp=otp)
        message = MIMEText(body_content)
        message['Subject'] = subject
        message['From'] = EMAIL_NAME
        message['To'] = to_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_NAME, EMAIL_PASSWORD)
            smtp.send_message(message)
        return True
    except Exception as e:
        print(f"Failed to send SMTP email to {to_email}: {e}")
        return False
