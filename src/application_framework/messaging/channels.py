class Channels:
    def __init__(self, host_to_supervisor, supervisor_to_host, supervisor_to_service, service_to_supervisor):
        self.host_to_supervisor = host_to_supervisor
        self.supervisor_to_host = supervisor_to_host
        self.supervisor_to_service = supervisor_to_service
        self.service_to_supervisor = service_to_supervisor
