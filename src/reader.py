import email
import imaplib
import logging
import os
import asyncio
import webbrowser
from email.header import decode_header
from repeated_timer import RepeatedTimer
from imap_message import ImapMessage
from collections import OrderedDict
#import client

# creds
username = 'zabolonkovd4@ptri.unn.ru'
password = 'Qua*pAD_Scoob'
imap_server = 'ptri.unn.ru'

# creating imap4 class with ssl
imap = imaplib.IMAP4_SSL(imap_server)

# auth
imap.login(username, password)

status, message = imap.select("INBOX")

# imap message container
msgs = set()

N = 5
messages = int(message[0])


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def imap_poll():
    # iterate over last N message
    print(messages)
    print(messages - N)
    for i in range(messages, messages - N, -1):
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
            #print("Subject:", subject)
            #print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        imap_message = ImapMessage()
                        body = part.get_payload(decode=True).decode()
                        imap_message.content = body
                        print(i)
                        print(body)
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        # pack imap body message
                        imap_message.content = body
                        #print(body)
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
                            imap_message.attachment = attachment
                            open(filepath, "wb").write(attachment)
                            # TODO: send file via bot, then remove the file from os
                            imap_message.content = body
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    #print(body)
                    pass
                imap_message.content = body
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
                imap_message.content = body
                # TODO: send a file via bot, then delete from os
                #await client.send_message()
            msgs.add(imap_message)
            print("=" * 100)
    return msgs


if __name__ == '__main__':
    #rt = RepeatedTimer(5, imap_poll)
    #rt.start()
    messages = imap_poll()
    print("len of set: {}".format(len(messages)))
    for msg in messages:
        print(msg.content)
    #client.executor.start_polling(client.dp, skip_updates=True)

