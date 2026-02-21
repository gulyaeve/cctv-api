import tomllib
from pathlib import Path

# Load pyproject.toml
path = Path(__file__).parent.parent / "pyproject.toml"
with open(path, "rb") as f:
    data = tomllib.load(f)

# Extract version from [project] or [tool.poetry]
version = data.get("project", {}).get("version")

if __name__ == "__main__":
    print(version)

