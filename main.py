import os
import sys
from pathlib import Path
import subprocess
from yaml import safe_load

ALIASES = {"commands": {}, "flags": {}, "resources": {}}
_aliases_env = os.environ.get("KKGEPO_ALIASES")
if not _aliases_env:
    print("KKGEPO_ALIASES environment variable is not set", file=sys.stderr)
else:
    aliases_file = Path(_aliases_env).expanduser()
    try:
        with open(aliases_file, "r") as f:
            ALIASES = safe_load(f)
    except FileNotFoundError:
        print(f"Alias file not found: {aliases_file}", file=sys.stderr)

commands = ALIASES.get("commands", {})

flags = ALIASES.get("flags", {})

resources = ALIASES.get("resources", {})


def print_help() -> None:
    """Print the help message describing available aliases."""

    groups = {
        "Resources": resources,
        "Commands": commands,
        "Flags": flags,
        "\u02d6\u2726\xb7\u02f3MAGIC\u02da\xb7\u2726\u02d6": {"ff": "fzf over resources"},
    }

    help_str = (
        "Usage:\n"
        "       main.py [-p] <alias1><alias2>... (do not use spaces between aliases)\n\n"
        "Use -p or --print to display the kubectl command without executing it.\n"
    )
    for group_name, mapping in groups.items():
        help_str += f"\n{group_name}:\n"
        for code, value in mapping.items():
            help_str += f"\t{code} => {value}\n"

    print(help_str)

def create_command(args: list):
    """
    Generates a kubectl shell command from a list of alias arguments.
    Args:
        args (list): List of command-line arguments. The second argument (args[1]) is expected to be a string of alias codes.
    Returns:
        str | None: The constructed kubectl command as a string, or ``None`` if a
        help or error message was printed.
    Behavior:
        - If the number of arguments is not 2, ``print_help`` is called and ``None``
          is returned.
        - Splits the alias string into 2-character chunks.
        - For each chunk:
            - If it matches a known command, flag, or resource, appends the corresponding kubectl syntax.
            - If it is 'ff', inserts a command to select a resource using fzf
              (defaults to 'pod' if no resource alias is found).
            - If the chunk is not recognized, an error message is printed and
              ``None`` is returned.
    """

    if len(args) != 2:
        print_help()
        return None
    
    alias = args[1]
    alias = [alias[i:i+2] for i in range(0, len(alias), 2)]

    subs = {**commands, **flags, **resources}
    command: str = 'kubectl'
    fzftab_cmd = os.environ.get(
        "FZFTAB_CMD",
        "fzf --height=13 --border --reverse --pointer '>' --header-lines=1 --color 'header:reverse'",
    )
    for a in alias:
        if a in subs:  # adds command, flag, or resource to shell command
            command += f" {subs[a]}"

        elif a == 'ff':  # fzf over resources. Default to pod.
            alias_resource = next((res for res in alias if res in resources), 'po')
            command += (
                f" $(kubectl get {subs[alias_resource]} | {fzftab_cmd} | awk '{{print $1}}')"
            )

        else:  # alias not found
            print(f"Alias not found: '{a}'. Call the script without arguments for help.")
            return None

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
    if cmd is None:
        return

    if print_only:
        print(cmd)
    else:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

if __name__ == '__main__':
    main()
