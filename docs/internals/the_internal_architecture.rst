.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.
   
Internal Architecture Overview
==============================

This section provides an overview of the framework's internal architecture.

.. image:: /_static/internals/architecture/actor_model.png
   :alt: The actor model.
   :align: right
   :width: 200

We utilize the actor model, where the primary components are actors that communicate by sending messages to each other.

Queues are established between the host and each supervisor, and each supervisor has its own queue with the service it manages.

Additionally, we use the event loop in an idiomatic Python manner. This involves using executors to set up any threads or processes the application requires, with the asyncio library handling the setup, management, and teardown. This approach allows us to focus on tasks within the main event loop, further simplifying the design.


Actors
------

The following concepts are central to our architecture:

.. image:: /_static/internals/architecture/actors.png
   :alt: The actors in the system.
   :align: right

- **Host:** Manages one or more supervisors.
- **Supervisor:** Oversees a service, handling its lifecycle (start, stop, restart) with various strategies.
- **Service:** Represents the main unit of work managed and executed within the framework (the *Application* in the public API).

We use the observer pattern for component notifications on state changes. For instance, if a service crashes, it notifies the executor via an event mechanism.

.. raw:: html

   <div style="clear: both;"></div>


Actor Messages
--------------

These are the messages that are communicated between the actors as part of controling the applications' lifecycles.

.. image:: /_static/internals/architecture/actor_messages.png
   :alt: The messages sent between the actors.
   :align: left

.. raw:: html

   <div style="clear: both;"></div>


Tasks, Processes, and Threads
-----------------------------

This example shows a host configured with five applications, each utilizing one of the five execution modes. It effectively demonstrates how each execution mode impacts the final resource setup.

.. image:: /_static/internals/architecture/resource_scheduling.png
   :alt: Example of the tasks, processes, and threads created for applications in each of the five execution modes.
