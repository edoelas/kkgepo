Requieres:
- fzf
- python
- https://github.com/rcaloras/bash-preexec/blob/master/bash-preexec.sh

to use: `source ~/kubealias/kubealiasrc`

```
k8s alias:
    af: apply --recursive -f,
    ak: apply -k,
    ku: kustomize,
    ex: exec -i -t,
    lo: logs -f,
    pr: proxy,
    pf: port-forward,
    ge: get,
    de: describe,
    ed: edit,
    ru: run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t,
    ar: all, # all resources
    po: pods,
    dp: deployment,
    st: statefulset,
    sv: service,
    in: ingress,
    cm: configmap,
    se: secret,
    no: nodes,
    ns: namespaces,
    pv: persistentvolume,
    pc: persistentvolumeclaim,
    oy: -o=yaml,
    ow: -o=wide,
    oj: -o=json,
    an: --all-namespaces, # all namespaces
    sl: --show-labels,
    wa: --watch,

Other alias:
    ksetco: set context
    ksetns: set namespace

Deactivated alias:
    rm: delete,
```