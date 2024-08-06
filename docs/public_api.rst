.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

########################
Examples
########################

Single application setup
------------------------

This example shows how to set up a basic single application using the framework.

.. code-block:: python
    
    # examples/single_app/main.py

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

        application = (
            ApplicationBuilder()
                .set_name("My Application")
                .set_root_directory(".")
                .add_route(protocol="http", path="/app/?.*", port=config.app.port)
                .set_application_class(Application)
                .set_execution_mode(ExecutionMode.MAIN_EVENT_LOOP_ASYNC)
                .set_restart_strategy(RestartStrategy.FIXED_BACKOFF)
                .register_instance(AppConfig, config.app)
                .register_transient(GreetAction)
                .build()
        )

        host = (
            HostBuilder()
                .add_application(application)
                .set_listening_port(config.host.port)
                .build()
        )

        host.start()


    if __name__ == "__main__":
        main()
