import sys
from pathlib import Path

try:
    from yaml import safe_load
except Exception:  # PyYAML not available
    from yaml_fallback import safe_load

ALIASES_FILE = Path(__file__).with_name("aliases.yaml")

try:
    with open(ALIASES_FILE, "r") as f:
        _ALIASES = safe_load(f)
except FileNotFoundError:
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

    help_str = "Usage:\\n\\tkubealias.py <alias1><alias2>... (do not use spaces between aliases)\\n"
    for k, v in groups.items():
        help_str += f"\\n{k}:\\n"
        for k, v in v.items():
            help_str += f"\\t{k} => {v}\\n"

    return f"printf \"{help_str}\\n\""

def create_command(args: list):
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

if __name__ == '__main__':
    print(create_command(sys.argv))