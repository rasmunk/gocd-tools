Intro
=====

The ``gocd-tools`` CLI is designed to function as a regular CLI.
To get general information or receive help at any level of the CLI tree, the ``-h`` argument is always a good place to go.

For instance, to simply get started, this could be the first thing we could try out as our base argument::

    $ gocd-tools -h
    usage: gocd-tools [-h] {setup} ...

    options:
    -h, --help  show this help message and exit

    COMMAND:
    {setup}

As we can see from the output, the only base command that the ``gocd-tools`` accept at the moment is the ``setup`` command.
So, we see what this ``setup`` command can provide us::

    $ gocd-tools setup -h
    usage: gocd-tools setup [-h] {secrets,server} ...

    options:
    -h, --help        show this help message and exit

    COMMAND:
    {secrets,server}

Next, we can see that the ``gocd-tools setup`` command can enable us to execute commands that are related to ``secrets`` and ``server``.
To explore these commands in details about how they are used and what they can do for us. Continue reading in the :doc:`/user/usage/gocd_setup_secrets` and :doc:`/user/usage/gocd_setup_server` sections.