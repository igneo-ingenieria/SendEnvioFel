
import logging
import re
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Falta control de error para nombre correo bien escrito

def comprobar_formato_gmail(email):
    exp_reg = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if re.match(exp_reg, email):
        return True
    else:
        return False

def send_email(sender_email, sender_password, recipient_email, subject, smtp_server, body_html ,image_rute, smtp_port):
    # Create the email
    message = MIMEMultipart("related")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    texto_html = MIMEMultipart("alternative")
    message.attach(texto_html)

    texto_html.attach(MIMEText(body_html, "html"))

    with open(image_rute, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<imagen1>')
        mime_image.add_header('Content-Disposition', 'inline')
        message.attach(mime_image)

    try:
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(message)
            return True
    except smtplib.SMTPAuthenticationError:
        logging.error("Correo electronico o contraseña erronea")
        return False
    except smtplib.SMTPConnectError:
        logging.error("No se ha podido conectar al servidor SMTP")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"Error SMTP: {e}")
        return False
    except Exception as e:
        logging.error(f"Error: {e}")
        return False