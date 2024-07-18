import asyncio

from application_framework.service.service import Service


class Supervisor(Service):
    def __init__(self, loop, service_config):
        self.loop = loop
        self.service_config = service_config

    async def run_async(self):
        while True:
            print(f"[Supervisor] Hello from supervisor ({self.service_config.service_id})")
            await asyncio.sleep(1.0)
