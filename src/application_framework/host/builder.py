import asyncio

from application_framework.host.host import Host


class HostBuilder:
    def __init__(self):
        self.loop = self.get_or_create_loop()
        self.service_configs = []
        self.listening_port = None

    def add_application(self, service_config):
        self.service_configs.append(service_config)
        return self

    def set_listening_port(self, listening_port):
        self.listening_port = listening_port
        return self

    def build(self):
        host = Host(self.loop)
        for service_config in self.service_configs:
            host.add_service_config(service_config)
        return host

    def get_or_create_loop(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
