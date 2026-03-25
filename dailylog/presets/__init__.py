import json
from utils.constants import PRESET_HEALTH_GOALS_PATH, PRESET_HAPPINESS_TASKS_PATH

# 加载 preset 健康目标
with open(PRESET_HEALTH_GOALS_PATH, "r", encoding="utf-8") as f:
    health_goals = json.load(f)

# 加载 preset 快乐任务
with open(PRESET_HAPPINESS_TASKS_PATH, "r", encoding="utf-8") as f:
    happiness_activities = json.load(f)
