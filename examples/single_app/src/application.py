from application_framework.application.base import ApplicationBase

from examples.single_app.config import AppConfig


class Application(ApplicationBase):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
