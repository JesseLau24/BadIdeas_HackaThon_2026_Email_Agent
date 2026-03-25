import imaplib
import email
from email.header import decode_header
from datetime import datetime, timezone
import re

def fetch_recent_emails(EMAIL, APP_PASSWORD, IMAP_SERVER, last_processed_timestamp=None, limit=5):
    """
    Fetch the most recent emails from the user's inbox via IMAP.

    Parameters:
        EMAIL (str): Email account for IMAP login.
        APP_PASSWORD (str): App password for the email account.
        IMAP_SERVER (str): IMAP server address (e.g., imap.gmail.com).
        last_processed_timestamp (str, optional): ISO formatted timestamp of the last processed email.
            Only emails after this timestamp will be fetched.
        limit (int, optional): Maximum number of recent emails to fetch. Defaults to 5.

    Returns:
        list of dict: Each dictionary contains:
            - subject (str): Email subject line.
            - from (str): Sender email address.
            - body (str): Plain text body of the email.
            - timestamp (str): UTC ISO timestamp of the email date.

    Notes:
        - Emails earlier than last_processed_timestamp are skipped to avoid re-processing.
        - Only 'text/plain' parts are extracted for multipart emails.
    """
    mails = []
    try:
        # Connect to IMAP server using SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        # Search all emails in inbox
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        latest_ids = mail_ids[-limit:]  # Take only the latest 'limit' emails

        for i in latest_ids:
            status, msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Decode email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")

            # Extract plain text email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # Convert email date to UTC ISO timestamp
            date_tuple = email.utils.parsedate_tz(msg["Date"])
            timestamp = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple), tz=timezone.utc)

            # Skip emails that are older than last_processed_timestamp
            if last_processed_timestamp:
                last_dt = datetime.fromisoformat(last_processed_timestamp)
                if timestamp <= last_dt:
                    continue

            mails.append({
                "subject": subject,
                "from": from_,
                "body": body,
                "timestamp": timestamp.isoformat()
            })
        mail.logout()
    except Exception as e:
        print("❌ IMAP error:", e)

    return mails


def extract_name_from_email(email_addr: str) -> str:
    """
    Extract the sender's name from an email address string.

    Parameters:
        email_addr (str): The email address string, e.g., "Jesse Huang <jesse@example.com>"

    Returns:
        str: The extracted name if present, otherwise the username part of the email.
    
    Notes:
        - If the email address contains '<>', the part before '<' is considered the name.
        - If no name is found, returns the part before '@' in the email.
    """
    if not email_addr:
        return ""
    # Extract the name portion from "Name <email@example.com>"
    match = re.match(r'(.*)<.*>', email_addr)
    if match:
        name = match.group(1).strip()
        return name
    # Fallback: return username part of the email
    return email_addr.split('@')[0]