from gocd_tools.config import load_config
from gocd_tools.io import exists
from gocd_tools.utils import process
from gocd_tools.secrets import init_secrets


def init_server():
    secret_db_path, msg = get_env_value(GO_SECRET_DB_FILE)
    if not exists(secret_db_path):
        print(msg)
        exit(1)

    secret_db = load_config(secret_db_path)
    if not secret_db:
        print("Failed loading: {}".format(secret_db_path))
        exit(1)

    # Initialize the secret DBs
    base_plugin_cmd = ["java", "-jar", file_secret_plugin_path]
    print("Base plugin cmd: {}".format(base_plugin_cmd))
    create_db_cmd = base_plugin_cmd + ["init", "-f"]
    print("Create_db_cmd: {}".format(create_db_cmd))

    # Add the secret key and values to the secret dbs
    base_add_secret_cmd = base_plugin_cmd + ["add", "-f"]
    for secret_db_key, secret_db in secret_db.items():
        # Create the secret db if it doesn't exist
        if not exists(secret_db["path"]):
            new_db_cmd = create_db_cmd + [secret_db["path"]]
            execute_kwargs = {"commands": [new_db_cmd], "capture": True}
            result = process(execute_kwargs=execute_kwargs)
            print("Result: {}".format(result))

        # Assign the 'data' key in the secret_db to the secret file
        db_add_cmd = base_add_secret_cmd + [secret_db["path"]]
        for key, value in secret_db["data"].items():
            add_secret_cmd = db_add_cmd + ["-n", key, "-v", value]
            execute_kwargs = {"commands": [add_secret_cmd], "capture": True}
            result = process(execute_kwargs=execute_kwargs)
            print("Result: {}".format(result))

    # TODO, have an optional flag for deleting the secret input db after setup


def cleanup_server():
    pass


if __name__ == "__main__":
    init_server()
    cleanup_server()
