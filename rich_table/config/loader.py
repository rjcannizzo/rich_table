import os
import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class AppConfig:
    username: str | None = None
    password: str | None = None


def get_user_config_file() -> Path:
    """Return OS-appropriate config file location."""
    home = Path.home()

    if os.name == "nt": # Windows
        return home / "AppData" / "Local" / "rich_table" / "config.json"
    elif os.uname().sysname == "Darwin": # macOS
        return home / "Library" / "Application Support" / "rich_table" / "config.json"
    else: # Linux and others
        return home / ".config" / "rich_table" / "config.json"


def load_config_file() -> dict:
    """Load config.json if it exists."""
    path = get_user_config_file()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            print("Warning: Invalid config file.")
    return {}


def load_config() -> AppConfig:
    """Load configuration from environment variables AND config file."""
    file_cfg = load_config_file()

    return AppConfig(
        username=os.getenv("Rich_Table_USERNAME") or file_cfg.get("username"),
        password=os.getenv("Rich_Table_PASSWORD") or file_cfg.get("password"),
    )