import email
import imaplib
import logging
import os
import webbrowser
from email.header import decode_header
from imap_message import ImapMessage
from collections import OrderedDict
from env_parser import EnvParser

env = EnvParser()


# Logger
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s(%(filename)s:%(lineno)d)] %(message)s',
    level=env.logging_level
)


def imap_auth(imap_server: str, username: str, password: str) -> imaplib.IMAP4_SSL:
    # creating imap4 class with ssl
    imap = imaplib.IMAP4_SSL(imap_server)
    # auth
    imap.login(username, password)
    return imap


def imap_get_messages(imap: imaplib.IMAP4_SSL) -> int:
    status, message = imap.select("INBOX")
    return int(message[0])


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def imap_poll():
    imap = imap_auth(env.imap_server, env.imap_username, env.imap_password)
    messages = imap_get_messages(imap)
    # imap message container
    msgs = OrderedDict()
    # iterate over last N message
    for i in range(messages, messages - env.last_messages_count, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(response, bytes):
                try:
                    subject = subject.decode(encoding)
                except TypeError:
                    continue
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                        imap_message = ImapMessage(content=body)
                        logging.info("#{} Message body read: {}".format(i, imap_message.content))
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        # pack imap body message
                        imap_message = ImapMessage(content=body)
                        logging.info("Message body read: {}".format(imap_message.content))
                    elif "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            attachment = part.get_payload(decode=True)
                            open(filepath, "wb").write(attachment)
                            imap_message = ImapMessage(content=body, attachment=attachment)
                            # TODO: send file via bot, then remove the file from os
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    imap_message = ImapMessage(content=body)
                    logging.info("#{} Message body read: {}".format(i, imap_message.content))
            if content_type == "text/html":
                # if it's HTML, create a new HTML file and open it in browser
                folder_name = clean(subject)
                if not os.path.isdir(folder_name):
                    # make a folder for this email (named after the subject)
                    os.mkdir(folder_name)
                filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                open(filepath, "w").write(body)
                # open in the default browser
                webbrowser.open(filepath)
                imap_message = ImapMessage(content=body)
                # TODO: send a file via bot, then delete from os
            msgs[imap_message] = None
            print("=" * 100)
    return msgs
