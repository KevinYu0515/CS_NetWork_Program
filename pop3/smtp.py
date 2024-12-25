import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

# Email settings
smtp_server = '140.134.135.41'  # Your SMTP server address
smtp_port = 25 # Typically 587 for TLS
username = 'iecs04'
password = '5aBMRhcy'

# Sender and recipient
from_address = 'iecs01@netpg.ics.fcu.edu.tw'

# Create the email
subject = 'Cat Asciii art'

with open('message.txt', 'r', encoding='utf-8') as f:
    body = f.read()

print(body)
# Create a multipart message
message = MIMEText(body, 'plain')
message['From'] = from_address
message['Subject'] = subject
message['Date'] = formatdate(localtime=True)
message['User-Agent'] = 'Mutt/1.5.21 (2024-10-16)' 

server = smtplib.SMTP(smtp_server, smtp_port)
try:
    for j in range(1):
        # for i in range(10):
        #     to_address = f"iecs0{i + 1}" if i + 1 < 10 else f"iecs{i + 1}"
        to_address = "iecs04"
        message['To'] = to_address
        server.sendmail(from_address, to_address, message.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    # Terminate the SMTP session
    server.quit()
