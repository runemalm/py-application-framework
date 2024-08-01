import threading
import time

from application_framework.actor.actor import ActorBase


class Service(ActorBase):
    def __init__(self):
        super().__init__()
        self.loop = None
        self.service_id = None
        self.channels = None
        self.supervisor_listener_thread = None
        self.supervisor_listener_task = None

    def start(self, stop_event):
        self.stop_event = stop_event
        self.supervisor_listener_thread = threading.Thread(target=self.run_supervisor_listener, daemon=True)
        self.supervisor_listener_thread.start()
        self.run()

    async def start_async(self, stop_event):
        self.stop_event = stop_event
        self.supervisor_listener_task = self.loop.create_task(self.run_supervisor_listener_async())
        await self.run_async()

    def run(self):
        """Run the service synchronously. Override this method in subclasses."""
        raise Exception("No sync() method has been implemented.")

    async def run_async(self):
        """Run the service asynchronously. Override this method in subclasses."""
        raise Exception("No async() method has been implemented.")

    def stop(self):
        self.stop_event.set()
        if self.supervisor_listener_thread:
            self.supervisor_listener_thread.join()

    async def stop_async(self):
        self.stop_event.set()

    def run_supervisor_listener(self):
        while not self.stop_event.is_set():
            message = self.channels.supervisor_to_service.receive()
            if message:
                if message.content == "stop":
                    print("[Service] Received 'stop' message")
                    self.stop_event.set()
                else:
                    raise NotImplementedError(f"Received some unknown message: {message}")
            time.sleep(0.5)
        print("[Service] STOP EVENT WAS SET!")

    async def run_supervisor_listener_async(self):
        while not self.stop_event.is_set():
            message = await self.channels.supervisor_to_service.receive_async(self.loop)
            if message.content == "stop":
                print("[Service] Received 'stop' message")
                self.stop_event.set()
            else:
                raise NotImplementedError(f"Received some unknown message: {message}")
        print("[Service] STOP EVENT WAS SET!")

    def set_loop(self, loop):
        self.loop = loop

    def set_service_id(self, service_id):
        self.service_id = service_id

    def set_channels(self, channels):
        self.channels = channels
