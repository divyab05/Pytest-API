import email
import imaplib
import logging
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities import Crypt


class GmailClient:

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        self.imap_email = str(app_config.env_cfg['imap_email'])
        self.imap_password = str(app_config.env_cfg['imap_password'])
        self.decodedPassword = Crypt.decode(key='GMAILENCRYPTIONKEY', enc=self.imap_password)

    def read_email_from_gmail(self, count=1, contain_body=False):
        """
        This function is used to connect to gmail via imap and read emails.
        :param count: count of emails to iterate over
        :param contain_body: to check body of the email

        :return: Currently it is returning the subject of the email received
        """
        subject = None
        while subject is None:
            # Create server and login
            try:
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login(self.imap_email, self.decodedPassword)

                # Using SELECT to choose the e-mails.
                res, messages = mail.select('INBOX')

                # Caluclating the total number of sent Emails
                messages = int(messages[0])

                # Iterating over the sent emails
                for i in range(messages, messages - count, -1):
                    # RFC822 protocol
                    res, msg = mail.fetch(str(i), "(RFC822)")
                    for response in msg:
                        if isinstance(response, tuple):
                            msg = email.message_from_bytes(response[1])
                            # Store subject of the email
                            subject = msg["Subject"]

                mail.close()
                mail.logout()
            except:
                pass

            return subject


