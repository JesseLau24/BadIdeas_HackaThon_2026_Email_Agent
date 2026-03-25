from cli_agent.core import run_cli_agent

EMAIL = "lazybomb1024@gmail.com"
APP_PASSWORD = "tmzb bqxm kcsp tihv"
IMAP_SERVER = "imap.gmail.com"
TASKS_PATH = "data/tasks.json"
LAST_PROCESSED_JSON_PATH = "data/last_processed.json"

if __name__ == "__main__":
    run_cli_agent(EMAIL, APP_PASSWORD, IMAP_SERVER, TASKS_PATH, LAST_PROCESSED_JSON_PATH)