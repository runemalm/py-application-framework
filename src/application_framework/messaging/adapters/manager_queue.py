import traceback

from application_framework.messaging.message_queue import MessageQueue


class ManagerQueue(MessageQueue):
    def __init__(self, queue):
        self.queue = queue

    async def send_async(self, message, loop):
        try:
            await loop.run_in_executor(None, self.queue.put, message)
            print(f"[ManagerQueue] Async message sent: {message}")
        except BrokenPipeError:
            print(f"[ManagerQueue] Broken pipe error while sending message asynchronously: {message}")
        except Exception as e:
            print(f"[ManagerQueue] Error sending message asynchronously: {e}")
            # print(traceback.format_exc())

    async def receive_async(self, loop):
        try:
            message = await loop.run_in_executor(None, self.queue.get, 1)
            print(f"[ManagerQueue] Async message received: {message}")
            return message
        except EOFError:
            print(f"[ManagerQueue] EOFError while receiving message asynchronously.")
        except Exception as e:
            print(f"[ManagerQueue] Error receiving message asynchronously: {e}")
            # print(traceback.format_exc())
        return None

    def send(self, message):
        try:
            self.queue.put(message)
            print(f"[ManagerQueue] Message sent: {message}")
        except Exception as e:
            print(f"[ManagerQueue] Error sending message: {e}")

    def receive(self):
        try:
            if not self.queue.empty():
                message = self.queue.get(timeout=1)
                print(f"[ManagerQueue] Message received: {message}")
                return message
        except Exception as e:
            print(f"[ManagerQueue] Error receiving message: {e}")
            print(traceback.format_exc())
        return None
