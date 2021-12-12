def import_from_module(module_path, module_name, func_name):
    module = __import__(module_path, fromlist=[module_name])
    return getattr(module, func_name)


def cli_exec(args):
    # action determines which function to execute
    module_path = args.module_path
    module_name = args.module_name
    func_name = args.func_name
    # if hasattr(args, "provider_groups"):
    #     provider_groups = args.provider_groups
    # else:
    #     provider_groups = []

    # if hasattr(args, "argument_groups"):
    #     argument_groups = args.argument_groups
    # else:
    #     argument_groups = []

    # if hasattr(args, "skip_config_groups"):
    #     skip_config_groups = args.skip_config_groups
    # else:
    #     skip_config_groups = []
    func = import_from_module(module_path, module_name, func_name)
    if not func:
        return False

    # Extract none config kwargs from args
    return func()
