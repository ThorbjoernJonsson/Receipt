import email
import imaplib
import os

EMAIL_ACCOUNT = "thorbjornjons@gmail.com"
PASSWORD = "Jtbhrjtjmj5%"
path = r'Receipt\Unfiltered receipts'
def run_thr_em():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('Receipts')
    result, data = mail.uid('search', None, "Unseen") # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        temp = date_tuple[2]

        if os.path.isdir(path):
            download_img(email_message, "{}{}{:02d}_{}.jpg".format(date_tuple[0], date_tuple[1], date_tuple[2], x))
        else:
            os.mkdir(path)
            download_img(email_message, "{}{}{:02d}_{}.jpg".format(date_tuple[2], date_tuple[2], date_tuple[2], x))


def download_img(email_message, name):
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(path, name)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
run_thr_em()