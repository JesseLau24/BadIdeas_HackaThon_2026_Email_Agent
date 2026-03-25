# utils/constants.py

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 数据文件夹
DATA_DIR = os.path.join(BASE_DIR, "data")

# 各类 JSON 文件路径
TASKS_JSON_PATH = os.path.join(DATA_DIR, "tasks.json")
LAST_PROCESSED_JSON_PATH = os.path.join(DATA_DIR, "last_processed.json")
STRIKE_LOG_PATH = os.path.join(DATA_DIR, "strike_log.json")

# ✅ 统一提醒 + 惩罚视频文件夹路径
ALERT_VIDEO_DIR = os.path.join(BASE_DIR, "assets", "alerts")

# ✅ 支持的视频扩展名
ALERT_VIDEO_EXT = ".mp4"

# Preset 模板路径
PRESET_HEALTH_GOALS_PATH = os.path.join(BASE_DIR, "dailylog", "presets", "health_goals.json")
PRESET_HAPPINESS_TASKS_PATH = os.path.join(BASE_DIR, "dailylog", "presets", "happiness_activities.json")

# ✅ 每日健康目标和乐趣任务用户上传内容路径
DAILY_LOG_FILE_TEMPLATE = os.path.join(DATA_DIR, 'daily_logs', '{year}.json')

# ✅ 图片存储路径
IMAGE_DIR = os.path.join("static", "images")