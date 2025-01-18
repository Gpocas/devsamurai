from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, env_file_encoding='utf-8'
    )

    CSV_PATH: Path = BASE_DIR / 'aulas.csv'
    DOWNLOAD_PATH: Path = BASE_DIR / 'downloads'
