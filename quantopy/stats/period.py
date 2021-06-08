from enum import (
    Enum,
    auto,
)


class period(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    SEMIANNUAL = auto()
    YEARLY = auto()


annualization_factor = {
    period.DAILY: 252,
    period.WEEKLY: 52,
    period.MONTHLY: 12,
    period.QUARTERLY: 4,
    period.SEMIANNUAL: 2,
    period.YEARLY: 1,
}
