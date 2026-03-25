# 🤖 LazyBomb CLI Agent (for BadIdeas Hackathon 2026)

Welcome to the slightly chaotic, mildly rebellious, and surprisingly effective **LazyBomb CLI Agent** 🚀

This tool is a command-line based productivity assistant that:

* 📬 Fetches emails via IMAP
* 🧠 Uses a local LLM (via Ollama) to extract actionable tasks
* 📝 Stores and deduplicates tasks
* ⚡ Summarizes and highlights urgent work

All without relying on expensive cloud APIs (because… well… we’re broke students 😅)

Therefore, you must have Ollama installed on your local device and download Phi4:14B model.

(if you want to change models, go to "cli_agent\ai_utils.py")

---

## 🧩 Project Structure

The CLI Agent is organized into a modular package for clarity and maintainability:

### `cli_agent/`

Main package containing the core logic.

* **`core.py`**

  * The main CLI loop
  * Orchestrates everything: email fetching → task extraction → storage → AI summary

* **`email_utils.py`**

  * Handles IMAP connection and email fetching
  * Extracts subject, sender, body, and timestamps
  * Filters emails based on `last_processed.json`

* **`ai_utils.py`**

  * Communicates with the local LLM (Ollama)
  * Converts raw email text into structured JSON tasks
  * Includes a small but critical fallback to stabilize missing fields (because LLMs have… personality)

---

### External Modules

* **`task_storage/`**

  * `task_writer.py`: Appends tasks into `data/tasks.json`
  * `task_parser.py`: Safely parses LLM output into structured JSON

---

### Data Files

* `data/tasks.json` → Stores all extracted tasks
* `data/last_processed.json` → Tracks last processed email timestamp
* `data/strikes.json` → (Optional) Punishment/discipline system 😈

---

## ⚙️ How It Works

1. User runs the CLI
2. Agent fetches recent emails
3. LLM extracts tasks from email content
4. Tasks are deduplicated and saved
5. AI summarizes current workload and highlights urgency

---

## ☁️ About Cloud Models (a brave side quest)

One of our teammates is currently exploring the possibility of using **cloud-based LLM APIs** 👀

However:

* We have **very limited experience with API-based models**
* Also… budget constraints exist (instant noodles are already expensive enough)

Due to time limitations, we were **unable to integrate the cloud-based version into this repository**.
So for now, this project focuses entirely on **local model execution (Ollama)**.

---

## ⚖️ A Note to the Judges (with honesty and a bit of guilt)

This project builds upon a previous assignment of ours.

We did ask whether this was allowed, and the answer was *yes* —
but we still feel slightly morally conflicted about it 😅

So we’d like to acknowledge that:

> This may give us a small structural advantage compared to teams starting fully from scratch.

We kindly ask you to **take this into consideration during evaluation**,
as fairness matters more to us than squeezing out a few extra points 🙏

---

## 🎯 Final Thoughts

This project is:

* A mix of practicality and experimentation
* Slightly duct-taped in places
* Surprisingly functional

And most importantly:

> Built with curiosity, caffeine, and just enough chaos to make it fun ☕💻

---

Thanks for checking it out ❤️
 
 
 =========
 Here is the original ReadMe:
 =========
 
 # 🚀 How to Run LazyBomb Locally

## 📦 One-Time Setup
Activate your virtual environment

For Linux:
```Terminal
source /home/jesse/Projects/myenvs/lazybomb/bin/activate
```
For Windows:
```
& "C:\Users\jesse\Projects\MyEnvs\test\Scripts\Activate.ps1"
```
For Mac:
```
I don't know, I don't own a Mac
```

Adjust the path if your virtual environment is elsewhere.

Install required dependencies if you haven't (or the service won't run)
```PowerShell
pip install -r requirements.txt
```
**Recommended Python version: 3.12**

| Package            | Version   |
|--------------------|-----------|
| APScheduler        | 3.11.0    |
| blinker            | 1.9.0     |
| certifi            | 2025.6.15 |
| charset-normalizer | 3.4.2     |
| click              | 8.2.1     |
| colorama           | 0.4.6     |
| demjson3           | 3.0.6     |
| Flask              | 3.1.1     |
| flask-cors         | 6.0.1     |
| idna               | 3.10      |
| itsdangerous       | 2.2.0     |
| Jinja2             | 3.1.6     |
| MarkupSafe         | 3.0.2     |
| numpy              | 2.3.1     |
| requests           | 2.32.4    |
| tzdata             | 2025.2    |
| tzlocal            | 5.3.1     |
| urllib3            | 2.5.0     |
| Werkzeug           | 3.1.3     |

**Dependencies pinned in requirements.txt:**

For Linux and macOS, make sure python-tk or python3-tk is installed, otheriwise, "/punishment_module/notifier.py" module won't work properly.

```PowerShell
sudo apt-get install python3-tk
```

or for macOS (I am not sure. I don't own a Mac)
```PowerShell
brew install python-tk
```
**Ollama must be installed locally.**

You need to download the model "phi4:14b" via Ollama, or configure the model version manually in "ollama_module/ollama_agent.py" if you want to use other Ollama agents.

## 🧠 Step-by-Step Run Instructions
1. Start the Flask API Server
In your project root (LazyBomb/), open a terminal (make sure venv is activated), and run:

```PowerShell
python3 task_status_api.py
(or python task_status_api.py)
```

This starts the backend Flask server at http://127.0.0.1:5000. (or http://localhost:5000)

2. Open the Task Page in Browser
Visit this URL in your browser:

http://localhost:5000

You’ll see your interactive task list.

4. Update Task Status from the Page
Each task has a dropdown menu to update its status.
When changed, the page will send a POST request to:

http://localhost:5000/update_status

The updated status will be written back into the tasks.json file.
(PS: it would only update the "tasks.json" file, the "tasklist.html" would only be updated when the html_generator.py run again)

# 🛠️ Development Tips
CORS Configuration
The Flask server must allow requests from http://localhost:8000.

Make sure flask_cors is installed and used in task_status_api.py.

Activate Virtual Env
For both terminals, activate the virtual environment before running anything.

Refresh to See Updates
The status is saved in tasks.json. Reload the page to see the latest from disk.

When "html_generator.py" activates again, the "tasklist.html" would be updated again.

Check Logs
Use browser developer tools (F12) to view console and network errors if things break.

# 📝 Regenerate HTML Task Page
If you added new tasks and want to regenerate the HTML:

```PowerShell
python3 utils/html_generator.py
```

This updates tasklist.html with the latest tasks from tasks.json.



-------------------
# Debug Mode for LazyBomb

This guide explains how to enable debug mode for LazyBomb and where to find debug output files when JSON parsing from the model output fails.

## How to Enable Debug Mode

Set the environment variable `LAZYBOMB_DEBUG=1` before running the script. The exact command depends on your terminal:

### On Windows CMD (Command Prompt)

```cmd
set LAZYBOMB_DEBUG=1
python main.py
```


### On PowerShell

```PowerShell
$env:LAZYBOMB_DEBUG=1
python main.py
```

### On Git Bash, WSL, Linux, or macOS Terminal

```bash
export LAZYBOMB_DEBUG=1
python main.py
```

# Where to find the Debug File

If JSON parsing fails, debug information will be saved to: debug_output.txt

This file is located in the project root directory

# What Does the Debug File Contain?

The original model output or extracted JSON snippet

Error details including JSON decode errors

This helps diagnose why task extraction failed.
