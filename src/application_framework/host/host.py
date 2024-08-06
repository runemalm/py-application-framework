import asyncio
import os
import signal
import threading
from asyncio import CancelledError
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Manager
from dependency_injection.container import DependencyContainer

from application_framework.messaging.adapters.manager_queue import ManagerQueue
from application_framework.messaging.channels import Channels
from application_framework.messaging.message import Message
from application_framework.messaging.adapters.zero_mq_queue import ZeroMQQueue
from application_framework.supervisor.supervisor import Supervisor
from application_framework.service.execution_mode import ExecutionMode


class Host:
    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        self.stop_event = asyncio.Event()
        self.thread_pool_executor = None
        self.process_pool_executor = None
        self.supervisor_tasks = []
        self.service_tasks = []
        self.channels = {}
        self.manager = self.start_manager()
        self.service_configs = []
        self.setup_signal_handlers()

    def start_manager(self):
        return Manager()

    def add_service_config(self, service_config):
        self.service_configs.append(service_config)

    def setup_signal_handlers(self):
        self.loop.add_signal_handler(signal.SIGTERM, self.handle_signal, signal.SIGTERM)
        self.loop.add_signal_handler(signal.SIGINT, self.handle_signal, signal.SIGINT)

    def handle_signal(self, signum):
        print(f"Received signal {signum}, stopping host...")
        self.loop.create_task(self.stop_async())

    async def send_sigint_after_delay(self, delay):
        await asyncio.sleep(delay)
        os.kill(os.getpid(), signal.SIGINT)

    def create_pools(self):
        thread_count = sum([
            1 for sc in self.service_configs
            if sc.execution_mode in [ExecutionMode.SEPARATE_THREAD,
                                     ExecutionMode.SEPARATE_THREAD_ASYNC]
        ])
        process_count = sum([
            1 for sc in self.service_configs
            if sc.execution_mode in [ExecutionMode.SEPARATE_PROCESS,
                                     ExecutionMode.SEPARATE_PROCESS_ASYNC]
        ])
        if thread_count:
            self.thread_pool_executor = ThreadPoolExecutor(max_workers=thread_count)
        if process_count:
            self.process_pool_executor = ProcessPoolExecutor(max_workers=process_count)

    def start(self):
        self.create_pools()

        try:
            self.loop.create_task(self.send_sigint_after_delay(3))
            self.loop.run_until_complete(self.run_async())
        except CancelledError:
            print("Main loop was cancelled.")
        except Exception as e:
            print(f"Exception in main loop: {e}")
        finally:
            print("Main loop was finished.")
            self.cleanup_loop()
            self.cleanup_manager()
            self.cleanup_executors()

    def stop(self):
        self.loop.create_task(self.stop_async())

    async def stop_async(self):
        self.stop_event.set()

    async def run_async(self):
        for config in self.service_configs:

            # Create communication channels
            channels = self.create_channels()
            self.channels[config.service_id] = channels

            # Schedule supervisor
            self.schedule_supervisor(config.service_id, channels, config.restart_strategy)

            # Schedule service
            if config.execution_mode == ExecutionMode.MAIN_EVENT_LOOP_ASYNC:
                self.schedule_service_task_async(config, channels)
            elif config.execution_mode == ExecutionMode.SEPARATE_THREAD:
                self.schedule_service_task_thread(config, channels)
            elif config.execution_mode == ExecutionMode.SEPARATE_THREAD_ASYNC:
                self.schedule_service_task_async_thread(config, channels)
            elif config.execution_mode == ExecutionMode.SEPARATE_PROCESS:
                self.schedule_service_task_process(config, channels)
            elif config.execution_mode == ExecutionMode.SEPARATE_PROCESS_ASYNC:
                self.schedule_service_task_async_process(config, channels)
            else:
                raise ValueError("Invalid execution mode specified")

        while not self.stop_event.is_set():
            await asyncio.sleep(1.0)

        await self.cleanup_tasks()

    async def cleanup_tasks(self):
        for channel in self.channels.values():
            await channel.host_to_supervisor.send_async(
                Message(sender="host", content=f"stop"),
                self.loop,
            )

        results = await asyncio.gather(
            *(self.supervisor_tasks + self.service_tasks),
            return_exceptions=True)

        print("[Host] All tasks have finished.")

        for result in results:
            if isinstance(result, CancelledError):
                print("Task was cancelled.")
            elif result is not None:
                print(f"Task ended with exception: {result}")

        self.loop.stop()

    def cleanup_loop(self):
        if not self.loop.is_closed():
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    def cleanup_manager(self):
        try:
            self.manager.shutdown()
            print("Manager and all related processes have been properly shut down.")
        except Exception as e:
            print(f"Error during manager shutdown: {e}")

    def cleanup_executors(self):
        if self.thread_pool_executor:
            self.thread_pool_executor.shutdown(wait=True)
        if self.process_pool_executor:
            self.process_pool_executor.shutdown(wait=True)

    def create_queue(self):
        queue = self.manager.Queue()
        return ManagerQueue(queue)
        # return ZeroMQQueue(self.loop, "tcp://127.0.0.1:5555")

    def create_channels(self):
        host_to_supervisor = self.create_queue()
        supervisor_to_host = self.create_queue()
        supervisor_to_service = self.create_queue()
        service_to_supervisor = self.create_queue()
        return Channels(
            host_to_supervisor, supervisor_to_host,
            supervisor_to_service, service_to_supervisor
        )

    # Schedule Tasks

    def schedule_supervisor(self, service_id, channels, restart_strategy):
        stop_event = asyncio.Event()
        supervisor = Supervisor(self.loop, service_id, channels, restart_strategy)
        task = self.loop.create_task(supervisor.start_async(stop_event))
        self.supervisor_tasks.append(task)

    def schedule_service_task_async(self, service_config, channels):
        task = self.loop.create_task(Host.start_service_async(service_config, channels, self.loop))
        self.service_tasks.append(task)

    def schedule_service_task_thread(self, service_config, channels):
        task = self.loop.run_in_executor(self.thread_pool_executor, Host.start_service, service_config, channels)
        self.service_tasks.append(task)

    def schedule_service_task_async_thread(self, service_config, channels):
        task = self.loop.run_in_executor(self.thread_pool_executor, Host.run_service_async_thread, service_config, channels)
        self.service_tasks.append(task)

    def schedule_service_task_process(self, service_config, channels):
        task = self.loop.run_in_executor(self.process_pool_executor, Host.start_service, service_config, channels)
        self.service_tasks.append(task)

    def schedule_service_task_async_process(self, service_config, channels):
        task = self.loop.run_in_executor(self.process_pool_executor, Host.run_service_async_process, service_config, channels)
        self.service_tasks.append(task)

    @staticmethod
    def start_service(service_config, channels):
        try:
            stop_event = threading.Event()
            container = DependencyContainer.get_instance(name=service_config.service_id)
            container.deserialize_state(service_config.serialized_state)
            service_instance = container.resolve(service_config.service_class)
            service_instance.set_service_id(service_config.service_id)
            service_instance.set_channels(channels)
            service_instance.start(stop_event)
        except Exception as e:
            print(f"Error in start_service: {e}")

    @staticmethod
    async def start_service_async(service_config, channels, loop):
        try:
            stop_event = asyncio.Event()
            container = DependencyContainer.get_instance(name=service_config.service_id)
            container.deserialize_state(service_config.serialized_state)
            service_instance = container.resolve(service_config.service_class)
            service_instance.set_loop(loop)
            service_instance.set_service_id(service_config.service_id)
            service_instance.set_channels(channels)
            await service_instance.start_async(stop_event)
        except Exception as e:
            print(f"Error in start_service_async: {e}")

    @staticmethod
    def run_service_async_thread(service_config, channels):
        try:
            thread_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(thread_loop)
            thread_loop.run_until_complete(Host.start_service_async(service_config, channels, thread_loop))
        except Exception as e:
            print(f"Error in run_service_async_thread: {e}")

    @staticmethod
    def run_service_async_process(service_config, channels):
        try:
            process_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(process_loop)
            process_loop.run_until_complete(Host.start_service_async(service_config, channels, process_loop))
        except Exception as e:
            print(f"Error in run_service_async_process: {e}")
