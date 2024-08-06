.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _basic-concepts-application:

Application
===========

Overview
--------

The `Application` class is a fundamental component within our framework, designed to manage the core functionality and lifecycle of your application. By extending the `Service` class, the `Application` class provides essential methods for synchronous and asynchronous operation, resource management, and handling application-specific tasks.

.. _basic-concepts-application-builder:

Application Builder
-------------------

The `ApplicationBuilder` class provides methods for configuring and building an `Application` instance. Here are the main methods you can use:

set_name(name)
~~~~~~~~~~~~~~

Sets the name of the application. This helps in identifying and managing the application within the framework.

set_root_directory(root_directory)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the root directory for the application. This is useful for setting the base path for configuration files, logs, and other resources.

.. _basic-concepts-application-builder-set-execution-mode:

set_execution_mode(execution_mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the execution mode of the application, such as synchronous or asynchronous. This ensures that the application runs in the intended manner, compatible with the framework's operational requirements. For more details on execution modes, see :ref:`basic-concepts-execution-mode`.

add_route(protocol, path, port)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds a route configuration for the application. This method allows you to specify the protocol (e.g., HTTP), path, and port for routing traffic to the application.

set_application_class(application_class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the class that defines the application logic. The provided class should extend the `Service` class and implement the necessary methods for running the application.

.. _basic-concepts-application-builder-set-restart-strategy:

set_restart_strategy(strategy, fixed_backoff_time=5, max_backoff_time=60, max_jitter=5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configures the restart strategy for the application. This includes setting parameters like fixed backoff time, maximum backoff time, and maximum jitter to ensure the application restarts efficiently in case of failures. For more details on restart strategies, see :ref:`basic-concepts-restart-strategy`.

register_instance(*args, **kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registers an instance of a class or component to be used within the application. This method is useful for dependency injection and managing application components.

register_transient(*args, **kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registers a transient dependency, which ensures that a new instance is created each time it is requested.

register_scoped(*args, **kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registers a scoped dependency, which ensures that a single instance is created and shared within a specific scope.

register_singleton(*args, **kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registers a singleton dependency, which ensures that a single instance is created and shared across the entire application.

register_factory(*args, **kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registers a factory method for creating dependencies. This is useful for managing complex dependencies that require custom instantiation logic.

build()
~~~~~~~

Constructs and returns an `Application` instance based on the configurations provided. This method finalizes the setup and prepares the application for integration into the host environment.

.. note::

   For a detailed example of how to use the `ApplicationBuilder`, refer to the :ref:`Getting Started Guide <userguide-build-application-object>`.

Run Methods
-----------

An `Application` class must implement either the `run` method for synchronous operation or the `run_async` method for asynchronous operation, depending on the execution mode.

.. note::

   You only need to implement one of these methods (`run` or `run_async`) based on the chosen execution mode. For more information, see :ref:`basic-concepts-execution-mode`.

run()
~~~~~

This method contains the synchronous execution logic of the application. It runs in a loop until the `cancellation_token` is set, indicating that the framework has instructed the application to stop.

Example:

.. code-block:: python

   def run(self):
       self.crashed = False
       while not self.cancellation_token.is_set():
           if self.crashed:
               print(f"[Application] Application has crashed!")
               time.sleep(1.0)
           else:
               try:
                   print(f"[Application] Hello from application")
                   time.sleep(1.0)
               except Exception as e:
                   self.crashed = True
                   self.channels.service_to_supervisor.send(
                       Message(sender=self.service_id, content="crashed")
                   )
       print(f"[Application] Application was instructed to stop")
       self.channels.service_to_supervisor.send(
           Message(sender=self.service_id, content="stopped")
       )

run_async()
~~~~~~~~~~~

This method contains the asynchronous execution logic of the application. It runs in a loop until the `cancellation_token` is set, indicating that the framework has instructed the application to stop.

Example:

.. code-block:: python

   async def run_async(self):
       self.crashed = False
       while not self.cancellation_token.is_set():
           if self.crashed:
               print(f"[Application] Application has crashed!")
               await asyncio.sleep(1.0)
           else:
               try:
                   print(f"[Application] Hello from application")
                   await asyncio.sleep(1.0)
               except Exception as e:
                   self.crashed = True
                   await self.channels.service_to_supervisor.send_async(
                       Message(sender=self.service_id, content="crashed"),
                       self.loop,
                   )
       print(f"[Application] Application was instructed to stop")
       await self.channels.service_to_supervisor.send_async(
           Message(sender=self.service_id, content="stopped"),
           self.loop,
       )

Cancellation Token
------------------

The `cancellation_token` is a flag used to signal the application to stop. The framework sets this token when it instructs the application to stop running. Your application's `run` or `run_async` method should periodically check this token and gracefully exit the loop when it is set.

Example:

.. code-block:: python

   if self.cancellation_token.is_set():
       break

Each of these sections provides detailed information on how to implement and manage the `Application` class within the framework, ensuring that it operates efficiently and effectively within your deployment environment.
