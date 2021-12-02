import email
import os
import smtplib
import time
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import utils


def clear_logs():
    """Clears log files of emails sent and not sent"""
    try:
        os.remove("logs/sent.log")
        os.remove("logs/notsent.log")
    except FileNotFoundError:
        return
    except Exception as e:
        raise e


def message_replace(user: str, uuid: str, confirm_link: str, message: str) -> str:
    """Replace tags in message with given information."""
    message = message.replace("{user}", user)
    message = message.replace("{confirm_link}", (confirm_link + uuid))
    return message


def send_mail_with_attachments(config: dict):
    """Sends mail with attachment to the sender"""
    sender_mail = config["mail"]
    sender_password = config["password"]
    message_content = config['attachment_mail_text']
    with smtplib.SMTP(config["host"], config["port"]) as smtp_client:
        # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.starttls
        smtp_client.starttls()
        smtp_client.login(sender_mail, sender_password)
        message = MIMEMultipart()
        message["Subject"] = config["attachments_subject"]
        message.attach(MIMEText(message_content, "plain"))
        filenames = ["data/mails.json", "logs/sent.log", "logs/notsent.log"]
        for filename in filenames:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename= {filename}"
            )
            message.attach(part)
        time.sleep(10)
        try:
            smtp_client.sendmail(
                sender_mail, sender_mail, message.as_string())
            print(f"{sender_mail} sent")
            utils.log(f"{utils.current_time()} {sender_mail} sent")
        except Exception as e:
            print(f"{sender_mail} not sent, exception: {e}")
            utils.log(
                f"{utils.current_time()} {sender_mail} not sent, reason: {e}")
    return


def send_mails(config: dict, receivers: map):
    """Sends mails to given receivers, with a given link."""
    sender_mail = config["mail"]
    sender_password = config["password"]
    with open(f"config/{config['mail_template']}", encoding="utf-8", mode="rt") as file:
        message_content = file.read()
    with smtplib.SMTP(config["host"], config["port"]) as smtp_client:
        # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.starttls
        smtp_client.starttls()
        smtp_client.login(sender_mail, sender_password)
        clear_logs()
        for receiver in receivers:
            message = EmailMessage()
            message['Subject'] = config["subject"]
            content = message_replace(
                receiver.name, receiver.uuid, config["confirm_link"], message_content)
            message.set_content(content)
            time.sleep(10)
            try:
                smtp_client.sendmail(
                    sender_mail, receiver.mail, message.as_string())
                print(f"{receiver.mail} sent")
                utils.log(f"{utils.current_time()} {receiver.mail} sent")
                utils.log_to_file("sent.log", f"{receiver.mail}")
            except Exception as e:
                print(f"{receiver.mail} not sent, exception: {e}")
                utils.log(
                    f"{utils.current_time()} {receiver.mail} not sent, reason: {e}")
                utils.log_to_file("notsent.log", f"{receiver.mail}")
