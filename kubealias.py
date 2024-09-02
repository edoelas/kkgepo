import sys

subs = {
    'af': 'apply --recursive -f',
    'ak': 'apply -k',
    'ku': 'kustomize',
    'ex': 'exec -i -t',
    'lo': 'logs -f',
    'pr': 'proxy',
    'pf': 'port-forward',
    'ge': 'get',
    'de': 'describe',
    'rm': 'delete',
    'ed': 'edit',
    'ru': 'run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t',
    'ar': 'all', # all resources
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
    'oy' : '-o=yaml',
    'ow' : '-o=wide',
    'oj' : '-o=json',
    'an' : '--all-namespaces', # all namespaces
    'sl' : '--show-labels',
    'wa' : '--watch',
}

resources = [
    'po',
    'dp',
    'st',
    'sv',
    'in',
    'cm',
    'se',
    'no',
    'ns',
    'pv',
    'pc',
]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        help_str = "Usage:\\\\n\\\\tkubealias.py <alias1> <alias2> ... \\\\nAlias:\\\\n" # scape backslashes
        for k, v in subs.items():
            help_str += f"\\\\t{k} => {v}\\\\n"
        print(f"printf \"{help_str}\"")

        sys.exit(1)
    
    alias = sys.argv[1]
    alias = [alias[i:i+2] for i in range(0, len(alias), 2)]

    command: str = 'kubectl'
    for a in alias:
        if a in subs:
            command += f" {subs[a]}"
            
        elif a == 'ff':
            # get resource in alias. Default to pod.
            alias_resource = next((res for res in alias if res in resources), 'po')
            command += f" $(kubectl get {subs[alias_resource]} --no-headers | fzf | awk '{{print $1}}')"

        else:
            print(f"echo \"Alias not found: {a}\"")
            sys.exit(1)

    print(command)
    sys.exit(0)