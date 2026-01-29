from pic_back.shared import TimeSeconds


def test_time_seconds_values():
    assert TimeSeconds.MINUTE.value == 60
    assert TimeSeconds.HOUR.value == 60 * 60
    assert TimeSeconds.HALF_DAY.value == 12 * 60 * 60
    assert TimeSeconds.DAY.value == 24 * 60 * 60
    assert TimeSeconds.TWO_DAYS.value == 2 * 24 * 60 * 60
    assert TimeSeconds.WEEK.value == 7 * 24 * 60 * 60
