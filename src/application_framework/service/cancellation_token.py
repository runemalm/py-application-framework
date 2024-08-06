import asyncio

class CancellationToken:
    def __init__(self, event):
        self._is_cancellation_requested = False
        self._event = event

    @property
    def is_cancellation_requested(self):
        return self._is_cancellation_requested

    async def wait_cancellation_async(self):
        if isinstance(self._event, asyncio.Event):
            await self._event.wait()
        else:
            while not self._event.is_set():
                await asyncio.sleep(0.1)

    def cancel(self):
        self._is_cancellation_requested = True
        self._event.set()
