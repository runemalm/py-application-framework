import time
import asyncio
from application_framework.service.service import Service
from examples.single_app.config import AppConfig
from application_framework.messaging.message import Message


class Application(Service):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self.crashed = False

    def run(self):
        self.crashed = False
        while not self.stop_event.is_set():
            if self.crashed:
                print(f"[Application] Application has crashed!")
                time.sleep(1.0)
            else:
                try:
                    print(f"[Application] Hello from application")
                    time.sleep(1.0)
                    # await self.channels.service_to_supervisor.send_async(
                    #     Message(sender=self.service_id, content="dummy"),
                    #     self.loop,
                    # )
                except Exception as e:
                    self.crashed = True
                    self.channels.service_to_supervisor.send(
                        Message(sender=self.service_id, content="crashed")
                    )
        print(f"[Application] Application was instructed to stop")
        self.channels.service_to_supervisor.send(
            Message(sender=self.service_id, content="stopped")
        )

    async def run_async(self):
        self.crashed = False
        while not self.stop_event.is_set():
            if self.crashed:
                print(f"[Application] Application has crashed!")
                await asyncio.sleep(1.0)
            else:
                try:
                    print(f"[Application] Hello from application")
                    await asyncio.sleep(1.0)
                    # await self.channels.service_to_supervisor.send_async(
                    #     Message(sender=self.service_id, content="dummy"),
                    #     self.loop,
                    # )
                except Exception as e:
                    self.crashed = True
                    await self.channels.service_to_supervisor.send_async(
                        Message(sender=self.service_id, content="crashed"),
                        self.loop,
                    )
        print(f"[Application] Application was instructed to stop")
        await self.channels.service_to_supervisor.send_async(
            Message(sender=self.service_id, content="stopped"),
            self.loop,
        )
