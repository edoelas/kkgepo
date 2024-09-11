> *It is 3am and you start hearing "kkgepo kkeddeff kkgesvanow kkloff ..." You think the old ones have come after you, but no, it is even worse, your flatmate is a sysadmin.*
> 
> kkgepo, the language of the devil, used to speak with k8s.

kkgepo is just a bunch of dinamically generated kubectl aliases. It does not check anything, it just substitutes words. But there is more, by selling your soul now you can use `ff`, which allows you to choose a specific resource to apply your actions. 
kkgepo is simple to use and to extend, less than 100 python lines including documentation. 

**Requirements**:
- fzf
- python
- https://github.com/rcaloras/bash-preexec/blob/master/bash-preexec.sh

**Installation**: `source ~/kkgepo/kubealiasrc`

**Help**:
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
