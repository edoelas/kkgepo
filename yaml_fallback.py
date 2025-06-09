"""Minimal YAML parser implementing a subset of PyYAML's API."""

def safe_load(stream):
    if hasattr(stream, "read"):
        content = stream.read()
    else:
        content = str(stream)

    result = {}
    current = None
    for line in content.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            current = line.rstrip(":")
            result[current] = {}
        else:
            key, value = line.strip().split(":", 1)
            result[current][key.strip()] = value.strip().strip('"')
    return result
