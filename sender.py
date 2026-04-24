import os
import smtplib
from email.message import EmailMessage

from utils import get_xlsx_filepath, email_title

# Configuration

# Get the secret from environment variables
EMAIL_FROM = os.environ.get('EMAIL_USERNAME')
EMAIL_TO = os.environ.get('EMAIL_DEV')
PASSWORD = os.environ.get('EMAIL_PASSWORD')
filename = "fidelity.xlsx"
FILE = get_xlsx_filepath(filename)
# Create Message
msg = EmailMessage()
msg['Subject'] = email_title("Fidelity")
msg['From'] = f"Amine Upwork <{EMAIL_FROM}>"
msg['To'] = EMAIL_TO
msg.set_content("Please see attached.")

# Attach File (Example: PDF)
with open(FILE, 'rb') as f:
    print(FILE)
    file_data = f.read()
    msg.add_attachment(file_data, maintype='application',
                       subtype='xlsx', filename=filename)

# Send via SMTP_SSL
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    if EMAIL_FROM and PASSWORD:
        smtp.login(EMAIL_FROM, PASSWORD)
        smtp.send_message(msg)
