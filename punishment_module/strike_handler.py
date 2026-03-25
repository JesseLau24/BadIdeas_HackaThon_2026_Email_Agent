# punishment_module/strike_handler.py

import json
import os
from datetime import datetime, timedelta
from typing import Dict
from utils.constants import STRIKE_LOG_PATH
from punishment_module.meme_player import play_random_alert_video  # ✅ 使用统一播放接口

def check_and_strike(task: Dict):
    """
    执行社死惩罚：
    - 随机播放提醒/惩罚视频（.mp4）
    - 记录 strike_log.json
    """
    print(f"💀 STRIKE INITIATED for task: {task.get('task')}")

    # 播放视频（惩罚/提醒统一处理）
    play_random_alert_video()

    # 记录惩罚日志
    record_strike(task)

def record_strike(task: Dict):
    """
    将被罚任务记录到 data/strike_log.json，避免重复记录（1小时内）。
    """
    record = {
        "task": task.get("task"),
        "deadline": task.get("deadline") or task.get("due_date"),
        "status": task.get("status"),
        "strike_time": datetime.now().isoformat()
    }

    log = []
    if os.path.exists(STRIKE_LOG_PATH):
        try:
            with open(STRIKE_LOG_PATH, "r", encoding="utf-8") as f:
                log = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to read existing strike log: {e}")

    # ✅ 检查是否已在1小时内被记录过
    now = datetime.now()
    for entry in log[::-1]:  # 逆序查找最新记录更快
        if entry.get("task") == record["task"]:
            try:
                last_time = datetime.fromisoformat(entry["strike_time"])
                if now - last_time < timedelta(hours=1):  # ✅ 阈值可改（如 5 分钟）
                    print("⏳ Strike already recorded recently. Skipping.")
                    return
            except Exception as e:
                print(f"⚠️ Error parsing strike_time: {e}")

    log.append(record)

    try:
        with open(STRIKE_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
        print(f"✅ Strike recorded in {STRIKE_LOG_PATH}")
    except Exception as e:
        print(f"❌ Failed to write strike log: {e}")
