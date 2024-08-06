.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _configuration-system:

Configuration System
====================

The configuration system in our application framework is designed to be highly flexible and capable of loading settings from various sources. This document provides an overview of the configuration system, including how to use it in your application.

Overview
--------

The configuration system is built using the `ConfigBuilder` class, which allows for the loading and processing of configuration data from multiple sources, including environment variables, YAML files, JSON files, INI files, and more. This system also supports type conversion and nested configuration structures.

Configuration Sources
---------------------

The `ConfigBuilder` class supports the following configuration sources:

- **YAML Files:** Add a YAML file as a configuration source using the `add_yaml_file` method.
- **JSON Files:** Add a JSON file as a configuration source using the `add_json_file` method.
- **INI Files:** Add an INI file as a configuration source using the `add_ini_file` method.
- **Environment Variables:** Load environment variables with a specified prefix using the `add_prefixed_env_vars` method.
- **Profiled Files:** Load files based on the current environment profile using the `add_profiled_file` method.

.. note::

   YAML and JSON files inherently support various data types such as strings, numbers, booleans, lists, and dictionaries. INI files and environment variables primarily store values as strings, but type conversion can be applied to map these strings to the appropriate types.

.. note::
   
   The configuration sources are applied in the order they are added to the `ConfigBuilder`. This means that later sources can override values from earlier sources. Understanding this order is crucial for ensuring the correct configuration values are used.

Example Usage
-------------

Below is an example of how to create a configuration object using the configuration builder.

.. code-block:: python

    import os
    
    from application_framework.config.builder import ConfigBuilder
    from examples.single_app.config import Config

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


Configuration Builder Methods
-----------------------------

**`set_environment_profile(env)`**

Sets the environment profile for the configuration. This can be used to load different configurations based on the environment (e.g., development, staging, production).

**`add_yaml_file(path)`**

Adds a YAML file as a configuration source. The path to the file should be provided.

**`add_json_file(path)`**

Adds a JSON file as a configuration source. The path to the file should be provided.

**`add_ini_file(path)`**

Adds an INI file as a configuration source. The path to the file should be provided.

**`add_prefixed_env_vars(prefix, section_separator=".")`**

Loads environment variables with the specified prefix. The `section_separator` can be used to denote nested configuration keys.

**`add_profiled_file(template)`**

Loads a configuration file based on the current environment profile. The template should include `{profile}` which will be replaced with the current environment profile.

**`set_type_conversion(key, type_func)`**

Sets a type conversion function for a specific configuration key. This is useful for converting strings to other types such as integers or booleans.

**`bind(config_class)`**

Binds the configuration data to a specified data class. This allows for strong typing and easy access to configuration values.

**`build()`**

Builds and returns the configuration object.

Data Binding with Config Classes
--------------------------------

The framework uses data classes to define the structure of the configuration and to facilitate data binding. Below are the data classes used in the example:

.. code-block:: python

   from dataclasses import dataclass, field

   @dataclass
   class HostConfig:
       port: int = 80

   @dataclass
   class AppConfig:
       port: int = 5000

   @dataclass
   class Config:
       host: HostConfig = field(default_factory=HostConfig)
       app: AppConfig = field(default_factory=AppConfig)

       @classmethod
       def from_dict(cls, config_dict):
           host_config = config_dict.get('host', {})
           app_config = config_dict.get('app', {})
           return cls(host=HostConfig(**host_config), app=AppConfig(**app_config))

.. tip::

   While you can define your own structure for the `Config` class, it is recommended to include at least a `HostConfig` and an `AppConfig` at the top level. This helps in organizing configuration settings effectively and ensures clarity in your configuration structure.

In this example, `HostConfig` and `AppConfig` are used to define the structure of the host and application configurations, respectively. The `Config` class combines these into a single configuration object. By using the `ConfigBuilder` to bind configuration data to these data classes, the framework ensures that the configuration data is consistently and correctly mapped to the expected structure, enabling automatic synchronization and type-safe access to configuration settings.
