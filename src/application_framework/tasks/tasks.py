import asyncio
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from dependency_injection.container import DependencyContainer

from application_framework.supervisor.supervisor import Supervisor


class SupervisorTask:
    def __init__(self, loop, service_config):
        self.loop = loop
        self.service_config = service_config
        self.task = None

    def schedule(self):
        supervisor = Supervisor(self.loop, self.service_config)
        self.task = self.loop.create_task(supervisor.run_async())


# Base Task class
class BaseServiceTask(ABC):
    def __init__(self, loop, service_config):
        self.loop = loop
        self.service_config = service_config
        self.task = None

    def run(self):
        container = DependencyContainer.get_instance(name=self.service_config.service_id)
        container.deserialize_state(self.service_config.serialized_state)
        service_instance = container.resolve(self.service_config.service_class)
        service_instance.run()

    async def run_async(self):
        container = DependencyContainer.get_instance(name=self.service_config.service_id)
        container.deserialize_state(self.service_config.serialized_state)
        service_instance = container.resolve(self.service_config.service_class)
        await service_instance.run_async()

    @abstractmethod
    def schedule(self):
        """Schedule the task on the event loop. Override this method in subclasses."""
        pass


class AsyncTask(BaseServiceTask):
    def schedule(self):
        self.task = self.loop.create_task(self.run_async())


class ThreadTask(BaseServiceTask):
    def schedule(self):
        with ThreadPoolExecutor() as executor:
            self.task = self.loop.run_in_executor(executor, self.run)


class AsyncThreadTask(BaseServiceTask):
    def schedule(self):
        with ThreadPoolExecutor() as executor:
            self.task = self.loop.run_in_executor(executor, asyncio.run, self.run_async())


class ProcessTask(BaseServiceTask):
    def schedule(self):
        with ProcessPoolExecutor() as executor:
            self.task = self.loop.run_in_executor(executor, self.run)


class AsyncProcessTask(BaseServiceTask):
    def schedule(self):
        with ProcessPoolExecutor() as executor:
            self.task = self.loop.run_in_executor(executor, asyncio.run, self.run_async())
