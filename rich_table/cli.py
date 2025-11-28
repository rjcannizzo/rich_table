from rich_table.config.loader import load_config
from rich_table.main import show


def main() -> None:
    """Entry point for the 'rich-table' console script."""
    config = load_config()
    show(config)


if __name__ == "__main__":
    main()
