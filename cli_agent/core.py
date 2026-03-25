import os
import json
from .email_utils import fetch_recent_emails, extract_name_from_email
from .ai_utils import call_ollama, extract_tasks_from_email
from task_storage.task_writer import append_tasks

def run_cli_agent(EMAIL, APP_PASSWORD, IMAP_SERVER, TASKS_PATH, LAST_PROCESSED_JSON_PATH):
    """
    Main CLI loop for LazyBomb Agent, integrating email fetching, task extraction, and AI summarization.

    Parameters:
        EMAIL (str): Email account used for IMAP login.
        APP_PASSWORD (str): App password for email login.
        IMAP_SERVER (str): IMAP server address.
        TASKS_PATH (str): Path to the JSON file storing all tasks.
        LAST_PROCESSED_JSON_PATH (str): Path to JSON file storing last processed email timestamp.

    Functionality:
        - Continuously prompt the user for input in CLI.
        - Fetch recent emails after last processed timestamp.
        - Extract tasks from emails using LLM.
        - Deduplicate tasks using 'deadline + assigner'.
        - Append new tasks to TASKS_PATH.
        - Update last processed timestamp safely.
        - Call AI (Ollama) to summarize current tasks and highlight urgent/overdue ones.
    """

    # Welcome message for CLI users
    print("🤖 LazyBomb Agent CLI (Ollama + IMAP)")
    print("Type 'exit' to quit.\n")

    # Load the last processed timestamp to avoid re-processing old emails
    last_processed_timestamp = None
    if os.path.exists(LAST_PROCESSED_JSON_PATH):
        try:
            with open(LAST_PROCESSED_JSON_PATH, "r", encoding="utf-8") as f:
                last_processed_timestamp = json.load(f).get("last_processed")
        except:
            last_processed_timestamp = None
    print(f"📅 Last processed timestamp: {last_processed_timestamp}")

    # ======================
    # CLI main loop
    # ======================
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            break  # Exit CLI loop gracefully

        # ----------------------
        # 1️⃣ Fetch emails
        # ----------------------
        print("📬 Fetching emails...")
        emails = fetch_recent_emails(EMAIL, APP_PASSWORD, IMAP_SERVER, last_processed_timestamp)
        print(f"📅 Found {len(emails)} new emails. Extracting tasks...")

        # ----------------------
        # 2️⃣ Load existing tasks
        # ----------------------
        all_tasks = []
        if os.path.exists(TASKS_PATH):
            try:
                with open(TASKS_PATH, "r", encoding="utf-8") as f:
                    all_tasks = json.load(f)
            except:
                all_tasks = []

        new_tasks_count = 0

        # ----------------------
        # 3️⃣ Extract tasks from each new email
        # ----------------------
        for email_data in emails:
            tasks = extract_tasks_from_email(email_data["body"])
            for task in tasks:
                # Fill assigner from email sender if missing
                if not task.get("assigner"):
                    task["assigner"] = extract_name_from_email(email_data["from"])

                # Ensure required fields
                task["email_content"] = email_data["body"]
                task["source"] = "email"
                task["status"] = task.get("status", "to do")
                task["id"] = task.get("id") or str(os.urandom(16).hex())

                # ----------------------
                # Deduplication: check if a task with same deadline + assigner exists
                # ----------------------
                duplicate = any(
                    t.get("deadline") == task.get("deadline") and
                    t.get("assigner") == task.get("assigner")
                    for t in all_tasks
                )
                if duplicate:
                    continue  # Skip adding duplicate tasks

                # Append new unique task
                all_tasks.append(task)
                new_tasks_count += 1

        # ----------------------
        # 4️⃣ Save new tasks and update last_processed timestamp
        # ----------------------
        if new_tasks_count > 0:
            append_tasks(all_tasks, TASKS_PATH)
            print(f"✅ Added {new_tasks_count} new task(s) to {TASKS_PATH}")

            if emails:
                latest_timestamp = emails[-1]["timestamp"]
                try:
                    with open(LAST_PROCESSED_JSON_PATH, "w", encoding="utf-8") as f:
                        json.dump({"last_processed": latest_timestamp}, f, indent=2)
                    last_processed_timestamp = latest_timestamp
                    print(f"✅ Updated last processed timestamp to {latest_timestamp}")
                except Exception as e:
                    print(f"❌ Failed to update last_processed.json: {e}")
        else:
            if emails:
                print("📭 No new tasks to add. (All tasks are duplicates and skipped)")
            else:
                print("📭 No new tasks to add.")

        # ----------------------
        # 5️⃣ Summarize tasks with AI
        # ----------------------
        prompt = f"""
You are an AI productivity assistant.

User asked:
{user_input}

Here is current task data:
{json.dumps(all_tasks, indent=2)}

Please summarize tasks and highlight urgent/overdue ones.
"""
        summary = call_ollama(prompt)
        print("====== AI RESPONSE ======")
        print(summary)
        print("=========================\n")