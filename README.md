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
