.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _configuration-system:

Host
====

Overview
--------

The ``Host`` class is essential for managing the deployment and lifecycle of your applications. It handles resource management, ensuring the proper setup, teardown, and cleanup of event loops, threads, tasks, and processes. The ``Host`` also oversees application lifecycle management, including restarts based on the specified restart strategy, ensuring robustness and resilience. Additionally, it manages routing, directing traffic from the specified container port to your applications as configured.

Host Builder
------------

The ``HostBuilder`` class provides methods for configuring and building the ``Host`` instance. Here are the main methods you can use:

add_application(application)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds an application to the host configuration. You need to provide an ``application`` instance, which is created using the ``ApplicationBuilder.build()`` method. This instance describes how the application should be set up and managed within the host.

.. note::

   The ``application`` parameter is actually a ``ServiceConfig`` object, which encapsulates all the necessary information for the ``Host`` to correctly initialize and manage the application. This abstraction helps simplify the user experience.

set_listening_port(listening_port)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the port on which the host will listen for incoming traffic. This port is used to route traffic to the applications based on the configuration.

build()
~~~~~~~

Constructs and returns an instance of the ``Host`` class based on the configurations provided. This method finalizes the setup and prepares the ``Host`` for running the applications.

Each of these methods allows you to customize the host to suit the needs of your applications, ensuring that it operates efficiently and effectively within your deployment environment.
