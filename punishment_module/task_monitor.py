# punishment_module/task_monitor.py

import json
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple

from utils.constants import TASKS_JSON_PATH
from punishment_module.strike_handler import record_strike


def load_tasks() -> List[Dict]:
    if os.path.exists(TASKS_JSON_PATH):
        with open(TASKS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def parse_deadline(deadline_str: str) -> datetime:
    """
    Convert ISO datetime string to aware datetime.
    """
    return datetime.fromisoformat(deadline_str)


def monitor_tasks() -> Tuple[List[Dict], List[Dict]]:
    """
    检查任务状态，返回两个列表：
    - reminder_tasks：即将到期，需提醒
    - strike_tasks：严重超时，需惩罚
    """
    now = datetime.now(timezone.utc)
    tasks = load_tasks()

    reminder_tasks = []
    strike_tasks = []

    for task in tasks:
        status = task.get("status", "to do").lower()
        deadline_str = task.get("deadline") or task.get("due_date")
        if not deadline_str:
            continue

        try:
            deadline = parse_deadline(deadline_str).astimezone(timezone.utc)
        except Exception as e:
            print(f"⚠️ Failed to parse deadline for task: {task.get('task')}, error: {e}")
            continue

        time_to_deadline = deadline - now
        time_past_deadline = now - deadline

        if status in ["to do", "i'm on it"]:
            if timedelta(seconds=0) <= time_to_deadline <= timedelta(minutes=15):
                print(f"🔔 Reminder: Task '{task['task']}' is due in less than 15 minutes.")
                reminder_tasks.append(task)

            if time_past_deadline > timedelta(minutes=15):
                print(f"☠️ STRIKE: Task '{task['task']}' missed deadline over 15 minutes ago.")
                strike_tasks.append(task)
                record_strike(task)

    return reminder_tasks, strike_tasks
