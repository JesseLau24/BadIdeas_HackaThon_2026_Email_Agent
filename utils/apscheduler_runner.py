# utils/apscheduler_runner.py

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from main_runner import run_lazybomb                          # 👉 抓取 Gmail 并添加任务
from punishment_module.task_monitor import monitor_tasks     # 👉 检查哪些任务要提醒/惩罚
from punishment_module.reminder_engine import execute_reminders  # 👉 实际触发提醒 + 视频

def scheduled_run():
    """
    定时运行的任务，每 5 分钟执行一次：
      - 抓取新邮件并提取任务
      - 检查任务状态（提醒 + 惩罚）
    """
    print("🕒 APScheduler triggered. Running LazyBomb + Monitoring tasks...")
    
    # ✅ 1. 抓取新任务
    run_lazybomb()

    # ✅ 2. 检查哪些任务要提醒/惩罚
    reminder_tasks, strike_tasks = monitor_tasks()

    # ✅ 3. 执行提醒和惩罚动作
    execute_reminders(reminder_tasks, strike_tasks)

    print("✅ Scheduled run complete.\n")

def start_scheduler():
    """
    启动定时调度器：
      - 启动时立即运行一次
      - 之后每 5 分钟运行一次
    """
    scheduler = BlockingScheduler(timezone="UTC")  # 你也可以改成 "Europe/Riga" 等

    print("🚀 Running LazyBomb immediately at startup...")

    # ✅ 启动时先跑一次
    run_lazybomb()
    reminder_tasks, strike_tasks = monitor_tasks()
    execute_reminders(reminder_tasks, strike_tasks)

    print("🛡️ APScheduler is now running. LazyBomb will auto-run every 5 minutes.\n")

    # ✅ 每 5 分钟运行一次
    scheduler.add_job(
        scheduled_run,
        CronTrigger(minute="*/5"),
        id="lazybomb_periodic_job",
        replace_existing=True
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Scheduler stopped.")
