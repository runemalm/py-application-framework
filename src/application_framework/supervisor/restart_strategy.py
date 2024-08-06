class RestartStrategy:
    IMMEDIATE = 'Immediate'
    FIXED_BACKOFF = 'FixedBackoff'
    EXPONENTIAL_BACKOFF = 'ExponentialBackoff'
    LINEAR_BACKOFF = 'LinearBackoff'

    def __init__(self, strategy=EXPONENTIAL_BACKOFF, fixed_backoff_time=5, max_backoff_time=60, max_jitter=5):
        self.strategy = strategy
        self.fixed_backoff_time = fixed_backoff_time
        self.max_backoff_time = max_backoff_time
        self.max_jitter = max_jitter
