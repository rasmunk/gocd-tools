Configuration Files
===================

.. _target configuration files:

The `gocd-tools` tool relies solely on YAML configuration files to configure a particular GoCD server.
When a particular configuration operation is executed, the `gocd-tools` expects to find a related configuration file
in the ``~/.gocd-tools/config`` directory.

The names of these files is related to the config operation it :ref:`GoCD Type that this tool supports <target supported types>`.
