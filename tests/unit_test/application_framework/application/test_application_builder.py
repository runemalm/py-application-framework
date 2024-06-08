from application_framework.application.base import ApplicationBase
from unit_test.unit_test_case import UnitTestCase

from application_framework.application.builder import ApplicationBuilder
from application_framework.monitoring.restart_policy import RestartPolicy

from examples.single_app.config import AppConfig, Config
from examples.single_app.src.greet_action import GreetAction


class Application(ApplicationBase):
    def __init__(self):
        super().__init__()


class TestApplicationBuilder(UnitTestCase):

    def setUp(self):
        self.builder = ApplicationBuilder()

    def test_build_complete_application(self):
        config_dict = {
            "host": {
                "port": 80
            },
            "app": {
                "port": 5000,
            },
        }

        config = Config.from_dict(config_dict)

        application_builder = (
            ApplicationBuilder()
                .set_config(config.app)
                .set_root_directory("/some/path")
                .set_name("TestApp")
                .run_in_separate_process()
                .add_route(protocol="http", path="/app/?.*", port=config.app.port)
                .set_application_class(Application)
                .set_restart_policy(RestartPolicy.ExponentialBackoff)
                .register_instance(AppConfig, config.app)
                .register_transient(GreetAction)
        )

        # Build the application
        application = application_builder.build()

        # Assertions to ensure the application is built correctly
        self.assertIsInstance(application, Application)
        self.assertEqual(application.root_directory, "/some/path")
        self.assertEqual(application.name, "TestApp")
        self.assertTrue(application.run_in_separate_process)
        self.assertEqual(application.routes, [{"protocol": "http", "path": "/app/?.*", "port": 5000}])
        self.assertEqual(application.restart_policy, RestartPolicy.ExponentialBackoff)

        # Ensure dependencies are registered correctly
        resolved_config = application.container.resolve(AppConfig)
        resolved_greet_action = application.container.resolve(GreetAction)
        self.assertEqual(resolved_config, config.app)
        self.assertIsInstance(resolved_greet_action, GreetAction)
