.. warning::

   This library is currently in the alpha stage of development. Expect changes and improvements as we work towards a stable release.

.. _basic-concepts-restart-strategy:

Restart Strategy
================

Overview
--------

In `py-application-framework`, ``RestartStrategy`` defines various strategies to handle application restarts after failures. The framework provides different backoff strategies to control the delay before an application is restarted, enhancing the system's resilience. For information on how to set the restart strategy, see the :ref:`ApplicationBuilder <basic-concepts-application-builder-set-restart-strategy>` page.

Restart Strategies
------------------

The framework includes the following strategies:

``IMMEDIATE``
~~~~~~~~~~~~~
Restarts the application immediately without any delay.

``FIXED_BACKOFF``
~~~~~~~~~~~~~~~~~
Waits for a fixed amount of time before restarting the application. The delay is specified by the ``fixed_backoff_time`` parameter.

``EXPONENTIAL_BACKOFF``
~~~~~~~~~~~~~~~~~~~~~~~
Increases the delay between restarts exponentially up to a maximum limit, helping to avoid overwhelming the system. The initial delay is 1 second, and the maximum is specified by the ``max_backoff_time`` parameter. Additionally, jitter is configurable via the ``max_jitter`` parameter.

``LINEAR_BACKOFF``
~~~~~~~~~~~~~~~~~~
Increases the delay between restarts linearly up to a maximum limit. The initial delay is 1 second, and the maximum is specified by the ``max_backoff_time`` parameter.

Conclusion
----------

The `py-application-framework` provides various strategies to manage application restarts, offering flexibility in handling application failures and enhancing system resilience. By choosing the appropriate restart strategy and configuring your application using the `ApplicationBuilder` methods, you can optimize the reliability and performance of your application. For more details on setting the restart strategy, see the :ref:`ApplicationBuilder <application-builder>` page.
