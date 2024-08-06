import uuid

from dependency_injection.container import DependencyContainer

from application_framework.service.service_config import ServiceConfig
from application_framework.supervisor.restart_strategy import RestartStrategy


class ApplicationBuilder:
    def __init__(self):
        self.service_id = uuid.uuid4()
        self.name = None
        self.root_directory = None
        self.execution_mode = None
        self.routes = []
        self.application_class = None
        self.restart_strategy = RestartStrategy()
        self.container = DependencyContainer.get_instance(f"{self.service_id}_initial")

    def set_root_directory(self, root_directory):
        self.root_directory = root_directory
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_execution_mode(self, execution_mode):
        self.execution_mode = execution_mode
        return self

    def add_route(self, protocol, path, port):
        self.routes.append({"protocol": protocol, "path": path, "port": port})
        return self

    def set_application_class(self, application_class):
        self.application_class = application_class
        self.container.register_singleton(self.application_class)
        return self

    def set_restart_strategy(self, strategy, fixed_backoff_time=5, max_backoff_time=60, max_jitter=5):
        self.restart_strategy = RestartStrategy(strategy, fixed_backoff_time, max_backoff_time, max_jitter)
        return self

    def set_fixed_backoff_time(self, fixed_backoff_time):
        self.fixed_backoff_time = fixed_backoff_time
        return self

    def set_max_backoff_time(self, max_backoff_time):
        self.max_backoff_time = max_backoff_time
        return self

    def set_max_jitter(self, max_jitter):
        self.max_jitter = max_jitter
        return self

    def register_instance(self, *args, **kwargs):
        self.container.register_instance(*args, **kwargs)
        return self

    def register_transient(self, *args, **kwargs):
        self.container.register_transient(*args, **kwargs)
        return self

    def register_scoped(self, *args, **kwargs):
        self.container.register_scoped(*args, **kwargs)
        return self

    def register_singleton(self, *args, **kwargs):
        self.container.register_singleton(*args, **kwargs)
        return self

    def register_factory(self, *args, **kwargs):
        self.container.register_factory(*args, **kwargs)
        return self

    def build(self):
        service_config = ServiceConfig(
            service_class=self.application_class,
            execution_mode=self.execution_mode,
            restart_strategy=self.restart_strategy,
            serialized_state=self.container.serialize_state(),
            root_directory=self.root_directory,
            name=self.name,
            service_id=self.service_id,
            routes=self.routes,
        )
        return service_config
