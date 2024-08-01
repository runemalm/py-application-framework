from abc import ABC


class ActorBase(ABC):
    def __init__(self):
        self.stop_event = None

    def start(self, stop_event):
        raise Exception("No start() method has been implemented.")

    async def start_async(self, stop_event):
        raise Exception("No start_async() method has been implemented.")

    def stop(self):
        raise Exception("No stop() method has been implemented.")

    async def stop_async(self):
        raise Exception("No stop_async() method has been implemented.")
