import re

from pic_back.settings import get_settings


def test_settings_values():
    pattern = r"^\d+\.\d+\.\d+$"

    settings = get_settings()

    assert re.match(pattern, settings.version)
