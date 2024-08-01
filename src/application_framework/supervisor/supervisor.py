import asyncio

from application_framework.actor.actor import ActorBase
from application_framework.messaging.message import Message


class Supervisor(ActorBase):
    def __init__(self, loop, service_id, channels):
        super().__init__()
        self.loop = loop
        self.service_id = service_id
        self.channels = channels
        self.host_listener_task = None
        self.service_listener_task = None
        self.starting_event = asyncio.Event()
        self.stopping_event = asyncio.Event()
        self.stopped_event = asyncio.Event()
        self.crashed_event = asyncio.Event()

    async def start_async(self, stop_event):
        self.stop_event = stop_event
        self.host_listener_task = self.loop.create_task(self.run_host_listener_async())
        self.service_listener_task = self.loop.create_task(self.run_service_listener_async())
        await self.run_async()

    async def stop_async(self):
        self.stop_event.set()

    async def run_host_listener_async(self):
        while not self.stop_event.is_set():
            message = await self.channels.host_to_supervisor.receive_async(self.loop)
            if message.content == "stop":
                print("[Supervisor] Received 'stop' message")
                self.stop_event.set()

    async def run_service_listener_async(self):
        while not self.stop_event.is_set():
            message = await self.channels.service_to_supervisor.receive_async(self.loop)
            if message.content == "started":
                self.starting_event.clear()
                self.stopped_event.clear()
                self.crashed_event.clear()
            elif message.content == "stopped":
                self.stopped_event.set()
            elif message.content == "crashed":
                self.crashed_event.set()
            else:
                print(f"[Supervisor] Unsupported message received, dropping: {message}")

    async def run_async(self):
        while not self.stop_event.is_set():
            try:
                print(f"[Supervisor] Hello from supervisor")
                if self.crashed_event.is_set():
                    await self.channels.supervisor_to_service.send_async(
                        Message(sender="supervisor", content=f"start"),
                        self.loop,
                    )
                    self.crashed_event.clear()
                    self.starting_event.set()
                elif self.starting_event.is_set():
                    self.starting_event.clear()
                await asyncio.sleep(1.0)
            except Exception as e:
                print(f"[Supervisor] Crashed: {e}")
                raise NotImplementedError()

        # Stop service
        print(f"[Supervisor] Sending 'stop' to service")
        await self.channels.supervisor_to_service.send_async(
            Message(sender="supervisor", content=f"stop"),
            self.loop,
        )
        while not self.stopped_event.is_set():
            print(f"[Supervisor] Waiting for service to stop..")
            await asyncio.sleep(1.0)
        print(f"[Supervisor] Service has stopped!")
