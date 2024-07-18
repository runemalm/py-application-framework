import asyncio
import time

from application_framework.service.service import Service
from examples.single_app.config import AppConfig


class Application(Service):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config

    def run(self):
        """Run the application synchronously."""
        while True:
            print(f"[Application] Hello from application")
            time.sleep(1.0)

    async def run_async(self):
        while True:
            print(f"[Application] Hello from application")
            await asyncio.sleep(1.0)
