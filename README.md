Requieres:
- fzf
- python
- https://github.com/rcaloras/bash-preexec/blob/master/bash-preexec.sh

to use: `source ~/kubealias/kubealiasrc`

```
Usage:
        kubealias.py <alias1> <alias2> ... 
Alias:
        po => pods*
        dp => deployment*
        st => statefulset*
        sv => service*
        in => ingress*
        cm => configmap*
        se => secret*
        no => nodes*
        ns => namespaces*
        pv => persistentvolume*
        pc => persistentvolumeclaim*
        af => apply --recursive -f
        ak => apply -k
        ku => kustomize
        ex => exec -i -t
        lo => logs -f
        pr => proxy
        pf => port-forward
        ge => get
        de => describe
        rm => delete
        ed => edit
        ru => run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t
        ar => all
        oy => -o=yaml
        ow => -o=wide
        oj => -o=json
        an => --all-namespaces
        sl => --show-labels
        wa => --watch
        ff => .˖✦·˳MAGIC˚.✦.˳˖ (fzf)
```