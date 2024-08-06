.. warning::

   This framework is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

py-application-framework
=======================

An application framework for Python.

Purpose
-------

The purpose of the py-application-framework is to provide a flexible, easy-to-use, and extensible framework for building Python applications. By leveraging standard design patterns, this framework aims to cater to both beginners and professional developers, helping them to create robust applications with minimal effort. The framework's design choices emphasize simplicity, readability, and maintainability, making it an ideal choice for developers looking to adhere to best practices in software development.

Key Advantages
--------------

- **Standard Design Patterns:** The framework employs well-known design patterns, making it intuitive for developers familiar with these patterns. This approach ensures that the framework is accessible to beginners while being powerful enough for professional developers.
- **Ease of Use:** With a focus on simplicity and ease of use, py-application-framework allows developers to quickly set up and configure their applications without getting bogged down by complex setup procedures.
- **Extensibility:** The framework is designed to be highly extensible, allowing it to evolve and adapt to new requirements and technologies over time.
- **Maintainability:** By following best practices and using standard design patterns, the framework promotes maintainable code, reducing the long-term cost of ownership for applications built with it.
- **Flexibility:** Supports multiple configuration sources (e.g., YAML, JSON, INI, environment variables) with the ability to override settings from different sources, providing maximum flexibility in configuration management.
- **Dependency Management:** Supports dependency containers, facilitating dependency injection and inversion of control, which enhances modularity, testability, and overall flexibility in managing dependencies.

.. userguide-docs:
.. toctree::
  :maxdepth: 1
  :caption: User Guide

  userguide

.. basic-concepts-docs:
.. toctree::
  :maxdepth: 1
  :caption: Basic Concepts

  basic_concepts/host
  basic_concepts/application
  basic_concepts/execution_modes
  basic_concepts/restart_strategies

.. core-systems-docs:
.. toctree::
  :maxdepth: 1
  :caption: Core Systems

  core_systems

.. .. examples-docs:
.. .. toctree::
..   :maxdepth: 1
..   :caption: Examples

..   examples/single_application
..   examples/multi_application

.. internals-docs:
.. toctree::
  :maxdepth: 1
  :caption: Internals

  .. internals/design_philosophy
  internals/the_internal_architecture
  .. internals/how_to_submit
  .. internals/design_patterns

.. releases-docs:
.. toctree::
  :maxdepth: 1
  :caption: Releases

  releases

.. .. apireference-docs:
.. .. toctree::
..   :maxdepth: 1
..   :caption: API Reference

..   py-modindex

You can find the source code for `py-application-framework` in our `GitHub repository <https://github.com/runemalm/py-application-framework>`_.
