# ollama_module/ollama_agent.py

import requests

class OllamaAgent:
    def __init__(self, model_name: str = "phi4:14b"):
        self.model = model_name
        self.url = "http://localhost:11434/api/generate"

    def extract_tasks(self, email_body: str) -> str:
        """
        Send email body to local LLM via Ollama and return task JSON.
        """
        prompt = f"""
You are an intelligent assistant that extracts structured tasks from emails.

⚠️ First, determine if the email is a work-related message or a promotional/marketing email.

Ignore and return an empty list (`[]`) if the email is:
- A marketing or promotional message from services like Google, Microsoft, LinkedIn, etc.
- A newsletter, product announcement, webinar invite, survey request, or sales offer.
- Any automated message not directly asking the user to perform a specific work-related task.

Only proceed to extract tasks if the email clearly contains real, actionable work instructions.

From the email below, identify actionable tasks. For each task, return:
- "task": a clear description of the action to take
- "due_date": deadline in full ISO format "YYYY-MM-DDTHH:MM" if available, or null
- "priority": one of "high", "medium", "low", or null
- "assigner": the person or role who requested the task, or null
- "comments": any useful context, clarification, or assumptions
- "status": always set to "to do" by default

⚠️ Only split into separate tasks if the actions are logically independent.
E.g., "Prepare the report and upload it to Drive" should be one task.

⚠️ Use full ISO 8601 datetime format when the email includes a time (e.g., "July 10, 2 PM" → "2025-07-10T14:00").
If only the date is mentioned, use just "YYYY-MM-DD".

Output ONLY a valid JSON array. No markdown, no explanations, no comments.
Use double quotes for all keys and string values.
Do not include undefined or placeholder values like '2023-MM-DD'.

Here is the email:

{email_body}
"""

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        return result.get("response", "")
