Setup Server
============


The ``gocd-tools setup server`` command is used as indicated to configure the designated GoCD server 
with the infomatation contained in the location configuration directory.::

    $ gocd-tools setup server --help
    usage: gocd-tools setup server [-h] {init,configure,wipe} ...

    optional arguments:
    -h, --help            show this help message and exit

    COMMAND:
    {init,configure,wipe}
        init                Initializes the server with an Authorization Configuration as defined in the local config directory's authorization_config.yml file.
        configure           Configures the designated GoCD server with the configuration files stored in the local config directory.
        wipe                Will wipe all the configuration settings defined in the local config directory on the GoCD server.

``init``
~~~~~~~~

This command initializes the designated GoCD server with an Authorization Configuration as indicated by the general help message.::

    $ gocd-tools setup server init
    Init server: https://gocd-server-url
    Failed to find: 401:{
    "message": "You are not authenticated!"
    }
    {
        "msg": "The Authorization config for: https://gocd-server-url was completed",
        "status": "success"
    }

``configure``
~~~~~~~~~~~~~

This command configures the designated GoCD server with the configuration.::

    $ gocd-tools setup server configure
    Authenticate
    Setup Roles
    Failed to find: 404:{"message":"Role with name \u0027manager\u0027 was not found!"}
    Creating: manager
    Re-Authenticate
    Setup Artifacts Config
    Setup Secret Configs
    Setup Cluster Profiles
    Failed to find: 404:{"message":"Cluster profile with id \u0027cluster\u0027 was not found!"}
    Creating: cluster
    Setup Elastic Agent Configs
    Failed to find: 404:{"message":"Elastic agent profile with id \u0027python\u0027 was not found!"}
    Creating: python
    Failed to find: 404:{"message":"Elastic agent profile with id \u0027docker\u0027 was not found!"}
    Creating: docker
    Setup Pipeline Group Configs
    Failed to find: 404:{"message":"Template with name \u0027docker_image\u0027 was not found!"}
    Creating: docker_image
    Failed to find: 404:{"message":"Template with name \u0027pypi_package\u0027 was not found!"}
    Creating: pypi_package
    Create Config Repositories
    Failed to find: 404:{"message":"Config repo with id \u0027gocd-tools\u0027 was not found!"}
    Creating: Spirits
    Failed to find: 404:{"message":"Config repo with id \u0027site\u0027 was not found!"}
    Creating: site
    {
        "msg": "Succesfully configured the https://gocd-server-url endpoint",
        "status": "success"
    }

``wipe``
~~~~~~~~

This command wipes the designated GoCD server configurations as defined in the location configuration directory.::

    $ gocd-tools setup server wipe
    Authenticate
    Delete Config Repositories
    Removing: gocd-tools
    Delete Template Configs
    Removing: notebook_image
    Removing: docker_image
    Delete Pipeline Config Groups
    Removing: csharp_package
    Delete Elastic Agent Configs
    Removing: python
    Removing: docker
    Delete Cluster Profiles
    Removing: cluster
    Delete Roles
    Removing: manager
    {
        "msg": "Succesfully finished the cleanup of endpoint: https://gocd-server-url",
        "status": "success"
    }