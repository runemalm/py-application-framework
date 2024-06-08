class ApplicationBase:
    def __init__(self):
        self.root_directory = None
        self.name = None
        self.run_in_separate_process = False
        self.routes = []
        self.restart_policy = None
        self.container = None

    def set_root_directory(self, root_directory):
        self.root_directory = root_directory

    def set_name(self, name):
        self.name = name

    def set_run_in_separate_process(self, flag):
        self.run_in_separate_process = flag

    def add_route(self, protocol, path, port):
        self.routes.append({"protocol": protocol, "path": path, "port": port})

    def set_restart_policy(self, restart_policy):
        self.restart_policy = restart_policy

    def set_dependency_container(self, container):
        self.container = container
