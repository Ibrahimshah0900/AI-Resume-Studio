
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSETS_DIR = PROJECT_ROOT / "assets"
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
COMPONENTS_DIR = PROJECT_ROOT / "components"
UTILS_DIR = PROJECT_ROOT / "utils"
TESTS_DIR = PROJECT_ROOT / "tests"

SKILLS_DATA_DIR = DATA_DIR / "skills"
SAMPLE_RESUMES_DIR = DATA_DIR / "sample_resumes"
RESUME_DB_PATH = DATA_DIR / "resumes.db"

STYLES_DIR = ASSETS_DIR / "styles"
TEMPLATES_DIR = ASSETS_DIR / "templates"

def ensure_project_directories() -> None:
    directories = [
        ASSETS_DIR, DATA_DIR, MODELS_DIR, COMPONENTS_DIR,
        UTILS_DIR, TESTS_DIR, SKILLS_DATA_DIR, SAMPLE_RESUMES_DIR,
        STYLES_DIR, TEMPLATES_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_project_directories()
    print("Project directories verified successfully.")


# Auto-save settings
AUTO_SAVE_ENABLED = True
AUTO_SAVE_INTERVAL_SECONDS = 30  # Auto-save every 30 seconds
MAX_DRAFT_HISTORY = 20  # Maximum number of draft versions to keep
