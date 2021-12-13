from gocd_tools.io import exists, makedirs, remove
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


def cleanup_secrets_db():
    response = {}

    db_path, msg = get_secrets_dir_path()
    if not db_path:
        response["msg"] = msg
        return False, response

    if not exists(db_path):
        response["msg"] = "The db path: {} does not exist".format(db_path)
        return True, response

    removed, msg = remove(db_path)
    response["msg"] = msg
    if not removed:
        return False, response
    return True, response


if __name__ == "__main__":
    init_secrets()
    # cleanup_secrets_db()
