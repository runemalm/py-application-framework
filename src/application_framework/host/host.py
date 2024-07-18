import asyncio
import signal
from asyncio import CancelledError

from application_framework.tasks.execution_mode import ExecutionMode
from application_framework.tasks.tasks import AsyncProcessTask, AsyncTask, \
    AsyncThreadTask, ProcessTask, \
    SupervisorTask, ThreadTask


class Host:
    def __init__(self, loop):
        self.loop = loop
        self.is_running = False
        self.service_tasks = []
        self.supervisor_tasks = []
        self.service_configs = []
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        self.loop.add_signal_handler(signal.SIGTERM, self.handle_signal, signal.SIGTERM)
        self.loop.add_signal_handler(signal.SIGINT, self.handle_signal, signal.SIGINT)

    def handle_signal(self, signum):
        print(f"Received signal {signum}, stopping host...")
        self.loop.create_task(self.stop())

    def add_service_config(self, service_config):
        self.service_configs.append(service_config)

    def start(self):
        self.is_running = True
        try:
            self.loop.run_until_complete(self.run_async())
        except CancelledError:
            print("Main loop was cancelled.")
        finally:
            if not self.loop.is_closed():
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                self.loop.close()

    async def run_async(self):

        # Create tasks
        for service_config in self.service_configs:
            supervisor_task = self.create_supervisor_task(service_config)
            self.supervisor_tasks.append(supervisor_task)

            service_task = self.create_service_task(service_config)
            self.service_tasks.append(service_task)

        # Schedule tasks
        for supervisor_task in self.supervisor_tasks:
            supervisor_task.schedule()

        for service_task in self.service_tasks:
            service_task.schedule()

        # Run the event loop
        coroutines = [task.task for task in self.supervisor_tasks]
        coroutines += [task.task for task in self.service_tasks]

        await asyncio.gather(*coroutines)

    async def stop(self):
        print("Stopping tasks...")

        coroutines = [task.task for task in self.supervisor_tasks]
        coroutines += [task.task for task in self.service_tasks]

        for coroutine in coroutines:
            coroutine.cancel()

        results = await asyncio.gather(*coroutines, return_exceptions=True)
        for result in results:
            if isinstance(result, CancelledError):
                print("Task was cancelled.")
            elif result is not None:
                print(f"Task ended with exception: {result}")

        print("All tasks have been cancelled.")
        self.loop.stop()

        self.is_running = False

    def create_service_task(self, service_config):
        if service_config.execution_mode == ExecutionMode.MAIN_EVENT_LOOP_ASYNC:
            task = AsyncTask(self.loop, service_config)
        elif service_config.execution_mode == ExecutionMode.SEPARATE_THREAD:
            task = ThreadTask(self.loop, service_config)
        elif service_config.execution_mode == ExecutionMode.SEPARATE_THREAD_ASYNC:
            task = AsyncThreadTask(self.loop, service_config)
        elif service_config.execution_mode == ExecutionMode.SEPARATE_PROCESS:
            task = ProcessTask(self.loop, service_config)
        elif service_config.execution_mode == ExecutionMode.SEPARATE_PROCESS_ASYNC:
            task = AsyncProcessTask(self.loop, service_config)
        else:
            raise ValueError("Invalid execution mode specified")
        return task

    def create_supervisor_task(self, service_config):
        task = SupervisorTask(self.loop, service_config)
        return task
