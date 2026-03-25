# punishment_module/reminder_engine.py

from punishment_module.notifier import show_popup_notification
from punishment_module.meme_player import play_random_alert_video


def execute_reminders(reminder_tasks, strike_tasks):
    """
    接收需要提醒和惩罚的任务列表，并统一处理提醒动作。
    """
    if reminder_tasks or strike_tasks:
        show_popup_notification(reminders=reminder_tasks, strikes=strike_tasks)
        play_random_alert_video()
