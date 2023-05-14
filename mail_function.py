import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import unidecode
from imapclient import IMAPClient
from threading import Thread
def mail_function(info_from,info_to,topik, text,lock_smtp,lock_imap):
    print(unidecode.unidecode(topik))

    msg = MIMEText(text)
    #body = MIMEMultipart('alternative')

    msg["Subject"] = topik

    msg['From'] = f"{info_from['name']}<{info_from['mail']}>"
    full_name = ""
    try:
        full_name += f"{info_to['firstName']}"
    except:
        pass
    try:
        full_name += " " + f"{info_to['lastName']}"
    except:
        pass
    msg['To'] = f"{full_name}<{info_to['email']}>"
   # body.attach(MIMEText(text, 'plain'))
    #msg.attach(body)
    #msg["X-MAILER"] = "coltrans.pl webmail"
    msg["X-ME-DestFolders"] = "INBOX"
    respond=0
    t=0
    while respond==0 and t<10:
        try:
            t+=1
            with lock_smtp:
                with smtplib.SMTP('coltrans.pl', 587) as server:




                    server.login(f"{info_from['mail']}", f"{info_from['password']}")

                    respond=server.send_message(msg)
        except Exception as e:
            pass
    if respond==0:
        exit()
    t=0
    while t<5:
        t+=1
        try:
            with lock_imap:
                imap = IMAPClient('coltrans.pl', use_uid=True)
                imap.login(f"{info_from['mail']}", f"{info_from['password']}")
                respond = imap.append('SENT', msg.as_bytes(), flags=(b'\\Seen'))
                if "Done" in str(respond):
                    break
        except:
            pass

    return msg



