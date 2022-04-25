Prerequisites
=============

GoCD Authentication
-------------------

Because the gocd-tool uses the `GoCD Web API <https://api.gocd.org/current/>`_ to manage the server, it needs to be able to succesfully authenticate against against a running GoCD web server in order for it to apply any of its operations.
Specifically, the tool relies on using a user generated `Access Token <https://docs.gocd.org/current/configuration/access_tokens.html>`_ as the method of authentication.

Before such a token can be generated, the GoCD server has to have an `Authorization Configuration <https://docs.gocd.org/current/configuration/dev_authentication.html>`_ defined based on one of the built-in methods or one of the `Authentication Plugins <https://www.gocd.org/plugins/#authorization>`_ that GoCD supports.
Which `Authorization Configuration <https://docs.gocd.org/current/configuration/dev_authentication.html>`_ you choose is completely up to you, as long as you ensure to enable such a Configuration.

After this has been done, you should now be able to authenticate via the GoCD website. In this interface, as described by the
GoCD documentation, you should be able to generate a `Access Token <https://docs.gocd.org/current/configuration/access_tokens.html>`_ for your user.

Upon generating and saving the `Access Token <https://docs.gocd.org/current/configuration/access_tokens.html>`_, the `gocd-tools` expects that this value
is assigned to the ``GOCD_AUTH_TOKEN`` environment variable::

    export GOCD_AUTH_TOKEN="ACCESS_TOKEN"

Secondly, the `gocd-tools` also requires that the ``GOCD_BASE_URL`` variable be set to the URL of the GoCD server::

    export GOCD_BASE_URL=https://gocd_server_url

With these two prerequisites in place, the `gocd-tools` is now ready to be used to both be installed and used.
