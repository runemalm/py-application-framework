from enum import Enum


class RestartStrategy(Enum):
    IMMEDIATE = 'Immediate'
    FIXED_BACKOFF = 'FixedBackoff'
    EXPONENTIAL_BACKOFF = 'ExponentialBackoff'
    LINEAR_BACKOFF = 'LinearBackoff'
    CUSTOM_BACKOFF = 'CustomBackoff'
