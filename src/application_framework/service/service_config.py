class ServiceConfig:
    def __init__(self, service_id, service_class, execution_mode, restart_strategy, serialized_state, root_directory, name, routes):
        self.service_id = service_id
        self.service_class = service_class
        self.execution_mode = execution_mode
        self.restart_strategy = restart_strategy
        self.serialized_state = serialized_state
        self.root_directory = root_directory
        self.name = name
        self.routes = routes
