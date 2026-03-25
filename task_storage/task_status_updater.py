# task_storage/task_status_updater.py

import json
import os
from typing import List, Dict
from utils.constants import TASKS_JSON_PATH  # ✅ 新增导入

# 默认路径使用 data/tasks.json
TASK_FILE = TASKS_JSON_PATH

def load_tasks(filename: str = TASK_FILE) -> List[Dict]:
    """
    从JSON文件加载任务列表，文件不存在时返回空列表。
    """
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_tasks(tasks: List[Dict], filename: str = TASK_FILE):
    """
    将任务列表保存到JSON文件，并强制同步写入磁盘。
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
        f.flush()  # 立即写入内核缓冲区
        os.fsync(f.fileno())  # 立即写入磁盘

def update_task_status(task_name: str, new_status: str, filename: str = TASK_FILE) -> bool:
    """
    根据任务名称更新任务状态，成功返回True，任务不存在返回False。
    """
    tasks = load_tasks(filename)
    updated = False
    for task in tasks:
        if task.get("task") == task_name:
            task["status"] = new_status
            updated = True
            break

    if updated:
        save_tasks(tasks, filename)
        print(f"✅ Task '{task_name}' status updated to '{new_status}'.")
        return True
    else:
        print(f"⚠️ Task '{task_name}' not found.")
        return False
