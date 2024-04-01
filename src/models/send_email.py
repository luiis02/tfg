import smtplib
import ssl
from email.message import EmailMessage


def sendEmail(subject,body, receiver = "luisalcaldegarcia.02@gmail.com"):
    email_sender = 'apuntajefe@gmail.com'
    email_password = 'dfvc fokn tndf hztv'
    email_receiver = receiver

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())