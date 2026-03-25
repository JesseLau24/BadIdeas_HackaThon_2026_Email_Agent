# utils/html_generator.py

import json
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from utils.constants import TASKS_JSON_PATH

def generate_task_html_from_json(json_path=TASKS_JSON_PATH, output_path='download/tasklist_static.html'):
    # ✅ 1. 加载任务 JSON
    with open(json_path, encoding='utf-8') as f:
        tasks = json.load(f)

    # ✅ 2. 按日期归组（tasks_by_date[date_str] -> list of tasks）
    tasks_by_date = defaultdict(list)
    for task in tasks:
        date_key = (task.get("due_date") or "No Deadline")[:10]
        tasks_by_date[date_key].append(task)

    # ✅ 3. 初始化 Jinja2 模板引擎
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('tasklist_static.html.j2')

    # ✅ 4. 渲染 HTML 内容
    rendered_html = template.render(
        tasks_by_date=dict(tasks_by_date),
        export_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        statuses=["to do", "I'm on it", "finished", "deleted"]
    )

    # ✅ 5. 写入 HTML 文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"[✅] Static HTML snapshot exported to: {output_path}")


if __name__ == "__main__":
    generate_task_html_from_json()
