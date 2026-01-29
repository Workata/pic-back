from enum import Enum


class TimeSeconds(Enum):
    MINUTE = 60
    HOUR = MINUTE * 60
    HALF_DAY = 12 * HOUR
    DAY = 24 * HOUR
    TWO_DAYS = 2 * DAY
    WEEK = 7 * DAY
