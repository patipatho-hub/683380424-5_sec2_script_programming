import imaplib
import email
from email.header import decode_header
import os
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

class EmailReceiver:
    """จัดการการรับและอ่านอีเมลผ่าน IMAP"""
    def __init__(self, imap_server, sender_email, sender_password):
        self.imap_server = imap_server
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.mail = None
        logger.info(f"EmailReceiver initialized for {sender_email}.")

    def _connect(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into IMAP server.")
            return True
        except Exception as e:
            logger.error(f"IMAP connection failed: {e}")
            self.mail = None
            return False

    def _disconnect(self):
        if self.mail:
            try:
                self.mail.logout()
                logger.info("Disconnected from IMAP server.")
            except Exception as e:
                logger.warning(f"Error during IMAP disconnection: {e}")
            finally:
                self.mail = None

    def search_emails(self, mailbox='INBOX', criteria='UNSEEN', from_sender=None, subject_contains=None):
        if not self._connect():
            return []
        try:
            self.mail.select(mailbox)
            search_query = [criteria]
            if from_sender:
                search_query.extend(['FROM', from_sender])
            if subject_contains:
                search_query.extend(['SUBJECT', subject_contains])
            
            status, email_ids = self.mail.search(None, *search_query)
            if status != 'OK':
                return []
            
            uids = email_ids[0].split()
            logger.info(f"Found {len(uids)} emails matching criteria.")
            return uids
        except Exception as e:
            logger.error(f"Error searching emails: {e}")
            return []
        finally:
            self._disconnect()

    def fetch_email_content(self, uid, mark_as_read=True, download_attachments_dir=None):
        if not self._connect():
            return None
        try:
            self.mail.select('INBOX')
            status, msg_data = self.mail.fetch(uid, '(RFC822)')
            if status != 'OK':
                return None

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = self._decode_header_part(msg['From'])
            subject = self._decode_header_part(msg['Subject'])

            email_body = ""
            attachments_downloaded = []

            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename and download_attachments_dir:
                        ensure_directory_exists(download_attachments_dir)
                        filepath = os.path.join(download_attachments_dir, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        attachments_downloaded.append(filepath)
                elif "text/plain" in content_type and "attachment" not in content_disposition:
                    try:
                        email_body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                    except Exception:
                        email_body += "[ Undecodable text ]"

            if mark_as_read:
                self.mail.store(uid, '+FLAGS', '\\Seen')

            return {
                "uid": uid.decode('utf-8'),
                "sender": sender,
                "subject": subject,
                "body_snippet": email_body[:200] + "..." if len(email_body) > 200 else email_body,
                "attachments_downloaded": attachments_downloaded
            }
        except Exception as e:
            logger.error(f"Error fetching email UID {uid}: {e}")
            return None
        finally:
            self._disconnect()

    def _decode_header_part(self, header_value):
        if header_value is None:
            return ""
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        for part, charset in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(charset if charset else 'utf-8')
                except Exception:
                    decoded_string += part.decode('latin-1', errors='replace')
            else:
                decoded_string += part
        return decoded_string.strip()