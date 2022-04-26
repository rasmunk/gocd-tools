Configuration Files
===================

.. _target configuration files:

The ``gocd-tools`` tool relies solely on YAML configuration files to configure a particular GoCD server.
When a particular configuration operation is executed, the `gocd-tools` expects to find a related configuration file
in the ``~/.gocd-tools/config`` directory.

The names of these files is related to the config operation it :ref:`GoCD Type that this tool supports <target supported types>`.

.. _Artifacts Config: https://api.gocd.org/current/#artifacts-config
.. _Artifacts Config Object: https://api.gocd.org/current/#the-artifacts-config-object
.. _Artifacts Config File:

``artifacts_config.yml``
~~~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Artifacts Config`_ configuration.
The structure of this file is expected to abide by the format defined the GoCD API for an `Artifacts Config Object`_.
An example configuration of this could be::

    artifacts_dir: artifacts
    purge_settings:
        purge_start_disk_space: 5
        purge_upto_disk_space: 20


.. _Cluster Profiles: https://api.gocd.org/current/#cluster-profiles
.. _Cluster Profile Object: https://api.gocd.org/current/#the-cluster-profile-object
.. _Cluster Profiles File:

``cluster_profiles.yml``
~~~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Cluster Profiles`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Cluster Profile Object`_ format.
An example configuration of this could be::

  - id: "cluster"
    plugin_id: "cd.go.contrib.elastic-agent.docker-swarm"
    properties:
        - key: "go_server_url"
        value: "https://gocd-server-url/go"
        - key: "auto_register_timeout"
        value: "40"
        - key: "max_docker_containers"
        value: "200"
        - key: "docker_uri"
        value: "unix:///var/run/docker.sock"


.. _Config Repo: https://api.gocd.org/current/#config-repo
.. _Config Repo Object: https://api.gocd.org/current/#the-config-repo-object
.. _Config Repo File:

``config_repositories.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Config Repo`_ configurations.
The structure of this file is three-fold. First the ``id`` key-value pair is used to set a unique identifer for the `Config Repo`_ in question.
Second, then ``authentication`` section is used to define whether any form of authentication is required to access the designated `Config Repo`_.
An example of this could be that the designated `Config Repo`_ is a private GitHub repository that requires authentication.
To use ``authentication``, the ``gocd-tools`` expects this to be provided by a `Secret Config`_, which an example of can be seen below in the `secret_configs.yml`_ section.
Thirdly, the ``config`` section is passed directly as the `Config Repo`_ to be created.
An example configuration of this could be::

  - id: gocd-tools
    authentication:
        required: no
    config:
        plugin_id: yaml.config.plugin
        material:
            type: git
            attributes:
            url: https://github.com/rasmunk/gocd-tools
            branch: main
            auto_update: true
        rules:
            - directive: allow
            action: refer
            type: "*"
            resource: "*"

.. _Elastic Agent Profiles: https://api.gocd.org/current/#elastic-agent-profiles
.. _Elastic Agent Profile Object: https://api.gocd.org/current/#the-elastic-agent-profile-object
.. _Elastic Agent Profiles File:

``elastic_agent_profiles.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Elastic Agent Profiles`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Elastic Agent Profile Object`_ format.
An example configuration of this could be::

  - id: "python"
    cluster_profile_id: "cluster"
    properties:
      - key: "Image"
        value: "ucphhpc/gocd-agent-python:latest"
      - key: "MaxMemory"
        value: "5G"
      - key: "ReservedMemory"
        value: "1G"
      - key: "Networks"
        value: nginx_default
      - key: "Constraints"
        value: node.role == worker


.. _Pipeline Group Config: https://api.gocd.org/current/#pipeline-group-config
.. _Pipeline Group Config Object: https://api.gocd.org/current/#the-pipeline-group-object
.. _Pipeline Group Config File:

``pipeline_group_configs.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Pipeline Group Config`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Pipeline Group Config Object`_ format.
An example configuration of this could be::

  - name: bare_metal_pypi_package
    authorization:
        operate:
        roles:
            - manager

.. _Roles: https://api.gocd.org/current/#roles
.. _Roles Object: https://api.gocd.org/current/#the-role-object
.. _Roles File:

``roles.yml``
~~~~~~~~~~~~~

This file contains the `Roles`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Roles Object`_ format.
An example configuration of this could be::

  - name: manager
    type: plugin
    attributes:
      auth_config_id: github
      properties:
      - key: "Organizations"
          value: "ucphhpc"
    policy:
      - permission: allow
        action: administer
        type: "*"
        resource: "*"


.. _Secret Configs: https://api.gocd.org/current/#template-configs
.. _Secret Config Object: https://api.gocd.org/current/#the-secret-config-object
.. _Secret Config File:

``secret_configs.yml``
~~~~~~~~~~~~~~~~~~~~~~

This file contains the `Secret Configs`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Secret Config Object`_ format.
An example configuration of this could be::

  - id: "common"
    plugin_id: "cd.go.secrets.file-based-plugin"
    description: "File store for secrets"
    properties:
      - key: "SecretsFilePath"
        value: "/gosecret/common.json"
    rules:
      - directive: allow
        action: refer
        type: "*"
        resource: "*"


.. _Template Configs: https://api.gocd.org/current/#template-configs
.. _Template Config Object: https://api.gocd.org/current/#get-template-config
.. _Template COnfig File:

``templates.yml``
~~~~~~~~~~~~~~~~~

This file contains the `Template Configs`_ configurations.
The structure of this file is expected to abid by the formated expected by the `Template Config Object`_ format.
An example configuration of this could be::

  - name: "docker_image"
    stages:
      - name: "build"
        fetch_materials: true
        keep_artifacts: true
        jobs:
          - name: "build"
            elastic_profile_id: "docker"
            timeout: 0
            tasks:
              - type: "exec"
                attributes:
                  command: make
                  arguments:
                  - IMAGE=#{IMAGE}
                  - ARGS=#{ARGS}
                  run_if:
                  - passed
                  working_directory: "#{SRC_DIRECTORY}"
            artifacts:
              - type: build
                  source: "#{SRC_DIRECTORY}/**"
                  destination: ""
