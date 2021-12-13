import os
import yaml
from gocd_tools.io import exists, load


def load_config(path=None):
    if not os.path.exists(path):
        return False
    return load(path, handler=yaml, Loader=yaml.FullLoader)


def get_secrets_path(path, env_postfix=None):
    env_var = None
    if env_postfix and isinstance(env_postfix, str):
        env_var = "CORC_{}".format(env_postfix)
    if env_var in os.environ:
        path = os.environ[env_var]
    return path


def config_exists(path):
    if not path:
        return False
    return exists(path)
