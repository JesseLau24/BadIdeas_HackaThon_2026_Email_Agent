import subprocess
from task_storage.task_parser import extract_task_list_from_output

def call_ollama(prompt, model="phi4:14b"):
    """
    Call a local Ollama LLM to process a given prompt.

    Parameters:
        prompt (str): The text prompt to send to the model.
        model (str): The Ollama model name to use (default "phi4:14b").

    Returns:
        str: The model's stdout output as a string, stripped of extra spaces.
             Returns empty string if an error occurs or output is empty.

    Notes:
        - Uses subprocess.run to invoke the local Ollama CLI.
        - Ensures proper UTF-8 handling and replaces problematic characters.
        - Prints any stderr from the model for debugging purposes.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],  # Run Ollama CLI with specified model
            input=prompt,              # Send prompt via stdin
            stdout=subprocess.PIPE,    # Capture stdout
            stderr=subprocess.PIPE,    # Capture stderr for debugging
            text=True,                 # Treat I/O as text
            encoding="utf-8",          # Decode bytes as UTF-8
            errors="replace"           # Replace undecodable characters
        )
        if result.stderr.strip():
            print("🔹 Ollama stderr:", result.stderr.strip())  # Show model warnings/errors
        output = result.stdout
        return output.strip() if output else ""  # Return stripped output or empty string
    except Exception as e:
        print(f"❌ Ollama subprocess error: {e}")
        return ""  # Return empty string on exception

def extract_tasks_from_email(email_body: str):
    """
    Extract structured tasks from the body of an email using an LLM.

    Parameters:
        email_body (str): Raw plain-text email content.

    Returns:
        list[dict]: A list of task dictionaries, each containing:
            - task: Task description
            - due_date: Optional due date (ISO format)
            - priority: Low/medium/high
            - assigner: Person who assigned the task
            - comments: Additional information
            - status: Task status (default "to do")
            - deadline: Optional deadline (ISO format)
            - email_content: Original email text
            - id: Unique identifier for the task (UUID)
            - source: Source of the task ("email")

    Notes:
        - Builds a prompt that instructs the LLM to output a JSON list.
        - Calls `call_ollama` to get the LLM's response.
        - Parses the JSON safely using `extract_task_list_from_output`.
        - Prints a warning if parsing fails or no tasks are returned.
        - Ensures that only a valid JSON list is returned; never returns None.
    """
    prompt = f"""
Extract all tasks from the following email and output as a JSON list.
Each task must have the following fields (fill with available info; empty string if unknown):

[
  {{
    "task": "task description",
    "due_date": "YYYY-MM-DDTHH:MM",
    "priority": "low/medium/high",
    "assigner": "name",
    "comments": "any additional details",
    "status": "to do",
    "deadline": "YYYY-MM-DDTHH:MM",
    "email_content": "{email_body.replace('"','\\"')}",
    "id": "generate a uuid4 string",
    "source": "email"
  }}
]

Only output valid JSON list. Do not include extra text.
"""
    output_text = call_ollama(prompt)  # Send the prompt to the model
    if not output_text:
        return []  # Return empty list if model produced no output

    # Parse the JSON list returned by the model into Python dicts
    tasks = extract_task_list_from_output(output_text, debug=True)
    if not tasks:
        print("⚠️ Failed to parse Ollama output.")  # Warn if parsing fails
        return []
    # ✅ Fill due_date using deadline if due_date is missing
    for task in tasks:
        if (not task.get("due_date")) and task.get("deadline"):
            task["due_date"] = task["deadline"]

    return tasks  # Return the list of extracted task dictionaries