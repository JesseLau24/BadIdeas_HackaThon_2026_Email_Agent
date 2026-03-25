# task_storage/task_writer.py

import json
import os
from typing import List, Dict
from utils.constants import TASKS_JSON_PATH  # ✅ 新增导入
import uuid

# 默认路径使用 data/tasks.json
TASK_FILE = TASKS_JSON_PATH

def load_tasks(filename: str = TASK_FILE) -> List[Dict]:
    """
    Load existing tasks from a JSON file. Return empty list if file doesn't exist.
    """
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_tasks(tasks: List[Dict], filename: str = TASK_FILE):
    """
    Save list of task dicts to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def append_tasks(new_tasks: List[Dict], filename: str = TASK_FILE):
    """
    Append new tasks to file. Avoid duplicates based on 'task' field.
    Ensure each task has a 'status' field (default to 'to do').
    """
    existing = load_tasks(filename)
    existing_task_names = {task["task"] for task in existing}

    normalized = []
    for t in new_tasks:
        t = t.copy()
        t["status"] = t.get("status", "to do")
        t["source"] = t.get("source", "manual")
        t["deadline"] = t.get("deadline", t.get("due_date", ""))
        t["id"] = t.get("id", str(uuid.uuid4()))  # 👈 自动补 ID
        normalized.append(t)

    filtered = [t for t in normalized if t["task"] not in existing_task_names]

    if filtered:
        updated = existing + filtered
        save_tasks(updated, filename)
        print(f"✅ Added {len(filtered)} new task(s) to {filename}")
    else:
        print("📭 No new tasks to add (all duplicates)")