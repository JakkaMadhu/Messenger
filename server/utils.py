import re
import socket
import resend
from config import RESEND_API_KEY

# Configure the Resend SDK key
resend.api_key = RESEND_API_KEY

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
    Sends OTP email using the Resend SDK.
    """
    if not RESEND_API_KEY:
        print("[WARNING] RESEND_API_KEY is missing in environment.")
        return False
        
    body_content = body_template.format(otp=otp)
    print(f"Attempting to send email via Resend SDK to {to_email}...")
    try:
        # Send transactional email using the official Resend Python SDK
        r = resend.Emails.send({
            "from": "Messenger <onboarding@resend.dev>",
            "to": to_email,
            "subject": subject,
            "html": f"<p>{body_content}</p>"
        })
        print(f"Resend email sent successfully: {r}")
        return True
    except Exception as e:
        print(f"Failed to send email via Resend to {to_email}: {e}")
        return False
