import os

from application_framework.config.builder import ConfigBuilder
from application_framework.host.builder import HostBuilder
from application_framework.service.application.builder import ApplicationBuilder
from application_framework.supervisor.restart_strategy import RestartStrategy
from application_framework.service.execution_mode import ExecutionMode

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

    # Specify the number of applications and their execution mode distribution
    num_applications = 4
    execution_mode_distribution = {
        ExecutionMode.MAIN_EVENT_LOOP_ASYNC: 0.20,
        ExecutionMode.SEPARATE_THREAD: 0.20,
        ExecutionMode.SEPARATE_THREAD_ASYNC: 0.20,
        ExecutionMode.SEPARATE_PROCESS: 0.20,
        ExecutionMode.SEPARATE_PROCESS_ASYNC: 0.20,
    }

    # Calculate the number of applications for each execution mode
    mode_counts = {mode: int(num_applications * proportion) for mode, proportion in
                   execution_mode_distribution.items()}

    # Correct any rounding errors to ensure total applications count is correct
    total_assigned = sum(mode_counts.values())
    while total_assigned < num_applications:
        for mode in execution_mode_distribution:
            if total_assigned < num_applications:
                mode_counts[mode] += 1
                total_assigned += 1

    applications = []
    app_counter = 1

    for mode, count in mode_counts.items():
        for _ in range(count):
            application_name = f"App {app_counter} [{mode.name.lower()}]"
            application = (
                ApplicationBuilder()
                    .set_name(application_name)
                    .set_root_directory(".")
                    .add_route(protocol="http", path="/app/?.*", port=config.app.port)
                    .set_application_class(Application)
                    .set_execution_mode(mode)
                    .set_restart_strategy(RestartStrategy.IMMEDIATE)
                    .register_instance(AppConfig, config.app)
                    .register_transient(GreetAction)
                    .build()
            )
            applications.append(application)
            app_counter += 1

    host_builder = HostBuilder()

    for app in applications:
        host_builder.add_application(app)

    host = (
        host_builder
            .set_listening_port(config.host.port)
            .build()
    )

    host.start()


if __name__ == "__main__":
    main()
