.. warning::

    This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _userguide-getting-started:

Getting Started
===============

Follow this guide to create your first "Hello World" application with the py-application-framework.

.. note::

    You can find the complete source code in the `examples/single_app <https://github.com/runemalm/py-application-framework/tree/master/examples/single_app>`_ folder on GitHub.

Installation
------------

Install using `pip <http://pypi.python.org/pypi/pip/>`_::

    $ pip install py-application-framework


Project structure
-----------------

Your project folder should be structured as follows:

.. code-block:: arduino

   hello-world/
   │
   ├── config.common.yaml
   ├── config.py
   ├── main.py
   └── src/
       └── application.py

We will create the files in the sections to come.


Create the main.py file
-----------------------

The **`main.py`** file serves as the entry point for your application. Create this file in your project root:

.. code-block:: python

    def main():
        pass

    if __name__ == "__main__":
        main()

Create the host- and application configuration
----------------------------------------------

We'll create a configuration file and corresponding classes to handle configuration settings. For more detailed information, refer to the :ref:`Configuration System <configuration-system>`.

1. Create **`config.common.yaml`** in your project root:

.. code-block:: yaml

    host:
        port: 80
    app:
        port: 5000
        greeting: "Hello World!"

2. Create **`config.py`** to bind these configurations:

.. code-block:: python

    from dataclasses import dataclass, field


    @dataclass
    class HostConfig:
        port: int = 80

    @dataclass
    class AppConfig:
        port: int = 5000
        greeting: str = "Hello World"

    @dataclass
    class Config:
        host: HostConfig = field(default_factory=HostConfig)
        app: AppConfig = field(default_factory=AppConfig)

        @classmethod
        def from_dict(cls, config_dict):
            host_config = config_dict.get('host', {})
            app_config = config_dict.get('app', {})
            return cls(host=HostConfig(**host_config), app=AppConfig(**app_config))

3. Build the **`config`** object in **`main.py`**:

.. code-block:: python

    import os
    
    from application_framework.config.builder import ConfigBuilder
    from examples.single_app.config import Config


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

Create the application
----------------------

Create a simple "Hello World" application:

1. Create **`application.py`** in the **`src`** folder:

.. code-block:: python

    import time
    import asyncio

    from application_framework.service.service import Service
    from application_framework.messaging.message import Message

    from examples.single_app.config import AppConfig


    class Application(Service):
        def __init__(self, config: AppConfig):
            super().__init__()
            self.config = config
            self.crashed = False

        async def run_async(self):
            self.crashed = False
            while not self.stop_event.is_set():
                if self.crashed:
                    print(f"[Application] We have crashed..")
                    # Do nothing until framework takes action based on restart strategy.
                    await asyncio.sleep(1.0)
                else:
                    try:
                        print(f"[Application] {self.config.greeting}")
                        await asyncio.sleep(1.0)
                    except Exception as e:
                        self.crashed = True
                        await self.channels.service_to_supervisor.send_async(
                            Message(sender=self.service_id, content="crashed"),
                                self.loop,
                            )
                        print(f"[Application] Stopping..")
                        await self.channels.service_to_supervisor.send_async(
                            Message(sender=self.service_id, content="stopped"),
                                self.loop,
                            )

.. _userguide-build-application-object:

2. Build the **`application`** object in **`main.py`**:

.. code-block:: python

    # ...

    from application_framework.service.application.builder import ApplicationBuilder
    from application_framework.supervisor.restart_strategy import RestartStrategy
    from application_framework.service.execution_mode import ExecutionMode
    
    from examples.single_app.config import AppConfig
    from examples.single_app.src.application import Application
    from examples.single_app.src.greet_action import GreetAction

    def main():
      
        # ...

        application = (
            ApplicationBuilder()
                .set_name("Hello World")
                .set_root_directory(".")
                .add_route(protocol="http", path="/hello-world/?.*", port=config.app.port)
                .set_application_class(Application)
                .set_execution_mode(ExecutionMode.MAIN_EVENT_LOOP_ASYNC)
                .set_restart_strategy(RestartStrategy.EXPONENTIAL_BACKOFF)
                .register_instance(AppConfig, config.app)
                .register_transient(GreetAction)
                .build()
        )


Create the host
---------------

Configure and run the host to manage the application:

1. Build the **`host`** object in **`main.py`**:

.. code-block:: python

    # ...

    from application_framework.host.builder import HostBuilder

    def main():
      
        # ...

        host = (
            HostBuilder()
                .add_application(application)
                .set_listening_port(config.host.port)
                .build()
        )

        host.run()

.. _userguide-final-main-py:

The final main.py
-----------------

Here is the complete **`main.py`**:

.. code-block:: python

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
                .set_name("Hello World")
                .set_root_directory(".")
                .add_route(protocol="http", path="/hello-world/?.*", port=config.app.port)
                .set_application_class(Application)
                .set_execution_mode(ExecutionMode.MAIN_EVENT_LOOP_ASYNC)
                .set_restart_strategy(RestartStrategy.EXPONENTIAL_BACKOFF)
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

Running the host
----------------

To start the host, execute the main.py script. You can do this from your IDE or directly from the command line:

.. code-block:: bash

   $ python main.py

This command starts the host, which in turn runs your "Hello World" application.

That's it!
----------

This guide provides a quick start to using the py-application-framework. For more detailed information on each concept, refer to the corresponding pages in the menu.
