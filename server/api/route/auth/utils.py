import re
import dns.resolver
from dns.exception import DNSException


EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def is_email_valid(email):
    # Check if the email matches the regex pattern
    if not EMAIL_REGEX.match(email):
        return False
    
    # Extract domain from email
    domain = email.split('@')[1]
    
    try:
        # Perform DNS query to check MX records
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False
    except dns.exception.DNSException:
        return False

def is_password_valid(password):
    # Check if password length is at least 8 characters
    if len(password) < 8:
        return True
    # Check if password has at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return True
    # Check if password has at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return True
    # Check if password has at least one digit
    if not re.search(r"[0-9]", password):
        return True
    # Check if password has at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return True
    # If all conditions are met, the password is valid
    return False

def is_phone_valid(phone):
    if len(phone) < 10 or len(phone) > 15:
        return False
    if not phone.isdigit():
        return False
    return True

    