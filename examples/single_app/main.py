import os

from application_framework.config.builder import ConfigBuilder
from application_framework.host.builder import HostBuilder
from application_framework.service.application.builder import ApplicationBuilder
from application_framework.supervisor.restart_strategy import RestartStrategy
from application_framework.tasks.execution_mode import ExecutionMode

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

    async_app = (
        ApplicationBuilder()
            .set_name("Async App")
            .set_root_directory(".")
            .add_route(protocol="http", path="/app/?.*", port=config.app.port)
            .set_application_class(Application)
            .set_execution_mode(ExecutionMode.MAIN_EVENT_LOOP_ASYNC)
            .set_restart_strategy(RestartStrategy.FIXED_BACKOFF)
            .register_instance(AppConfig, config.app)
            .register_transient(GreetAction)
            .build()
    )

    thread_app = (
        ApplicationBuilder()
        .set_name("Thread App")
        .set_root_directory(".")
        .add_route(protocol="http", path="/app/?.*", port=config.app.port)
        .set_application_class(Application)
        .set_execution_mode(ExecutionMode.SEPARATE_THREAD)
        .set_restart_strategy(RestartStrategy.FIXED_BACKOFF)
        .register_instance(AppConfig, config.app)
        .register_transient(GreetAction)
        .build()
    )

    process_app = (
        ApplicationBuilder()
        .set_name("Process App")
        .set_root_directory(".")
        .add_route(protocol="http", path="/app/?.*", port=config.app.port)
        .set_application_class(Application)
        .set_execution_mode(ExecutionMode.SEPARATE_PROCESS)
        .set_restart_strategy(RestartStrategy.FIXED_BACKOFF)
        .register_instance(AppConfig, config.app)
        .register_transient(GreetAction)
        .build()
    )

    host = (
        HostBuilder()
            .add_application(async_app)
            # .add_application(thread_app)
            # .add_application(process_app)
            .set_listening_port(config.host.port)
            .build()
    )

    host.start()


if __name__ == "__main__":
    main()
