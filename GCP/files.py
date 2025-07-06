import os

# Define the folder structure and files to create (empty)
structure = [
    "app/__init__.py",
    "app/ui.py",
    "app/chat.py",
    "config/__init__.py",
    "config/settings.py",
    "main.py",
    ".env",
    "requirements.txt",
    "README.md"
]

# Create folders and empty files
for path in structure:
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(path, "w", encoding="utf-8") as f:
        pass  # Just create empty files

print("✅ Folder structure created with empty files.")
