from enum import StrEnum

class Currency(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"

class Status(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"