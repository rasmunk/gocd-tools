Setup Secrets
=============

The ``gocd-tools setup secrets`` command is used as indicated to setup `Secrets <https://docs.gocd.org/current/configuration/secrets_management.html>`_ on the designated GoCD server.::

    usage: gocd-tools setup secrets [-h] {init,configure,delete} ...

    optional arguments:
    -h, --help            show this help message and exit

    COMMAND:
    {init,configure,delete}
        init                Initializes the secrets db directory where the GoCD secrets will be stored.
        configure           Configure the GoCD server with the secrets defined in the secrets db directory.
        delete              Delete the secrets db directory.

``init``
~~~~~~~~

This command initializes the directory where the GoCD secrets will be stored.
This means that it will create the directory path if it doesn't already exist.::

    $ gocd-tools setup secrets init
    {
        "msg": "Created: /gosecret",
        "status": "success"
    }

``configure``
~~~~~~~~~~~~~

This command configures the designated GoCD server with the secrets located in
the initialized go secret db. Therefore you need to move your secrets into this directory
before the command is executed. The tool specifically requires the `Secret Configs`_ configuration
to configure the secrets::

    $ gocd-tools secrets configure
    Assigned key: username to secret db: /gosecret/github.json, with output:
    ...
    {
        "msg": "The secrets db at: /gosecret/secrets.yml was used to configure the server",
        "status": "success"
    }

``delete``
~~~~~~~~~~

This command recursively deletes the intialized secrets db directory.::

    $ gocd-tools setup secrets delete
    {
        "msg": "Removed directory: /gosecret",
        "status": "success"
    }
