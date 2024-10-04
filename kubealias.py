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
    'an': '--all-namespaces',
    'sl': '--show-labels',
    'wa': '--watch',
    'oy': '-o=yaml',
    'ow': '-o=wide',
    'oj': '-o=json',
}

resources = {
    'no': 'nodes',
    'ns': 'namespaces',
    'dp': 'deployment',
    'st': 'statefulset',
    'po': 'pods',
    'sv': 'service',
    'in': 'ingress',
    'se': 'secret',
    'cm': 'configmap',
    'sa': 'serviceaccount',
    'rd': 'customresourcedefinition',
    'vr': 'vulnerabilityreport',
    'ro': 'role',
    'rb': 'rolebinding',
    'cr': 'clusterrole',
    'cb': 'clusterrolebinding',
    'pv': 'persistentvolume',
    'pc': 'persistentvolumeclaim',
    'ar': 'all', # all resources
}

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
            command += f" $(kubectl get {subs[alias_resource]} --no-headers | fzf | awk '{{print $1}}')"

        else: # alias not found
            return f"echo \"Alias not found: '{a}'. Call the script without arguments for help.\""

    return command

if __name__ == '__main__':
    print(create_command(sys.argv))