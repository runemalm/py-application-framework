.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

###############
Version History
###############

**1.0.0-alpha.5 (2024-08-06)**

- **New Host Builder Class:** Introduced the Host Builder class for improved host configuration and management.
- **Restart Strategies:** Introduced restart strategies to handle application crashes, enhancing reliability and stability.
- **Execution Modes:** Introduced execution modes allowing the application to run in separate thread, process or the event loop. Both asynchronous and synchronous support.
- **Cancellation Token Pattern:** Implemented the cancellation token pattern to enable graceful stopping of applications.
- **Documentation Updates:** Added more documentation on the basic concepts of the framework. Introduced a comprehensive "Getting Started" guide to help new users quickly onboard.
- **Refactored Internals Architecture:** Introduced several significant changes, including a clearer expression of the actor model. Refactored actors into coroutines and utilized the event loop in a more idiomatic manner. Simplified code design, including removal of the **`Executor`** classes.

`View release on GitHub <https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.5>`_

**1.0.0-alpha.4 (2024-06-17)**

- **Internals Documentation:** Added comprehensive documentation detailing the internal architecture of the framework, including basic concepts, the executor model, and the use of processes, threads, and coroutines.

`View release on GitHub <https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.4>`_

**1.0.0-alpha.3 (2024-06-08)**

- **New ApplicationBuilder Class:** Introduced the ApplicationBuilder class for a more streamlined and structured application setup.
- **Dependency Injection Support:** Now using a dependency container for improved dependency injection throughout the application.
- **Bug Fix:** Fixed an issue with the default initialization of dataclass fields in Python 3.11 and above.

`View release on GitHub <https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.3>`_

**1.0.0-alpha.2 (2024-06-07)**

- **New ConfigBuilder Class:** Introduced the ConfigBuilder class to handle application configuration flexibly and extensibly, supporting multiple sources such as YAML, JSON, INI, and environment variables, with type conversion and binding capabilities.
- **Basic Documentation:** Provided an initial set of documentation to give users an introduction to the library.
- **License:** Released under the GPL 3 license.
- **Initial Alpha Release:** Marked the initial alpha release of the framework.

`View release on GitHub <https://github.com/runemalm/py-application-framework/releases/tag/v1.0.0-alpha.2>`_
