# Introduction

A small example project to demonstrate: packaging a Python app with non-Python assets, configuration management, and a clean CLI / package layout.  
Inspired by learning best-practices for real-world Python application packaging and configuration.

Repository: [https://github.com/rjcannizzo/rich_table.git](https://github.com/rjcannizzo/rich_table.git)

---

## 🚀 Installation & Running

### Install locally for your user

From the root of the project (where `pyproject.toml` lives), run:

```bash
pip install --user .
````

This will install the package into your user Python site-packages and install the `rich-table` console command.  
Once installed, you can run:

```bash
rich-table
```

Alternatively, to install in **editable mode** (for active development):

```bash
pip install --user -e .
```

This way, any changes you make to the source files (Python or assets) are immediately visible when you run the command — no reinstall needed.

---

### Run as a package (without installing)

If you prefer or for testing, you can run directly from the source folder:

```bash
python -m rich_table
```

This uses the package’s `__main__.py` entry point, which delegates to the same CLI logic.

---

## 📦 Packaging Design & Concepts

This project demonstrates several important packaging and configuration design patterns.

### ✅ Including non-Python files (assets, data, etc.)

Because the package includes non-Python files (e.g., CSS files, note/data files under `css/`, `notes/`), we configured `pyproject.toml` so that setuptools will bundle these with the package:

```toml
[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
include = ["rich_table*"]

[tool.setuptools.package-data]
"rich_table" = ["css/**/*", "notes/**/*"]
```

- `include-package-data = true` tells setuptools to pay attention to package data definitions.
  
- The `package-data` section uses glob patterns (`**/*`) to include all files under subdirectories.
  
- This ensures that when the package is installed (via pip), these asset files are present in `site-packages/rich_table/css` and `.../notes`, so that code referencing them works properly.
  

This pattern scales well even if you later add many more assets (images, templates, data files, etc.) — no need to manually list every file.

---

### 🔐 Configuration Layer & Separation

Rather than hard-coding configuration (credentials, options, etc.) into code or relying on relative paths, the project uses a **dedicated configuration loader** under `rich_table/config/loader.py`.

Key points:

- Config is loaded from a **user-level config file** (e.g. on Windows: `C:\Users\<user>\AppData\Local\rich_table\config.json`; on Linux: `~/.config/rich_table/config.json`; on macOS: `~/Library/Application Support/rich_table/config.json`) — or from environment variables.
  
- This loader returns a simple `AppConfig` dataclass with credentials or settings.
  
- The application logic (`main.py`) takes the `config` object as an argument, and never reads environment variables directly.
  
- This design cleanly separates **configuration**, **bootstrap logic**, and **application logic**, which avoids exposing secrets in the source tree or in installed package, and ensures portability.
  

---

### 🧩 CLI vs Package Layout

The repository uses the common—and recommended—pattern for Python applications:

```
rich_table/              ← project root (contains pyproject.toml, README, etc.)
└── rich_table/          ← actual Python package
     ├── __init__.py
     ├── __main__.py     ← enables `python -m rich_table`
     ├── cli.py          ← console entry point for installed command
     ├── main.py         ← application logic
     ├── config/         ← config loader & schema
     ├── css/            ← non-Python asset files
     └── notes/          ← additional data or text files
```

This layout provides several advantages:

- Clean namespace separation: your importable package is inside `rich_table/`.
  
- Multiple entry points:
  
  - `rich-table` — installed console script, via `cli.py`
    
  - `python -m rich_table` — package mode, via `__main__.py`
    
- Easy development: `pip install -e .` lets you modify code and rerun immediately without reinstalling.
  
- Maintainability: assets and config live alongside package code, yet packaged properly.
  

---

## ✅ Summary

The `rich_table` project is a small but real-world-like example of how to build, package, and distribute a Python application which:

- Has a CLI entry point
  
- Supports direct “run from source” via `python -m ...`
  
- Includes non-Python assets (CSS, notes, etc.)
  
- Supports user or environment-based configuration
  
- Is structured so config and code are cleanly separated
  

If you clone or fork the repo:

```
git clone https://github.com/rjcannizzo/rich_table.git
cd rich_table
pip install --user -e .
rich-table
```

You should see the example table output using your config (if available).