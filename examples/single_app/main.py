import os

from application_framework.application.builder import ApplicationBuilder
from application_framework.config.builder import ConfigBuilder
from application_framework.host.builder import HostBuilder
from application_framework.monitoring.restart_policy import RestartPolicy

from examples.single_app.config import AppConfig, Config
from examples.single_app.src.application import Application
from examples.single_app.src.greet_action import GreetAction


def main():

    config = (
        ConfigBuilder()
            .set_environment_profile(env=os.getenv("APP_ENV", "development"))
            .add_yaml_file(path="config.common.yaml")
            .add_profiled_file(template="config.{profile}.yaml")
            .add_prefixed_env_vars(prefix="CFG_", section_separator=".")
            .set_type_conversion('host.port', int)
            .set_type_conversion('app.port', int)
            .bind(Config)
            .build()
    )

    application = (
        ApplicationBuilder()
            .set_config(config.app)
            .set_root_directory(".")
            .set_name("MyApp")
            .run_in_separate_process()
            .add_route(protocol="http", path="/app/?.*", port=config.app.port)
            .set_application_class(Application)
            .set_restart_policy(RestartPolicy.ExponentialBackoff)
            .register_instance(AppConfig, config.app)
            .register_transient(GreetAction)
            .build()
    )

    host = (
        HostBuilder()
            .set_config(config.host)
            .add_application(application)
            .set_listening_port(config.host.port)
            .build()
    )

    host.run()


if __name__ == "__main__":
    main()
