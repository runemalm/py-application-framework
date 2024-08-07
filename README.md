
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml)

> **⚠️ Note:** This framework is still in the alpha release stage. Expect potential changes and improvements in future releases.

## py-application-framework

An application framework for Python.

## Purpose

The purpose of the `py-application-framework` is to provide a flexible, easy-to-use, and extensible framework for building Python applications. By leveraging standard design patterns, this framework aims to cater to both beginners and professional developers, helping them to create robust applications with minimal effort. The framework's design choices emphasize simplicity, readability, and maintainability, making it an ideal choice for developers looking to adhere to best practices in software development.

## Key Advantages

- **Standard Design Patterns:** The framework employs well-known design patterns, making it intuitive for developers familiar with these patterns. This approach ensures that the framework is accessible to beginners while being powerful enough for professional developers.
- **Ease of Use:** With a focus on simplicity and ease of use, `py-application-framework` allows developers to quickly set up and configure their applications without getting bogged down by complex setup procedures.
- **Extensibility:** The framework is designed to be highly extensible, allowing it to evolve and adapt to new requirements and technologies over time.
- **Maintainability:** By following best practices and using standard design patterns, the framework promotes maintainable code, reducing the long-term cost of ownership for applications built with it.
- **Flexibility:** Supports multiple configuration sources (e.g., YAML, JSON, INI, environment variables) with the ability to override settings from different sources, providing maximum flexibility in configuration management.
- **Dependency Management:** Supports dependency containers, facilitating dependency injection and inversion of control, which enhances modularity, testability, and overall flexibility in managing dependencies.

## Compatibility

The library is compatible with the following Python versions:

- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

## Installation

```bash
$ pip install py-application-framework
```
  
## Quick Start

Here's a quick example to get you started:

```python
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
```

## Documentation

For more advanced usage and examples, please visit our [readthedocs](https://py-application-framework.readthedocs.io/en/latest/) page.

## License

`py-application-framework` is released under the GPL 3 license. See [LICENSE](LICENSE) for more details.

## Source Code

You can find the source code for `py-application-framework` on [GitHub](https://github.com/runemalm/py-application-framework).

## Release Notes

### [1.0.0-alpha.5](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.5) (2024-08-06)

- **New Host Builder Class:** Introduced the Host Builder class for improved host configuration and management.
- **Restart Strategies:** Introduced restart strategies to handle application crashes, enhancing reliability and stability.
- **Execution Modes:** Introduced execution modes allowing the application to run in separate thread, process or the event loop. Both asynchronous and synchronous support.
- **Cancellation Token Pattern:** Implemented the cancellation token pattern to enable graceful stopping of applications.
- **Documentation Updates:** Added more documentation on the basic concepts of the framework. Introduced a comprehensive "Getting Started" guide to help new users quickly onboard.
- **Refactored Internals Architecture:** Introduced several significant changes, including a clearer expression of the actor model. Refactored actors into coroutines and utilized the event loop in a more idiomatic manner. Simplified code design, including removal of the **`Executor`** classes.

### [1.0.0-alpha.4](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.4) (2024-06-17)

- **Internals Documentation:** Added comprehensive documentation detailing the internal architecture of the framework, including basic concepts, the executor model, and the use of processes, threads, and coroutines.

### [1.0.0-alpha.3](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.3) (2024-06-08)

- **New ApplicationBuilder Class:** Introduced the ApplicationBuilder class for a more streamlined and structured application setup.
- **Dependency Injection Support:** Now using a dependency container for improved dependency injection throughout the application.
- **Bug Fix:** Fixed an issue with the default initialization of dataclass fields in Python 3.11 and above.

### [1.0.0-alpha.2](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.2) (2024-06-07)

- **New ConfigBuilder Class:** Introduced the ConfigBuilder class to handle application configuration flexibly and extensibly, supporting multiple sources such as YAML, JSON, INI, and environment variables, with type conversion and binding capabilities.
- **Basic Documentation:** Provided an initial set of documentation to give users an introduction to the library.
- **License:** Released under the GPL 3 license.
- **Initial Alpha Release:** Marked the initial alpha release of the framework.

---

This README reflects the current state of the project and will be updated with new features and improvements in future releases. Stay tuned for updates!
