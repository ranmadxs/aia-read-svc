#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imaplib, email  # Library to interact with IMPAP server
import sys
from email.header    import Header
from email.mime.text import MIMEText
from getpass import getpass
from smtplib import SMTP_SSL
from dotenv import load_dotenv
import os
import pprint
from email.header import decode_header
import poplib
load_dotenv()

#poetry run pytest tests/test_yahoo.py::test_pop3 -s
def test_pop3():
    # input email address, password and pop3 server domain or ip address
    email= "grineldosanchez@yahoo.com"
    password = str(os.environ['YAHOO_PASSWORD'])
    pop3_server = "pop.mail.yahoo.com"
    server = poplib. POP3 (pop3_server) # connect to pop3 server
    # print debug information between client and pop3 server
    server.set_debuglevel(1)
    # get pop3 server welcome message.
    pop3_server_welcome_msg = server.getwelcome().decode('utf-8')
    # print out the pop3 server welcome message.
    print(server.getwelcome().decode('utf-8'))
    # user account authentication
    server.user(email)
    server.pass_(password)
    # stat() function return email count and occupied disk size
    print ('Messages: %s. Size: %s'% server.stat())
    # list() function return all email list
    resp, mails, octets = server.list()
    print(mails)
    # retrieve the newest email index number
    index = len(mails)
    # retr can get the contents of the email with index number
    resp, lines, octets = server.retr(index)
    # lines stores each line of the original text of the message
    msg_content=b'\r\n'.join(lines).decode('utf-8')
    # now parse out the email object.
    msg = Parser().parsestr(msg_content)
    # get email from, to, subject attribute value.
    email_from = msg.get ('From')
    email_to = msg.get('To')
    email_subject= msg.get("Subiect")
    print('From: '+ email_from)
    print('To email to')
    print('Subject: ' + email_subject)
    # delete the email from pop3 server directly by email index.
    #
    server.dele(index)
    # close pop3 server
    server.quit()

def obtain_header(msg):
    # decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes) and encoding != None:
        subject = subject.decode(encoding)
 
    # decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
 
    #print("Subject:", subject)
    #print("From:", From)
    return subject, From

#poetry run pytest tests/test_yahoo.py::test_read -s
def test_read():
    IMAP_server = "imap.mail.yahoo.com"  # Yahoo IMAP server
    mail_id = "grineldosanchez@yahoo.com"
    imap = imaplib.IMAP4_SSL(IMAP_server)
    pwd = str(os.environ['YAHOO_PASSWORD3'])
    # login to the server
    try:
        status, summary = imap.login(mail_id, pwd)
        if status == "OK":
            print(imap.list()) # print various inboxes
            print(summary)                
            status, messages = imap.select("INBOX")
            numOfMessages = int(messages[0])  
            print(numOfMessages)          
            for i in range(numOfMessages, numOfMessages - 10, -1):
                res,msg = imap.fetch(str(i), "(RFC822)")  # fetches email using ID
            
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject, From = obtain_header(msg)                            
                        print("------------------------------------------------")
                        print(subject)
                        print(From)
                        print("<"+str(From) + "> " + str(subject))
            imap.close()

    except imaplib.IMAP4.error:
        print("Error logging into Mail")
        sys.exit(0)  # Successful termination

#https://coderslegacy.com/python/imap-read-emails-with-imaplib/
#poetry run pytest tests/test_yahoo.py::test_read22 -s
def test_read22():
    IMAP_server = "imap.mail.yahoo.com"  # Yahoo IMAP server
    mail_id = "grineldosanchez@yahoo.com"
    imap = imaplib.IMAP4_SSL(IMAP_server)
    pwd = str(os.environ['YAHOO_PASSWORD'])
    # login to the server
    try:
        status, summary = imap.login(mail_id, pwd)
        if status == "OK":
            print(summary)
            imap.select('Inbox')
            tmp, data = imap.search(None, 'ALL')
            ids = data[0]
            id_list = ids.split()
            #get the most recent email id
            latest_email_id = int( id_list[-1] )
            print(latest_email_id)            
            for num in data[0].split():
                tmp, data = imap.fetch(num, '(RFC822)')
                print('Message: {0}\n'.format(num))
                pprint.pprint(data[0][1])
                break
            imap.close()

    except imaplib.IMAP4.error:
        print("Error logging into Mail")
        sys.exit(0)  # Successful termination



#poetry run pytest tests/test_yahoo.py::test_send_yahoo -s
def test_send_yahoo():
    # provide credentials
    login = 'grineldosanchez@yahoo.es'
    #password = getpass('Password for "%s": ' % login)
    password = str(os.environ['YAHOO_PASSWORD'])
    # create message
    msg = MIMEText('message body…33', 'plain', 'utf-8')
    msg['Subject'] = Header('subject…33', 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join([login, ])

    # send it   
    s = SMTP_SSL('smtp.mail.yahoo.com', timeout=10) #NOTE: no server cert. check
    s.set_debuglevel(0)
    try:
        s.login(login, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    finally:
        s.quit()
        