import asyncio
import random

from application_framework.actor.actor import ActorBase
from application_framework.messaging.message import Message
from application_framework.supervisor.restart_strategy import RestartStrategy


class Supervisor(ActorBase):
    def __init__(self, loop, service_id, channels, restart_strategy):
        super().__init__()
        self.loop = loop
        self.service_id = service_id
        self.channels = channels
        self.restart_strategy = restart_strategy
        self.host_listener_task = None
        self.service_listener_task = None
        self.starting_event = asyncio.Event()
        self.stopping_event = asyncio.Event()
        self.stopped_event = asyncio.Event()
        self.crashed_event = asyncio.Event()

    async def start_async(self, stop_event):
        """Starts the supervisor and initializes listener tasks."""
        self.stop_event = stop_event
        self.host_listener_task = self.loop.create_task(self.run_host_listener_async())
        self.service_listener_task = self.loop.create_task(self.run_service_listener_async())
        await self.run_async()

    async def stop_async(self):
        """Signals the supervisor to stop."""
        self.stop_event.set()

    async def run_host_listener_async(self):
        """Listens for messages from the host and handles them."""
        while not self.stop_event.is_set():
            message = await self.channels.host_to_supervisor.receive_async(self.loop)
            if message.content == "stop":
                print("[Supervisor] Received 'stop' message")
                self.stop_event.set()

    async def run_service_listener_async(self):
        """Listens for messages from the service and updates the supervisor's state."""
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
        """Main loop for the supervisor to manage the service."""
        while not self.stop_event.is_set():
            try:
                print("[Supervisor] Hello from supervisor")
                if self.crashed_event.is_set():
                    await self._restart_service()
                await asyncio.sleep(1.0)
            except Exception as e:
                print(f"[Supervisor] Crashed: {e}")
                break

        await self._stop_service()

    async def _restart_service(self):
        """Handles the restarting of the service when it crashes."""
        try:
            backoff_time = self._calculate_backoff()
            jitter = self._calculate_jitter()
            total_backoff = backoff_time + jitter
            print(f"[Supervisor] Restarting service after {total_backoff} seconds (backoff: {backoff_time}, jitter: {jitter})")
            await asyncio.sleep(total_backoff)
            await self.channels.supervisor_to_service.send_async(
                Message(sender="supervisor", content="start"),
                self.loop,
            )
            self.crashed_event.clear()
            self.starting_event.set()
            self._reset_backoff()
        except Exception as e:
            print(f"[Supervisor] Failed to restart service: {e}")

    def _calculate_backoff(self):
        """Calculates the backoff time based on the restart strategy."""
        if self.restart_strategy.strategy == RestartStrategy.IMMEDIATE:
            return 0
        elif self.restart_strategy.strategy == RestartStrategy.FIXED_BACKOFF:
            return self.restart_strategy.fixed_backoff_time
        elif self.restart_strategy.strategy == RestartStrategy.EXPONENTIAL_BACKOFF:
            backoff_time = min(self.backoff_time, self.restart_strategy.max_backoff_time)
            self.backoff_time = min(self.backoff_time * 2, self.restart_strategy.max_backoff_time)  # Exponentially increase the backoff time up to the maximum
            return backoff_time
        elif self.restart_strategy.strategy == RestartStrategy.LINEAR_BACKOFF:
            backoff_time = min(self.backoff_time, self.restart_strategy.max_backoff_time)
            self.backoff_time = min(self.backoff_time + 1, self.restart_strategy.max_backoff_time)  # Linearly increase the backoff time up to the maximum
            return backoff_time
        else:
            return 0

    def _calculate_jitter(self):
        """Calculates a random jitter based on the number of retry attempts."""
        if self.restart_strategy.strategy == RestartStrategy.EXPONENTIAL_BACKOFF:
            jitter = random.uniform(0, min(self.restart_strategy.max_jitter, int(self.backoff_time / 2)))
            self.retry_attempts += 1
            return jitter
        return 0

    def _reset_backoff(self):
        """Resets the backoff time and retry attempts if needed."""
        if self.restart_strategy.strategy in [RestartStrategy.EXPONENTIAL_BACKOFF, RestartStrategy.LINEAR_BACKOFF]:
            self.backoff_time = 1
            self.retry_attempts = 0

    async def _stop_service(self):
        """Handles stopping the service gracefully."""
        try:
            print("[Supervisor] Sending 'stop' to service")
            await self.channels.supervisor_to_service.send_async(
                Message(sender="supervisor", content="stop"),
                self.loop,
            )
            while not self.stopped_event.is_set():
                print("[Supervisor] Waiting for service to stop...")
                await asyncio.sleep(1.0)
            print("[Supervisor] Service has stopped!")
        except Exception as e:
            print(f"[Supervisor] Error stopping service: {e}")
