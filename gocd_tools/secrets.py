from gocd_tools.io import exists, makedirs
from gocd_tools.defaults import get_secrets_dir_path


def init_secrets():
    response = {}
    secrets_dir_path, msg = get_secrets_dir_path()
    if not secrets_dir_path:
        response["msg"] = msg
        return False, response

    if not exists(secrets_dir_path):
        # Ensure the secrets dir is there
        created, msg = makedirs(secrets_dir_path)
        response["msg"] = msg
        if not created:
            return False, response
        return True, response

    response["msg"] = "The secrets db directory already exists: {}".format(
        secrets_dir_path
    )
    return True, response
