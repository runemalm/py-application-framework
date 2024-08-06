from abc import ABC, abstractmethod

from application_framework.messaging.message import Message


class MessageQueue(ABC):
    @abstractmethod
    async def send_async(self, message, loop):
        pass

    @abstractmethod
    async def receive_async(self, loop):
        pass

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self):
        pass
