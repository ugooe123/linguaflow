import os
import json

DEFAULT_CONFIG = {
    "api_base": "https://api.openai.com/v1",
    "model": "gpt-4o-mini",
    "temperature": 0.3,
    "target_languages": ["zh-CN", "ja", "ko", "es", "pt-BR"],
    "max_retries": 3,
}

CONFIG_FILE = os.path.expanduser("~/.linguaflow.json")
PROJECT_CONFIG_FILE = ".linguaflow.json"


def load_global_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return dict(DEFAULT_CONFIG)


def save_global_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_project_config(path="."):
    cfg_path = os.path.join(path, PROJECT_CONFIG_FILE)
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            return json.load(f)
    return {}


def save_project_config(config, path="."):
    cfg_path = os.path.join(path, PROJECT_CONFIG_FILE)
    with open(cfg_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key():
    key = os.getenv("LINGUAFLOW_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        cfg = load_global_config()
        key = cfg.get("api_key", "")
    return key