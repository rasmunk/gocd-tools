from gocd_tools.cli.defaults import SECRETS, SERVER
from gocd_tools.cli.run import cli_exec
from gocd_tools.cli.secrets import add_secrets_groups
from gocd_tools.cli.server import add_server_groups


def setup_cli(parser):
    setup_commands = parser.add_subparsers(title="COMMAND")

    # Secrets
    secrets_parser = setup_commands.add_parser(SECRETS)
    add_secrets_groups(secrets_parser)
    secrets_commands = secrets_parser.add_subparsers(title="COMMAND")
    secrets_generate_parser = secrets_commands.add_parser("init")

    secrets_generate_parser.set_defaults(
        func=cli_exec,
        module_path="gocd_tools.cli.setup",
        module_name="setup",
        func_name="init_secrets",
    )

    # Server
    server_parsers = setup_commands.add_parser(SERVER)
    add_server_groups(server_parsers)
    server_commands = server_parsers.add_subparsers(title="COMMAND")
    setup_generate_parser = server_commands.add_parser("init")

    setup_generate_parser.set_defaults(
        func=cli_exec,
        module_path="gocd_tools.cli.setup",
        module_name="setup",
        func_name="init_server",
    )
