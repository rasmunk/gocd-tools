import os
from gocd_tools.utils import is_env_set

PACKAGE_NAME = "gocd-tools"

# API Request Defaults
CONTENT_TYPE = "application/json"
JSON_HEADER = {"Content-Type": CONTENT_TYPE}

API_VERSION_1 = "application/vnd.go.cd.v1+json"
API_VERSION_2 = "application/vnd.go.cd.v2+json"
API_VERSION_3 = "application/vnd.go.cd.v3+json"
API_VERSION_4 = "application/vnd.go.cd.v4+json"

ACCEPT_HEADER_1 = {"Accept": API_VERSION_1, **JSON_HEADER}
ACCEPT_HEADER_2 = {"Accept": API_VERSION_2, **JSON_HEADER}
ACCEPT_HEADER_3 = {"Accept": API_VERSION_3, **JSON_HEADER}
ACCEPT_HEADER_4 = {"Accept": API_VERSION_4, **JSON_HEADER}

GO_DATA_DIR = "/godata"
GO_SECRET_DIR = "/gosecrets"
GO_SECRET_DB_FILE = "{}/secrets.yml".format(GO_SECRET_DIR)
GO_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".{}".format(PACKAGE_NAME))
GO_PLUGIN_DIR = os.path.join(GO_DATA_DIR, "plugins")

# Other constants
GOCD_SECRET_PLUGIN = "gocd-file-based-secrets-plugin.jar"

BUNDLED_PLUGIN = "bundled"
EXTERNAL_PLUGIN = "external"

# Environment variables
ENV_GO_DATA_DIR = "GO_DATA_DIR"
ENV_GO_SECRET_DIR = "GO_SECRET_DIR"
ENV_GO_SECRET_DB_FILE = "GO_SECRET_DB_FILE"
ENV_GO_CONFIG_DIR = "GO_CONFIG_DIR"
ENV_GO_PLUGIN_DIR = "GO_PLUGIN_DIR"

# Default configuration input paths
default_base_path = GO_CONFIG_DIR
default_config_path = os.path.join(default_base_path, "config")

cluster_profiles_path = os.path.join(default_config_path, "cluster_profiles.yml")
elastic_agent_profile_path = os.path.join(
    default_config_path, "elastic_agent_profiles.yml"
)
repositories_path = os.path.join(default_config_path, "repositories.yml")
authorization_config_path = os.path.join(default_config_path, "authorization.yml")
secret_managers_config_path = os.path.join(default_config_path, "secret_managers.yml")


# Datadir discover
def get_data_dir():
    data_path, msg = is_env_set(ENV_GO_DATA_DIR)
    if not data_path:
        if GO_DATA_DIR:
            return GO_DATA_DIR, ""
        return False, msg
    return data_path, ""


# Secrets discover
def get_secrets_dir_path():
    env_dir_path, msg = is_env_set(ENV_GO_SECRET_DIR)
    if not env_dir_path:
        # Use the default as a backup
        if GO_SECRET_DIR:
            return GO_SECRET_DIR, ""
        return False, msg
    return env_dir_path, ""


def get_secrets_file_name():
    secrets_name, msg = is_env_set(ENV_GO_SECRET_DB_FILE)
    if not secrets_name:
        # Use the default as a backup
        if GO_SECRET_DB_FILE:
            return GO_SECRET_DB_FILE, ""
        return False, msg
    return secrets_name, ""


def get_secrets_db_path():
    dir_path, msg = get_secrets_dir_path()
    if not dir_path:
        return False, msg
    file_name, msg = get_secrets_file_name()
    if not file_name:
        return False, msg
    return os.path.join(dir_path, file_name)
