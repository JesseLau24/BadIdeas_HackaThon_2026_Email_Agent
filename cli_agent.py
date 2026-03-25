# cli_agent.py

import imaplib
import email
from email.header import decode_header
import json
import subprocess
import os
from datetime import datetime, timezone
from task_storage.task_writer import append_tasks
from task_storage.task_parser import extract_task_list_from_output

# ======================
# ⚙️ 配置区
# ======================
EMAIL = "lazybomb1024@gmail.com"
APP_PASSWORD = "tmzb bqxm kcsp tihv"
IMAP_SERVER = "imap.gmail.com"

TASKS_PATH = "data/tasks.json"
LAST_PROCESSED_JSON_PATH = "data/last_processed.json"
STRIKE_PATH = "data/strikes.json"

OLLAMA_MODEL = "phi4:14b"  # 确保本地已有

# ======================
# 📬 IMAP 读取邮件
# ======================
def fetch_recent_emails(last_processed_timestamp: str = None, limit=5):
    mails = []

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        latest_ids = mail_ids[-limit:]

        for i in latest_ids:
            status, msg_data = mail.fetch(i, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # 邮件时间
            date_tuple = email.utils.parsedate_tz(msg["Date"])
            timestamp = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple), tz=timezone.utc)

            # 根据 last_processed_timestamp 过滤
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


# ======================
# 😈 读取 strike
# ======================
def load_strikes():
    if not os.path.exists(STRIKE_PATH):
        return {}
    with open(STRIKE_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

# ======================
# 🧠 调用 Ollama
# ======================
def call_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",   # 解决 UnicodeDecodeError
            errors="replace"    # 遇到无法解码字符替换掉
        )
        if result.stderr.strip():
            print("🔹 Ollama stderr:", result.stderr.strip())
        output = result.stdout
        if not output:
            return ""
        return output.strip()
    except Exception as e:
        print(f"❌ Ollama subprocess error: {e}")
        return ""

# ======================
# 🤖 从邮件抽取任务
# ======================
def extract_tasks_from_email(email_body: str):
    prompt = f"""
Extract all tasks from the following email and output as a JSON list.
Each task must have the following fields (fill with available info; empty string if unknown):

[
  {{
    "task": "task description",
    "due_date": "YYYY-MM-DDTHH:MM",
    "priority": "low/medium/high",
    "assigner": "name",
    "comments": "any additional details",
    "status": "to do",
    "deadline": "YYYY-MM-DDTHH:MM",
    "email_content": "{email_body.replace('"','\\"')}",
    "id": "generate a uuid4 string",
    "source": "email"
  }}
]

Only output valid JSON list. Do not include any extra text or explanation.
"""
    output_text = call_ollama(prompt)
    if not output_text:
        return []

    tasks = extract_task_list_from_output(output_text, debug=True)
    if not tasks:
        print("⚠️ Failed to parse Ollama output.")
        return []
    return tasks

# ======================
# 💬 CLI 对话
# ======================
def main():
    print("🤖 LazyBomb Agent CLI (Ollama + IMAP)")
    print("Type 'exit' to quit.\n")

    # 读取 last_processed.json
    last_processed_timestamp = None
    if os.path.exists(LAST_PROCESSED_JSON_PATH):
        with open(LAST_PROCESSED_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                last_processed_timestamp = json.load(f).get("last_processed")
            except:
                last_processed_timestamp = None
    print(f"📅 Last processed timestamp: {last_processed_timestamp}")

    while True:
        user_input = input(">> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        print("📬 Fetching emails...")
        emails = fetch_recent_emails(last_processed_timestamp)
        print(f"📅 Found {len(emails)} new emails. Extracting tasks...")

        new_tasks_count = 0
        for email_data in emails:
            tasks = extract_tasks_from_email(email_data["body"])
            for task in tasks:
                # 添加邮件内容、source、id、status
                task["email_content"] = email_data["body"]
                task["source"] = "email"
                task["status"] = task.get("status", "to do")
                task["id"] = task.get("id", str(os.urandom(16).hex()))

            if tasks:
                append_tasks(tasks, TASKS_PATH)
                new_tasks_count += len(tasks)

        if new_tasks_count == 0:
            print("📭 No new tasks to add.")
        else:
            print(f"✅ Added {new_tasks_count} new task(s) to {TASKS_PATH}")

        # 更新 last_processed.json
        if emails:
            latest_timestamp = emails[-1]["timestamp"]
            with open(LAST_PROCESSED_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"last_processed": latest_timestamp}, f, indent=2)
            print(f"✅ Updated last processed timestamp to {latest_timestamp}")
            last_processed_timestamp = latest_timestamp

        print("😈 Loading strikes...")
        strikes = load_strikes()

        print("🧠 Thinking...\n")
        # 这里可以直接用 Ollama 做总结
        prompt = f"""
You are an AI productivity assistant.

User asked:
{user_input}

Here is email data:
{json.dumps(emails, indent=2)}

Please summarize tasks and highlight urgent/overdue ones.
"""
        summary = call_ollama(prompt)
        print("====== AI RESPONSE ======")
        print(summary)
        print("=========================\n")


if __name__ == "__main__":
    main()