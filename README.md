[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml)

> **⚠️ Note:** This framework is still in the alpha release stage. Expect potential changes and improvements in future releases.

## py-application-framework

A prototypical application framework for Python.

## Features:

- **Builder Pattern:** The framework incorporates the builder pattern to facilitate the assembly of a Host that accommodates multiple Applications. This approach ensures a structured and efficient setup process.

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

from application_framework.application.builder import ApplicationBuilder
from application_framework.config.builder import ConfigBuilder
from application_framework.host.builder import HostBuilder
from application_framework.host.restart_policy import RestartPolicy

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

    application = (
        ApplicationBuilder()
        .set_config(config)
        .set_root_directory(".")
        .use_entry_point("app:run")
        .run_in_separate_process()
        .add_http_route(path="/app/?.*", port=config.app.port)
        .add_websocket_route(path="/app/ws/?.*", port=config.app.port + 9)
        .build()
    )

    host = (
        HostBuilder()
        .add_application(application)
        .set_restart_policy(RestartPolicy.ExponentialBackoff)
        .set_listening_port(config.host.port)
        .build()
    )

    host.run()


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

### [1.0.0-alpha.1](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.1) (2024-06-07)

- Initial alpha release.
- ConfigBuilder: Introduces a flexible and extensible way to handle application configuration, supporting multiple sources such as YAML, JSON, INI, and environment variables, with type conversion and binding capabilities. Configurations can be overridden from multiple sources to provide maximum flexibility.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.

---

This README reflects the current state of the project and will be updated with new features and improvements in future releases. Stay tuned for updates!
