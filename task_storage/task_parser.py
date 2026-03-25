# task_storage/task_parser.py

import re
import json
from typing import Optional, List, Dict

try:
    import demjson3
except ImportError:
    demjson3 = None  # if demjson3 not installed, disable auto-fix feature

def fix_priority_quotes(json_str: str) -> str:
    """
    Add double quotes to priority field values, assuming only high/medium/low are possible options.
    """
    return re.sub(r'"priority":\s*(high|medium|low)', r'"priority": "\1"', json_str)

def normalize_deadline_fields(task_list: List[Dict]) -> List[Dict]:
    """
    Ensure all tasks use 'deadline' as the standard field.
    If 'due_date' exists and 'deadline' doesn't, copy its value to 'deadline'.
    """
    for task in task_list:
        if "due_date" in task and "deadline" not in task:
            task["deadline"] = task["due_date"]
    return task_list

def extract_task_list_from_output(output_text: str, debug: bool = False) -> Optional[List[Dict]]:
    """
    Extract a JSON list of tasks from model output.
    Supports Markdown-wrapped ```json ... ``` and fallback recovery.
    If parsing fails, attempts to auto-fix using demjson3 (if available).
    """
    json_str = None

    # ✅ First, try to extract the ```json ... ``` block
    match = re.search(r"```json\s*([\s\S]+?)\s*```", output_text)
    if match:
        json_str = match.group(1).strip()
    else:
        # ⛳ Fallback attempt: bare JSON array structure
        match = re.search(r"\[\s*{[\s\S]+?}\s*\]", output_text)
        if match:
            json_str = match.group(0).strip()
        else:
            # ⛳ Final attempt: parse the entire raw text
            json_str = output_text.strip()

    # Try using standard expression to fix priority field bare values
    json_str = fix_priority_quotes(json_str)
    if debug:
        print("🔍 JSON string after fixing priority quotes:")
        print(json_str)

    # ✅ First, try to parse using standard JSON
    try:
        parsed = json.loads(json_str)
        if isinstance(parsed, list):
            return normalize_deadline_fields(parsed)  # ✅ 标准化字段
        if debug:
            print("⚠️ Parsed result is not a list.")
        return None
    except json.JSONDecodeError as e:
        if debug:
            print(f"⚠️ JSON decode error: {e}")

    # 🔧 Try using demjson3 to auto-fix parsing
    if demjson3:
        if debug:
            print("🔧 Trying to auto-fix JSON using demjson3...")
        try:
            parsed = demjson3.decode(json_str)
            if isinstance(parsed, list):
                if debug:
                    print("✅ Auto-fix succeeded.")
                return normalize_deadline_fields(parsed)  # ✅ 标准化字段
            if debug:
                print("⚠️ Auto-fix result is not a list.")
        except Exception as demjson_err:
            if debug:
                print(f"❌ demjson3 failed: {demjson_err}")
    else:
        if debug:
            print("⚠️ demjson3 not available. Run `pip install demjson3` to enable auto-fix.")

    return None
