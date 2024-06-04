[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Master workflow](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-application-framework/actions/workflows/master.yml)

## py-application-framework

A prototypical application framework for Python.

### Features:

- **Builder Pattern:** The framework incorporates the builder pattern to facilitate the assembly of a Host that accommodates multiple Applications. This approach ensures a structured and efficient setup process.
- **Dependency Management:** Features an integrated dependency container that automates the management and injection of dependencies. This functionality streamlines object creation and configuration, enhancing simplicity and maintainability.
- **Proven Design Principles:** Adopts established design patterns recognized by the Gang of Four, along with hexagonal architecture and domain-driven design approaches. These principles are foundational in crafting robust, maintainable code that stands the test of time.
- **Simplicity First:** Prioritizes a straightforward approach to coding by deliberately avoiding complex features like asyncio and type hinting, fostering code that is both accessible and easy to understand.

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
# file: main.py

from application_framework.application.builder import ApplicationBuilder
from application_framework.architecture import Architecture
from application_framework.execution_unit import ExecutionUnit
from application_framework.host.builder import HostBuilder
from application_framework.infrastructure.builder import InfrastructureBuilder

if __name__ == '__main__':

    infrastructure = InfrastructureBuilder() \
        .add_proxy(80) \
        .add_service(name="service_a", excecution_unit=ExecutionUnit.Process) \
        .add_service(name="service_b", excecution_unit=ExecutionUnit.Thread) \
        .add_service(name="service_c", excecution_unit=ExecutionUnit.Coroutine) \
        .add_route(path="a/.*", service_name="service_a") \
        .add_route(path="b/.*", service_name="service_b") \
        .add_route(path="c/.*", service_name="service_c") \
        .add_database() \
        .build()

    application_a = ApplicationBuilder() \
        .set_architecture(Architecture.Hexagonal) \
        .set_root_directory(".") \
        .set_main_script("hexagonal_main.py") \
        .build()

    application_b = ApplicationBuilder() \
        .set_architecture(Architecture.Script) \
        .set_root_directory(".") \
        .set_main_script("main.py") \
        .build()

    application_c = ApplicationBuilder() \
        .set_architecture(Architecture.Script) \
        .set_root_directory(".") \
        .set_main_script("async_main.py") \
        .build()

    host = HostBuilder() \
        .set_infrastructure(infrastructure) \
        .add_application(app=application_a, service_name="service_a") \
        .add_application(app=application_b, service_name="service_b") \
        .add_application(app=application_c, service_name="service_c") \
        .build() \
        .run()
```

## Documentation

For more advanced usage and examples, please visit our [readthedocs](https://py-application-framework.readthedocs.io/en/latest/) page.

## License

`py-application-framework` is released under the GPL 3 license. See [LICENSE](LICENSE) for more details.

## Source Code

You can find the source code for `py-application-framework` on [GitHub](https://github.com/runemalm/py-application-framework).

## Release Notes

### [1.0.0-alpha.1](https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.1) (2024-06-xx)

- Initial alpha release.
- Added Host Builder: The library includes a dependency container for managing object dependencies.
- Basic Documentation: An initial set of documentation is provided, giving users an introduction to the library.
- License: Released under the GPL 3 license.
