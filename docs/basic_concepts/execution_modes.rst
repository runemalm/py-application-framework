.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _basic-concepts-execution-mode:

Execution Mode
==============

Overview
--------

In `py-application-framework`, ``ExecutionMode`` defines the various modes in which an application or service can be executed. The ``ExecutionMode`` enum provides different strategies to manage the concurrency and parallelism of services, ensuring flexibility in how services are deployed and executed. For information on how to set the execution mode, see the :ref:`ApplicationBuilder <basic-concepts-application-builder-set-execution-mode>` page.

Execution Modes
---------------

The ``ExecutionMode`` enum includes the following values:

- ``MAIN_EVENT_LOOP_ASYNC``
- ``SEPARATE_THREAD``
- ``SEPARATE_THREAD_ASYNC``
- ``SEPARATE_PROCESS``
- ``SEPARATE_PROCESS_ASYNC``

``MAIN_EVENT_LOOP_ASYNC``
~~~~~~~~~~~~~~~~~~~~~~~~~
Executes the service within the main event loop of the application. This mode is ideal for asynchronous tasks that do not require isolation from the main application flow. The service runs concurrently with other asynchronous tasks in the main loop.

``SEPARATE_THREAD``
~~~~~~~~~~~~~~~~~~~
Executes the service in a separate thread. This mode is useful for CPU-bound tasks that need to run concurrently with other services without blocking the main event loop. However, care must be taken to manage thread safety and avoid race conditions.

``SEPARATE_THREAD_ASYNC``
~~~~~~~~~~~~~~~~~~~~~~~~~
Executes the service in a separate thread with its own event loop. This mode combines the benefits of separate threading with asynchronous execution. It is suitable for services that require asynchronous operations but need isolation from the main event loop.

``SEPARATE_PROCESS``
~~~~~~~~~~~~~~~~~~~~
Executes the service in a separate process. This mode is ideal for tasks that require full isolation from the main application due to resource-intensive operations or potential instability. Inter-process communication is necessary to manage coordination between processes.

``SEPARATE_PROCESS_ASYNC``
~~~~~~~~~~~~~~~~~~~~~~~~~~
Executes the service in a separate process with its own event loop. This mode is similar to ``SEPARATE_THREAD_ASYNC`` but with the added isolation and resource management benefits of separate processes. It is suitable for highly isolated asynchronous operations.

Conclusion
----------

The ``ExecutionMode`` enum provides flexibility in how services are executed, allowing for various concurrency and parallelism strategies. By choosing the appropriate execution mode, you can optimize the performance and resource utilization of your application.
