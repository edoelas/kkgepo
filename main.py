import os
import sys
from pathlib import Path
import subprocess

try:
    from yaml import safe_load
except Exception:  # PyYAML not available
    from src.yaml_fallback import safe_load

_aliases_env = os.environ.get("KKGEPO_ALIASES")
if not _aliases_env:
    print("KKGEPO_ALIASES environment variable is not set", file=sys.stderr)
    _ALIASES = {"commands": {}, "flags": {}, "resources": {}}
else:
    ALIASES_FILE = Path(_aliases_env).expanduser()
    try:
        with open(ALIASES_FILE, "r") as f:
            _ALIASES = safe_load(f)
    except FileNotFoundError:
        print(f"Alias file not found: {ALIASES_FILE}", file=sys.stderr)
        _ALIASES = {"commands": {}, "flags": {}, "resources": {}}

commands = _ALIASES.get("commands", {})

flags = _ALIASES.get("flags", {})

resources = _ALIASES.get("resources", {})

def print_help():
    groups = {
        'Resources': resources,
        'Commands': commands,
        'Flags': flags,
        '˖✦·˳MAGIC˚✦˖': {'ff': 'fzf over resources'},
    }

    help_str = "Usage:\\n\\tmain.py <alias1><alias2>... (do not use spaces between aliases)\\n"
    for k, v in groups.items():
        help_str += f"\\n{k}:\\n"
        for k, v in v.items():
            help_str += f"\\t{k} => {v}\\n"

    return f"printf \"{help_str}\\n\""

def create_command(args: list):
    """
    Generates a kubectl shell command from a list of alias arguments.
    Args:
        args (list): List of command-line arguments. The second argument (args[1]) is expected to be a string of alias codes.
    Returns:
        str: The constructed kubectl command as a string, or an error/help message if the input is invalid.
    Behavior:
        - If the number of arguments is not 2, calls and returns the result of print_help().
        - Splits the alias string into 2-character chunks.
        - For each chunk:
            - If it matches a known command, flag, or resource, appends the corresponding kubectl syntax.
            - If it is 'ff', inserts a command to select a resource using fzf (defaults to 'pod' if no resource alias is found).
            - If the chunk is not recognized, returns an error message.
    """

    if len(args) != 2:
        return print_help()
    
    alias = args[1]
    alias = [alias[i:i+2] for i in range(0, len(alias), 2)]

    subs = {**commands, **flags, **resources}
    command: str = 'kubectl'
    for a in alias:
        if a in subs: # adds command, flag, or resource to shell command
            command += f" {subs[a]}"
            
        elif a == 'ff': # fzf over resources. Default to pod.
            alias_resource = next((res for res in alias if res in resources), 'po')
            command += f" $(kubectl get {subs[alias_resource]} | fzftab | awk '{{print $1}}')"

        else: # alias not found
            return f"echo \"Alias not found: '{a}'. Call the script without arguments for help.\""

    return command


def main(argv: list[str] | None = None) -> None:
    """Execute or print the command generated from ``argv``.

    The optional ``--print``/``-p`` flag causes the command to be printed
    instead of executed.
    """

    argv = argv or sys.argv
    print_only = False
    if len(argv) > 1 and argv[1] in ("--print", "-p"):
        print_only = True
        argv = [argv[0]] + argv[2:]

    cmd = create_command(argv)
    if print_only:
        print(cmd)
    else:
        subprocess.run(cmd, shell=True, check=False)

if __name__ == '__main__':
    main()
