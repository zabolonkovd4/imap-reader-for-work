import email
import imaplib
import os
import webbrowser
from email.header import decode_header

# creds
username = 'username'
password = 'password'
imap_server = 'server.com'

# creating imap4 class with ssl
imap = imaplib.IMAP4_SSL(imap_server)

# auth
imap.login(username, password)

status, message = imap.select("INBOX")

N = 5
messages = int(message[0])


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


for i in range(messages, messages - N, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            print('encoding={}'.format(encoding))
        if isinstance(response, bytes):
            subject = subject.decode(encoding)
        From, encoding = decode_header(msg.get("From"))[0]
        if isinstance(From, bytes):
            From = From.decode(encoding)
        print("Subject:", subject)
        print("From:", From)
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
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # print text/plain emails and skip attachments
                    print(body)
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
                        open(filepath, "wb").write(part.get_payload(decode=True))
        else:
            # extract content type of email
            content_type = msg.get_content_type()
            # get the email body
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
                # print only text email parts
                print(body)
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
        print("=" * 100)
