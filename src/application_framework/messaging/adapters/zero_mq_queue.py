import zmq
import zmq.asyncio

from application_framework.messaging.message import Message
from application_framework.messaging.message_queue import MessageQueue


class ZeroMQQueue(MessageQueue):
    def __init__(self, address):
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind(address)

    async def send_async(self, message, loop):
        await loop.run_in_executor(None, self.socket.send_json, message.__dict__)

    async def receive_async(self, loop):
        message_dict = await loop.run_in_executor(None, self.socket.recv_json)
        return Message(**message_dict)

    def send(self, message):
        self.socket.send_json(message.__dict__)

    def receive(self):
        message_dict = self.socket.recv_json()
        return Message(**message_dict)
