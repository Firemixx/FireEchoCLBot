import os
from pathlib import Path
from dotenv import load_dotenv
from fluentogram import TranslatorHub
from fluentogram.storage.file import FileStorage

env_path = Path(__file__).resolve().parents[2] / "Storage" / ".env"
loc_path = Path(__file__).resolve().parents[2] / "Storage" / "Localization"

hub: TranslatorHub = None


async def init():
    global hub

    load_dotenv(env_path)

    storage = FileStorage(str(loc_path))

    locales_map = {
        "en": "en",
        "uk": "uk",
        "ru": "ru",
    }

    hub = TranslatorHub(
        locales_map=locales_map,
        storage=storage
    )


async def get_loc(key: str, **kwargs) -> str:
    locale = os.getenv("LOCALIZATION")

    translator = hub.get_translator_by_locale(locale)

    return translator.get(key, **kwargs)