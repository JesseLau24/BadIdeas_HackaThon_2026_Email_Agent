# main_runner.py

from gmail_module.gmail_reader import GmailReader
from utils.timestamp_utils import read_last_processed_timestamp, write_last_processed_timestamp
from ollama_module.ollama_agent import OllamaAgent
from task_storage.task_writer import append_tasks
from task_storage.task_parser import extract_task_list_from_output
from utils.html_generator import generate_task_html_from_json
from utils.constants import TASKS_JSON_PATH, LAST_PROCESSED_JSON_PATH  # ✅ 使用统一路径
import uuid

from datetime import timezone
import json
import os

# 👉 Environment Variable Control -- Debug Mode
DEBUG_MODE = os.environ.get("LAZYBOMB_DEBUG", "0") == "1"

# 👉 Email credentials (consider securing via .env in the future)
EMAIL = "lazybomb1024@gmail.com"
PASSWORD = "tmzb bqxm kcsp tihv"

def run_lazybomb():
    # ✅ 初始化 Gmail 连接
    reader = GmailReader(EMAIL, PASSWORD)
    reader.connect()

    # ✅ 初始化 LLM 代理
    ollama = OllamaAgent()

    # ✅ 加载上次处理的时间戳
    last_time = read_last_processed_timestamp(LAST_PROCESSED_JSON_PATH)
    print(f"📅 Last processed time (UTC): {last_time.isoformat()}")

    # ✅ 抓取新邮件（过滤掉之前处理过的）
    emails = reader.fetch_new_email_bodies_since(last_time)

    for i, (body, timestamp) in enumerate(emails):
        print(f"\n📨 Email #{i+1} @ {timestamp.isoformat()} UTC:")
        print(body[:300], "...")  # 预览邮件内容

        # ✅ 调用大模型抽取任务
        response = ollama.extract_tasks(body)
        print("🤖 Extracted Task JSON:")
        print(response)

        # ✅ 解析任务
        tasks = extract_task_list_from_output(response, debug=DEBUG_MODE)
        if tasks:
            for task in tasks:
                task["email_content"] = body
                task["id"] = str(uuid.uuid4())  # ✅ 添加唯一 task ID
            append_tasks(tasks, filename=TASKS_JSON_PATH)

        else:
            print("⚠️ Failed to extract valid task list from model output")

    # ✅ 更新时间戳
    if emails:
        latest_timestamp = emails[-1][1]
        write_last_processed_timestamp(latest_timestamp, LAST_PROCESSED_JSON_PATH)

    # ✅ 登出 Gmail
    reader.logout()

    # 📝 静态 HTML 生成逻辑保留注释状态
    # generate_task_html_from_json(
    #     json_path=TASKS_JSON_PATH,
    #     output_path='tasklist.html'
    # )
