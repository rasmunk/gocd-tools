Configuration
=============

The gocd-tools have to be properly configured before it can be effectively used.
Most importantly, it relies on that the config you want to apply to a particular GoCD server is stored
in the relative user directory path ``~/.gocd-tools/config``. In this directory, the tool expects to find a set of YAML files
that define the configuration that it should apply to the GoCD server in question. 

An explanation of the different configuration files can be seen in :ref:`Configuration Files <target configuration files>`.

.. toctree::
    :maxdepth: 2

    config_files