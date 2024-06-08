from dependency_injection.container import DependencyContainer


class ApplicationBuilder:
    def __init__(self):
        self.config = None
        self.root_directory = None
        self.name = None
        self._run_in_separate_process_flag = False
        self.routes = []
        self.application_class = None
        self.restart_policy = None
        self.container = DependencyContainer.get_instance()

    def set_config(self, config):
        self.config = config
        return self

    def set_root_directory(self, root_directory):
        self.root_directory = root_directory
        return self

    def set_name(self, name):
        self.name = name
        return self

    def run_in_separate_process(self):
        self._run_in_separate_process_flag = True
        return self

    def add_route(self, protocol, path, port):
        self.routes.append({"protocol": protocol, "path": path, "port": port})
        return self

    def set_application_class(self, application_class):
        self.application_class = application_class
        self.container.register_singleton(self.application_class)
        return self

    def set_restart_policy(self, restart_policy):
        self.restart_policy = restart_policy
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
        app = self.container.resolve(self.application_class)
        app.set_root_directory(self.root_directory)
        app.set_name(self.name)
        app.set_run_in_separate_process(self._run_in_separate_process_flag)
        app.routes = self.routes
        app.set_restart_policy(self.restart_policy)
        app.set_dependency_container(self.container)
        return app
