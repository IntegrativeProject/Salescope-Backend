import os

# Folders and files structure
structure = {
    "backend": {
        "app": {
            "__init__.py": "",
            "main.py": "",
            "config.py": "",
            "database.py": "",
            "models": {
                "__init__.py": ""
            },
            "routers": {
                "__init__.py": ""
            },
            "schemas": {
                "__init__.py": ""
            },
            "services": {
                "__init__.py": ""
            },
            "analysis": {
                "__init__.py": ""
            },
        },
        ".env": "",
        "requirements.txt": "",
        "README.md": "",
        "run.py": ""
    }
}

# Recursive function to create folders and files
def create_structure(base_path, data):
    for name, content in data.items():
        path = os.path.join(base_path, name)

        # If it's a dict → folder
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Otherwise create file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# Start creating structure
create_structure(".", structure)

print("✔ Structure created successfully.")
