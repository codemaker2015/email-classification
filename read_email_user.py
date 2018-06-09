#-------------------------------------------------------------------------------
# Name:        read_email.py
# Purpose:     Retrieve All the emails from Gmail
#
# Author:      Vishnu Sivan
# Created:     20/03/2018
# Licence:      In the spirit of sharing knowledge and happiness,
#               You can copy, edit, share
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


import sys
from datetime import datetime, timedelta
import os
import re
import imaplib
import email


# # Read only emails from last 3 days
no_days_query = 3

server = "imap.gmail.com"
port_num = 993


def read_email1(gmail_user, gmail_pwd):

    conn = imaplib.IMAP4_SSL(server, port_num)
    conn.login(gmail_user, gmail_pwd)
    conn.select()

    #Check status for 'OK'
    status, all_folders = conn.list()

    folder_to_search = 'INBOX'
    folder_to_search = '[Google Mail]/All Mail'

    #Check status for 'OK'
    status, select_info = conn.select(folder_to_search)

    if status == 'OK':
        today = datetime.today()
        cutoff = today - timedelta(days=no_days_query)

        from_email = 'hemaelavumkudy@gmail.com'
        
        search_key = from_email + " after:" + cutoff.strftime('%Y/%m/%d')

        status, message_ids = conn.search(None, 'X-GM-RAW', search_key)


        for id in message_ids[0].split():
            status, data = conn.fetch(id, '(RFC822)')

            email_msg = email.message_from_string(data[0][1])

            #Print all the Attributes of email message like Subject,
            #print email_msg.keys()

            subject = email_msg['Subject']
            sender_email =  email_msg['From']
            sent_to_email =  email_msg['To']

            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_content = part.get_payload() # prints the raw text
                    #TODO :
                    #process_email() #Delete, Mark as Spam, Forward it
                    #TODO :
                    #print email_content

    else:
        print "Error"
    ## Search for relevant messages
    ## see http://tools.ietf.org/html/rfc3501#section-6.4.5









if __name__ == '__main__':

    # Gmail Configuration
    gmail_user = 'emailclassification.tcs@gmail.com'
    gmail_pwd = 'codemaker'

    ret = read_email1(gmail_user, gmail_pwd)

