import requests
import json
from gocd_tools.defaults import (
    authorization_config_path,
    cluster_profiles_path,
    elastic_agent_profile_path,
    repositories_path,
    roles_path,
    templates_path,
    secret_managers_config_path,
    GOCD_AUTH_TOKEN,
    GITHUB_AUTH_URL,
    GITHUB_GOCD_AUTH_URL,
    GITHUB_AUTHORIZATION_HEADER,
    ACCEPT_HEADER_1,
    ACCEPT_HEADER_2,
    ACCEPT_HEADER_3,
    ACCEPT_HEADER_4,
    ACCEPT_HEADER_7,
    GOCD_BASE_URL,
    AUTH_URL,
    AUTHORIZATION_HEADER,
    SECRET_CONFIG_URL,
    AUTHORIZATION_CONFIG_URL,
    CLUSTER_PROFILES_URL,
    ELASTIC_AGENT_URL,
    ROLE_URL,
    CONFIG_REPO_URL,
    TEMPLATE_URL,
)
from gocd_tools.config import load_config


def head(session, url, *args, **kwargs):
    try:
        return session.head(url, *args, **kwargs)
    except Exception as err:
        print("Failed HEAD request: {}".format(err))
    return None


def get(session, url, *args, **kwargs):
    try:
        return session.get(url, *args, **kwargs)
    except Exception as err:
        print("Failed GET request: {}".format(err))
    return None


def post(session, url, *args, **kwargs):
    try:
        return session.post(url, *args, **kwargs)
    except Exception as err:
        print("Failed POST request: {}".format(err))
    return None


def get_type(session, base_url, id, headers=None):
    id_url = "{}/{}".format(base_url, id)
    resp = get(session, id_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def get_types(session, base_url, headers=None):
    resp = get(session, base_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def create_type(session, url, data=None, headers=None):
    json_data = json.dumps(data)
    created = post(session, url, data=json_data, headers=headers)
    if created.status_code == 200:
        return True
    print("Failed to create type: {}".format(created.text))
    return False


def authenticate_github(session):
    if GOCD_AUTH_TOKEN == "":
        print(
            "The required environment variable GOCD_AUTH_TOKEN was empty: {}".format(
                GOCD_AUTH_TOKEN
            )
        )
        return False

    # Login to regular github
    github_auth = get(session, GITHUB_AUTH_URL, headers=GITHUB_AUTHORIZATION_HEADER)
    if github_auth.status_code != 200:
        print(
            "Failed to authenticate with GitHub: {} - {}".format(
                github_auth.status_code, github_auth.text
            )
        )
        return False

    redirect_location = get(
        session,
        GITHUB_GOCD_AUTH_URL,
        allow_redirects=False,
        headers=GITHUB_AUTHORIZATION_HEADER,
    )
    if not redirect_location.status_code == 302:
        print(
            "Failed to get the GitHub auth location: {} - {}".format(
                redirect_location.status_code, redirect_location.text
            )
        )
        return False

    if "location" not in redirect_location.headers:
        print(
            "Location not available in the GitHUB auth response: {}".format(
                redirect_location.headers
            )
        )
        return False

    # Get the URL location for the GitHub auth page.
    # TODO, the location_url does not properly authorize
    # the session with the existing github authentication.
    # Potentially lookinto a library option like
    # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html
    # location_url = redirect_location.headers["location"]
    # github_resp = get(
    #    session, location_url, allow_redirects=False
    # )
    #    if not github_resp.status_code == 200:
    #        return False
    #    return True
    return False


def authenticate(session, allow_redirects=False, **auth_kwargs):
    resp = get(session, AUTH_URL, headers=AUTHORIZATION_HEADER, **auth_kwargs)
    if resp.status_code == 200:
        return True
    print("Failed to authenticate: {} - {}".format(resp.status_code, resp.text))
    return False


def is_auth_repo(repository_config):
    if "authentication" not in repository_config:
        return False
    if "required" not in repository_config["authentication"]:
        return False
    if not repository_config["authentication"]["required"]:
        return False
    return True


def repo_auth_data(repository_config):
    return repository_config["authentication"]


def get_repo_secret(auth_data):
    if "secret" not in auth_data:
        return False
    return auth_data["secret"]


def get_repo_secret_manager(repository_config):
    return repository_config["authentication"]["secret_plugin"]


def get_secret_configs(session, headers=None):
    if not headers:
        headers = ACCEPT_HEADER_3
    return get(session, SECRET_CONFIG_URL)


def get_secret_manager(session, id):
    return get_type(session, SECRET_CONFIG_URL, id, headers=ACCEPT_HEADER_3)


def init_server():
    """ As the first thing, the server's authorization config
    is defined.
    """
    print("Init server")
    print("Configure the Authorization config on server: {}".format(GOCD_BASE_URL))
    authorization_configs = load_config(path=authorization_config_path)

    response = {}
    with requests.Session() as session:
        for auth_config in authorization_configs:
            exists = get_type(
                session,
                AUTHORIZATION_CONFIG_URL,
                auth_config["id"],
                headers=ACCEPT_HEADER_2,
            )
            if not exists:
                created = create_type(
                    session,
                    AUTHORIZATION_CONFIG_URL,
                    data=auth_config,
                    headers=ACCEPT_HEADER_2,
                )
                if not created:
                    response[
                        "msg"
                    ] = "Failed to create authorization config: {}".format(auth_config)
                    return False, response
    response["msg"] = "The Authorization config for: {} was completed".format(
        GOCD_BASE_URL
    )
    return True, response


def configure_server():
    authorization_configs = load_config(path=authorization_config_path)
    cluster_profiles_configs = load_config(path=cluster_profiles_path)
    elastic_agent_configs = load_config(path=elastic_agent_profile_path)
    repositories_configs = load_config(path=repositories_path)
    roles_configs = load_config(path=roles_path)
    templates_configs = load_config(path=templates_path)
    # TODO, load and create the authorization config
    secret_managers_configs = load_config(path=secret_managers_config_path)

    configs = [
        {"path": authorization_config_path, "config": authorization_configs},
        {"path": cluster_profiles_path, "config": cluster_profiles_configs},
        {"path": elastic_agent_profile_path, "config": elastic_agent_configs},
        {"path": repositories_path, "config": repositories_configs},
        {"path": roles_path, "config": roles_configs},
        {"path": templates_path, "config": templates_configs},
        {"path": secret_managers_config_path, "config": secret_managers_configs},
    ]
    response = {}

    for config in configs:
        if not config["config"]:
            response["msg"] = "Failed loading: {}".format(config["path"])
            return False, response

    with requests.Session() as session:
        print("Authenticate")
        # github_authed = authenticate_github(session)
        # if not github_authed:
        #    response["msg"] = "Failed to authenticate against: {}".format(
        #        GITHUB_AUTH_URL
        #    )
        #    return False, response

        authed = authenticate(session)
        if not authed:
            response["msg"] = "Failed to authenticate against: {}".format(
                GITHUB_GOCD_AUTH_URL
            )
            return False, response

        print("Setup Roles")
        for role_config in roles_configs:
            exists = get_type(
                session,
                ROLE_URL,
                role_config["id"],
                headers=ACCEPT_HEADER_3,
            )
            if not exists:
                created = create_type(
                    session,
                    ROLE_URL,
                    data=role_config,
                    headers=ACCEPT_HEADER_3,
                )
                if not created:
                    response["msg"] = "Failed to create role: {}".format(
                        role_config
                    )
                    return False, response

        print("Setup Secret Manager")
        for secret_manager_config in secret_managers_configs:
            exists = get_type(
                session,
                SECRET_CONFIG_URL,
                secret_manager_config["id"],
                headers=ACCEPT_HEADER_3,
            )
            if not exists:
                created = create_type(
                    session,
                    SECRET_CONFIG_URL,
                    data=secret_manager_config,
                    headers=ACCEPT_HEADER_3,
                )
                if not created:
                    response["msg"] = "Failed to create secret config: {}".format(
                        secret_manager_config
                    )
                    return False, response

        print("Setup Cluster profiles")
        # Create cluster profile
        for cluster_config in cluster_profiles_configs:
            existing_cluster = get_type(
                session,
                CLUSTER_PROFILES_URL,
                cluster_config["id"],
                headers=ACCEPT_HEADER_1,
            )
            if not existing_cluster:
                created = create_type(
                    session,
                    CLUSTER_PROFILES_URL,
                    data=cluster_config,
                    headers=ACCEPT_HEADER_1,
                )
                if not created:
                    response["msg"] = "Failed to create cluster profile: {}".format(
                        cluster_config
                    )
                    return False, response

        for agent_config in elastic_agent_configs:
            existing_agent = get_type(
                session, ELASTIC_AGENT_URL, agent_config["id"], headers=ACCEPT_HEADER_2
            )
            if not existing_agent:
                created = create_type(
                    session,
                    ELASTIC_AGENT_URL,
                    data=agent_config,
                    headers=ACCEPT_HEADER_2,
                )
                if not created:
                    response[
                        "msg"
                    ] = "Failed to create elastic agent profile: {}".format(created)
                    return False, response

        print("Create Template Configs")
        for template_config in templates_configs:
            existing_template = get_type(
                session, TEMPLATE_URL, template_config["name"], headers=ACCEPT_HEADER_7
            )
            if not existing_template:
                created = create_type(
                    session, TEMPLATE_URL, data=template_config, headers=ACCEPT_HEADER_7
                )
                if not created:
                    response["msg"] = "Failed to create template config: {}".format(
                        created
                    )
                    return False, response

        print("Create Config Repositories")
        for repository_config in repositories_configs:
            existing_repo = get_type(
                session,
                CONFIG_REPO_URL,
                repository_config["id"],
                headers=ACCEPT_HEADER_4,
            )
            if not existing_repo:
                # Check whether a secret auth token is required
                extra_config_kwargs = {}
                if is_auth_repo(repository_config):
                    auth_data = repo_auth_data(repository_config)
                    repo_secret_manager = get_repo_secret_manager(repository_config)
                    secret = get_repo_secret(auth_data)

                    secret_manager = get_secret_manager(session, repo_secret_manager)
                    if not secret_manager:
                        print(
                            "Repo: {} tries to use secret manager: {} which doesn't exist".format(
                                repository_config["id"], repo_secret_manager
                            )
                        )
                    # secret = get_type(session, SECRET_CONFIG_URL)
                    # if not secret:
                    # created = create_secret(repository_config)
                    #    created = create_secret(repository_config)
                    #    if not created:
                    #        print("Failed to create new secret")
                    #    extra_config_kwargs["secret"] = created
                created = create_type(
                    session,
                    CONFIG_REPO_URL,
                    data={"id": repository_config["id"], **repository_config["config"]},
                    headers=ACCEPT_HEADER_4,
                )
                if not created:
                    response["msg"] = "Failed to create repository config: {}".format(
                        created
                    )
                    return False, response


def cleanup_server():
    pass


if __name__ == "__main__":
    init_server()
    configure_server()
    cleanup_server()
