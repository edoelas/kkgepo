import sys

commands = {
    'ge': 'get',
    'de': 'describe',
    'rm': 'delete',
    'af': 'apply --recursive -f',
    'ak': 'apply -k',
    'ku': 'kustomize',
    'ed': 'edit',
    'ru': 'run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t',
    'lo': 'logs -f',
    'ex': 'exec -i -t',
}

flags = {
    'al': '--all',
    'oy': '-o=yaml',
    'ow': '-o=wide',
    'oj': '-o=json',
    'an': '--all-namespaces',
    'sl': '--show-labels',
    'wa': '--watch',
}

resources = {
    'po': 'pods',
    'dp': 'deployment',
    'st': 'statefulset',
    'sv': 'service',
    'in': 'ingress',
    'cm': 'configmap',
    'se': 'secret',
    'no': 'nodes',
    'ns': 'namespaces',
    'pv': 'persistentvolume',
    'pc': 'persistentvolumeclaim',
    'ar': 'all', # all resources
}

groups = {
    'Resources': resources,
    'Commands': commands,
    'Flags': flags,
    '.˖✦·˳MAGIC˚.✦.˳˖': {'ff': 'fzf over resources'},
}

def print_help():
    help_str = "Usage:\\n\\tkubealias.py <alias1> <alias2> ...\\n"

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
            command += f" $(kubectl get {subs[alias_resource]} --no-headers | fzf | awk '{{print $1}}')"

        else: # alias not found
            return f"echo \"Alias not found: {a}\""

    return command

if __name__ == '__main__':
    print(create_command(sys.argv))