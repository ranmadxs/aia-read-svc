# test_capitalize.py
import imaplib
import time
import poplib
import smtplib
from dotenv import load_dotenv
import os
load_dotenv()
#poetry run pytest -s

#poetry run pytest tests/test_mail.py::test_send_yahoo -s
def test_send_yahoo():
    fromMy = 'grineldosanchez@yahoo.es' # fun-fact: "from" is a keyword in python, you can't use it as variable.. did anyone check if this code even works?
    to  = 'ranmadxs@gmail.com'
    subj='TheSubject'
    date='2/1/2010'
    message_text='Hello Or any thing you want to send'

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )
    
    username = str('grineldosanchez@yahoo.es')  
    password = str(os.environ['YAHOO_PASSWORD']) 
    
    try :
        server = smtplib.SMTP("smtp.mail.yahoo.com",587)
        server.login(username,password)
        server.sendmail(fromMy, to,msg)
        server.quit()    
        print('ok the email has sent ')
    except :
        print('can\'t send the Email')    

#poetry run pytest tests/test_mail.py::test_yahoo_mail -s
def test_yahoo_mail():
    print("Test yahoo mail")
    M = poplib.POP3_SSL('pop.mail.yahoo.com', 995) #Connect to hotmail pop3 server
    M.set_debuglevel(2)
    success = False;
    user = "grineldosanchez@yahoo.es"

    while success == False:
        try:
            password = "pana1108"
            M.user(user)
            M.pass_(password)
        except:
            print("Invalid credentials")
        else:
            print("Successful login realyyyyy??")
            pop3info = M.stat() #access mailbox status
            print(pop3info)
            success = True
    assert True


def test_google_mail_example():
    print("Test google mail")
    start = time.time()
    ################ IMAP SSL Establish Connection #################
    start = time.time()
    try:
        #imap_ssl = imaplib.IMAP4_SSL(host="export.imap.mail.yahoo.com", port=993)
        imap_ssl = imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT)
    except Exception as e:
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
        imap_ssl = None

    print("Connection Object : {}".format(imap_ssl))
    print("Total Time Taken  : {:,.2f} Seconds\n".format(time.time() - start))

    ############### Login to Mailbox ######################
    print("Logging into mailbox...")
    try:
        #resp_code, response = imap_ssl.login("grineldosanchez@yahoo.es", "pana1108")
        resp_code, response = imap_ssl.login("ranmadxs@gmail.com", "mdjrcamcaaxhlupg")
    except Exception as e:
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
        resp_code, response = None, None

    print("Response Code : {}".format(resp_code))
    print("Response      : {}\n".format(response[0].decode()))

    ############### Logout of Mailbox ######################
    print("\nLogging Out....")
    try:
        resp_code, response = imap_ssl.logout()
    except Exception as e:
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
        resp_code, response = None, None

    print("Response Code : {}".format(resp_code))
    print("Response      : {}".format(response[0].decode()))    
    assert True