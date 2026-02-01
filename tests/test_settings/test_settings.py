import re
from pathlib import Path

from pic_back.settings import get_settings
from pic_back.shared import EnvType


def test_settings_values():
    pattern = r"^\d+\.\d+\.\d+$"

    settings = get_settings()

    assert settings.environment == EnvType.TEST
    assert settings.database_base_path == Path("./tests/data")
    assert re.match(pattern, settings.version)
