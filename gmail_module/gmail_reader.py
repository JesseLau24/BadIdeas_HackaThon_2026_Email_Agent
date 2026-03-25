# gmail_module/gmail_reader.py

import imaplib
import email
from email.header import decode_header
from typing import List, Tuple
from datetime import datetime, timezone


class GmailReader:
    def __init__(self, email_address: str, app_password: str):
        self.email_address = email_address
        self.app_password = app_password
        self.mail = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.email_address, self.app_password)
        self.mail.select("inbox")

    def fetch_new_email_bodies_since(self, last_processed_time: datetime) -> List[Tuple[str, datetime]]:
        """
        Fetch email bodies received after `last_processed_time` (assumed to be in UTC).
        Returns a list of (body, received_datetime) tuples.
        """
        status, messages = self.mail.search(None, "ALL")
        email_ids = messages[0].split()
        new_emails = []

        for eid in reversed(email_ids):  # newest first
            status, data = self.mail.fetch(eid, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Parse date
            date_str = msg["Date"]
            parsed_date = email.utils.parsedate_to_datetime(date_str)
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            else:
                parsed_date = parsed_date.astimezone(timezone.utc)

            # Skip already processed emails
            if parsed_date <= last_processed_time:
                break

            # Extract plain text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            new_emails.append((body, parsed_date))

        return list(reversed(new_emails))  # return oldest first

    def logout(self):
        self.mail.logout()
