#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 10:04:22 2018

@author: codemaker
"""

import smtplib
import time
import imaplib
import email
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "emailclassification.tcs" + ORG_EMAIL
FROM_PWD    = "codemaker"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    #print(response_part)
                    msg = email.message_from_string(response_part[1])
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            email_body = part.get_payload()
                            attachment = part.get_payload()[1]
                        if part.get_content_type() in ['image/jpeg', 'image/png']:
                            open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
                    
                    email_subject = msg['subject']
                    email_from = msg['from']

                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
                    print 'Body : ' + email_body + '\n'
                    

    except Exception, e:
        print str(e)


read_email_from_gmail()
