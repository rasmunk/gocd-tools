import os
import datetime
import sys
import subprocess
import inspect
import json
from ast import literal_eval


def get_env_value(name):
    value, msg = is_env_set(name)
    if not value:
        return False, msg
    return value


def is_env_set(name):
    if name not in os.environ:
        return False, "Environment variable: {} is not set".format(name)
    value = os.environ[name]
    if not value:
        return False, "Environment variable: {} is set but blank".format(name)
    return value, ""


def process(execute_kwargs=None):
    """Function for execute a set of command lines"""
    if not execute_kwargs:
        execute_kwargs = {}

    print("Execute Kwargs: {}".format(execute_kwargs))
    commands = execute_kwargs["commands"]
    if not isinstance(commands, list):
        commands = [execute_kwargs["commands"]]

    output_results = []
    for command in commands:
        if isinstance(command, str):
            prepared_command = command.split()
        elif isinstance(command, list):
            prepared_command = command
        else:
            raise TypeError("Incorrect command type handed to process")
        # Subprocess
        run_kwargs = {}
        available_arguments = inspect.getfullargspec(subprocess.run)
        if (
            "capture_output" in available_arguments.kwonlyargs
            and "capture" in execute_kwargs
        ):
            run_kwargs["capture_output"] = execute_kwargs["capture"]
        else:
            if execute_kwargs["capture"]:
                run_kwargs["stdout"] = subprocess.PIPE
                run_kwargs["stderr"] = subprocess.PIPE

        result = subprocess.run(prepared_command, **run_kwargs)
        command_results = {}
        if hasattr(result, "args"):
            command_results.update({"command": " ".join((getattr(result, "args")))})
        if hasattr(result, "returncode"):
            command_results.update({"returncode": str(getattr(result, "returncode"))})
        if hasattr(result, "stderr"):
            command_results.update({"error": str(getattr(result, "stderr"))})
        if hasattr(result, "stdout"):
            command_results.update({"output": str(getattr(result, "stdout"))})
        output_results.append(command_results)
    return output_results


def format_output_json(process_result):
    json_result = {}
    for key, value in process_result.items():
        try:
            evalued = literal_eval(value)
        except SyntaxError:
            json_result[key] = value
            continue
        if isinstance(evalued, bytes):
            evalued = evalued.decode("utf-8")
        if isinstance(evalued, str):
            # Ensure utf-8 encoding
            evalued = evalued.encode("utf-8")
        if isinstance(evalued, int):
            evalued = str(evalued)

        if len(evalued) > 0:
            json_result[key] = json.loads(evalued)
        else:
            json_result[key] = value
    return json_result


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def to_str(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
