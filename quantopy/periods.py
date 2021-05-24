from enum import Enum, auto


class Period(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    SEMIANNUAL = auto()
    YEARLY = auto()


annualization_factor = {
    Period.DAILY: 252,
    Period.WEEKLY: 52,
    Period.MONTHLY: 12,
    Period.QUARTERLY: 4,
    Period.SEMIANNUAL: 2,
    Period.YEARLY: 1,
}
