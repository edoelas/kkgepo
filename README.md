> *It is 3am and you start hearing "kkgepo kkeddeff kkgesvanow kkloff ..." You think the old ones have come after you, but no, it is even worse, your flatmate is a sysadmin.*
> 
> kkgepo, the language of evil, used to speak with k8s.

`kkgepo` is just a bunch of dynamically generated kubectl aliases. It does not check anything, it just substitutes words. But there is more, by selling your soul now you can use `ff`, which allows you to choose a specific resource to apply your actions.
`kkgepo` is simple to use and easy to extend, less than 100 python lines. `kkgepo` also includes ksetns and ksetco to set namespace and context respectively using fzf.

Usage with zsh is advised. It works waaay better. Probably support for bash will be dropped in the future due to problems.

**Requirements**:
- fzf
- python
- https://github.com/rcaloras/bash-preexec/blob/master/bash-preexec.sh

## Installation

Clone the repository and source `kubealiasrc` in your shell configuration:

```bash
git clone https://github.com/edoelas/kkgepo.git ~/kkgepo
source ~/kkgepo/kubealiasrc
```

The tool now requires the `KKGEPO_ALIASES` environment variable to point
at the YAML file containing all the alias definitions.  If the variable is
missing, `kkgepo` will print an error message and load no aliases.

## Project layout

```
kkgepo/
├── main.py           # command line interface
├── aliases.yaml      # default alias definitions
├── kubealiasrc       # shell helper functions
├── build.sh          # build script producing kk.pex
├── src/              # library modules (e.g. yaml_fallback)
└── tests/            # unit tests
```

`build.sh` compiles dependencies using `uv`, packages the project into a
stand‑alone `pex` archive (`kk.pex`) and runs it with the default aliases.

### Building

Run the provided script to create the executable archive:

```bash
./build.sh
```

The resulting `kk.pex` can be executed directly or copied somewhere on your
`$PATH`.

**Managing dependencies**:
This project uses [uv](https://github.com/astral-sh/uv) for dependency
management. After installing `uv`, create a virtual environment and install
the development requirements:

```bash
uv venv
uv pip install -e ".[develop]"
```

**Help**:
```
Usage:
        main.py <alias1> <alias2> ...

Resources:
        po => pods
        dp => deployment
        st => statefulset
        sv => service
        in => ingress
        cm => configmap
        se => secret
        no => nodes
        ns => namespaces
        pv => persistentvolume
        pc => persistentvolumeclaim
        ar => all

Commands:
        ge => get
        de => describe
        rm => delete
        af => apply --recursive -f
        ak => apply -k
        ku => kustomize
        ed => edit
        ru => run --rm --restart=Never --image-pull-policy=IfNotPresent -i -t
        lo => logs -f
        ex => exec -i -t

Flags:
        al => --all
        oy => -o=yaml
        ow => -o=wide
        oj => -o=json
        an => --all-namespaces
        sl => --show-labels
        wa => --watch

.˖✦·˳MAGIC˚.✦.˳˖:
        ff => fzf over resources
```
