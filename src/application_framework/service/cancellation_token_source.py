import asyncio
import threading

from application_framework.service.cancellation_token import CancellationToken


class CancellationTokenSource:
    def __init__(self, is_async):
        if is_async:
            self._token = CancellationToken(asyncio.Event())
        else:
            self._token = CancellationToken(threading.Event())

    @property
    def token(self):
        return self._token

    def cancel(self):
        self._token.cancel()
