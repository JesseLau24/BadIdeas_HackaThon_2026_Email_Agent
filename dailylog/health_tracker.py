# dailylog/health_tracker.py

import os
import json
from datetime import datetime
from pathlib import Path

from utils.constants import DATA_DIR
from dailylog.presets import health_goals  # we'll define this in __init__.py below

# 日志路径：data/daily_logs/2025.json（根据年份自动生成）
def get_log_path():
    year = datetime.now().year
    log_dir = os.path.join(DATA_DIR, "daily_logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"{year}.json")


# 初始化今天的健康目标（只在今天第一次调用时执行）
def initialize_today_health_goals():
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = get_log_path()

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = {}

    if today_str not in log_data:
        log_data[today_str] = {}

    if "health_goals" not in log_data[today_str]:
        log_data[today_str]["health_goals"] = [
            {"goal": item["goal"], "done": False}
            for item in health_goals
        ]
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)

    return log_data[today_str]["health_goals"]


# 获取今天的健康目标列表（不初始化，只读）
def get_today_health_goals():
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = get_log_path()

    # 如果日志文件不存在，先初始化
    if not os.path.exists(log_path):
        return initialize_today_health_goals()

    with open(log_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)

    # 如果今天还没有健康目标，也初始化
    if today_str not in log_data or "health_goals" not in log_data[today_str]:
        return initialize_today_health_goals()

    return log_data[today_str]["health_goals"]



# 更新某个目标的完成状态
def update_health_goal_status(goal_text: str, done: bool):
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = get_log_path()

    if not os.path.exists(log_path):
        return False

    with open(log_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)

    goals = log_data.get(today_str, {}).get("health_goals", [])
    for goal in goals:
        if goal["goal"] == goal_text:
            goal["done"] = done
            break
    else:
        return False  # 没找到目标

    log_data[today_str]["health_goals"] = goals
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    return True

# 新增：通过索引更新目标状态
def update_health_status(goal_index: int, done: bool):
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_path = get_log_path()

    if not os.path.exists(log_path):
        return False

    with open(log_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)

    goals = log_data.get(today_str, {}).get("health_goals", [])
    if 0 <= goal_index < len(goals):
        goals[goal_index]["done"] = done
        log_data[today_str]["health_goals"] = goals

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)

        return True
    return False

