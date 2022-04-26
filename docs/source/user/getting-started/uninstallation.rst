Uninstall
=========

To uninstall the ``gocd-tools``, simply reverse the recommended ``pip install`` operation presented in the installation section::

    pip3 uninstall gocd-tools

This will remove the tool itself, but will not remove the associated configuration files that it uses to configure your GoCD server.
To remove these, removed the directory where the ``gocd-tools`` expects to find the configuration files.
By default, unless user customized, the expectation is that these will be located in the ``~/.gocd-tools/config`` path::

    rm -fr ~/.gocd-tools

After this, ``gocd-tools`` and its related files should be completely removed from your system.
