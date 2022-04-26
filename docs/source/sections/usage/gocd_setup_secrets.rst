Setup Secrets
=============

The ``gocd-tools setup secrets`` command is used as indicated to setup secrets on a GoCD server.

    $ gocd-tools setup secrets --help
    usage: gocd-tools setup secrets [-h] {init,configure,del} ...

    optional arguments:
    -h, --help            show this help message and exit

    COMMAND:
    {init,configure,del}


``init``

This command initializes the directory where the GoCD secrets will be stored.
This means that it will create the directory path if it doesn't already exist.



``configure``


``delete``

