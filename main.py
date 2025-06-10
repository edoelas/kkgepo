"""Command line interface for the ``kkgepo`` alias generator."""

from __future__ import annotations

import os
import sys
from pathlib import Path
import subprocess
from yaml import safe_load

DEFAULT_ALIASES = {"commands": {}, "flags": {}, "resources": {}}


def _load_aliases_from_env() -> dict[str, dict[str, str]]:
    """Return alias definitions from the ``KKGEPO_ALIASES`` file."""

    path = os.environ.get("KKGEPO_ALIASES")
    if not path:
        print("KKGEPO_ALIASES environment variable is not set", file=sys.stderr)
        return DEFAULT_ALIASES

    path = Path(path).expanduser()
    try:
        with path.open("r") as f:
            return safe_load(f)
    except FileNotFoundError:
        print(f"Alias file not found: {path}", file=sys.stderr)
        return DEFAULT_ALIASES


ALIASES = _load_aliases_from_env()
commands = ALIASES.get("commands", {})
flags = ALIASES.get("flags", {})
resources = ALIASES.get("resources", {})


def print_help() -> None:
    """Display the supported aliases grouped by type."""

    groups = {
        "Resources": resources,
        "Commands": commands,
        "Flags": flags,
        "\u02d6\u2726\xb7\u02f3MAGIC\u02da\xb7\u2726\u02d6": {"ff": "fzf over resources"},
    }

    print(
        "Usage:\n"
        "       main.py [-p] <alias1><alias2>... (do not use spaces between aliases)\n\n"
        "Use -p or --print to display the kubectl command without executing it.\n"
    )
    for name, mapping in groups.items():
        print(f"\n{name}:")
        for code, value in mapping.items():
            print(f"\t{code} => {value}")

def _split_aliases(code: str) -> list[str]:
    return [code[i : i + 2] for i in range(0, len(code), 2)]


def create_command(args: list[str]) -> str | None:
    """Return the kubectl command represented by ``args`` or ``None``."""

    if len(args) != 2:
        print_help()
        return None

    tokens = _split_aliases(args[1])
    subs = {**commands, **flags, **resources}
    fzf_cmd = os.environ.get(
        "FZFTAB_CMD",
        "fzf --height=13 --border --reverse --pointer '>' --header-lines=1 --color 'header:reverse'",
    )

    parts = ["kubectl"]
    for token in tokens:
        if token == "ff":
            res = next((t for t in tokens if t in resources), "po")
            parts.append(
                f"$(kubectl get {subs[res]} | {fzf_cmd} | awk '{{print $1}}')"
            )
        elif token in subs:
            parts.append(subs[token])
        else:
            print(
                f"Alias not found: '{token}'. Call the script without arguments for help."
            )
            return None

    return " ".join(parts)


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
