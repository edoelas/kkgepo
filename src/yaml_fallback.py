"""Minimal YAML parser implementing a subset of PyYAML's API."""

def _strip_quotes(value: str) -> str:
    """Remove surrounding single or double quotes from a string."""
    if (
        (value.startswith("'") and value.endswith("'"))
        or (value.startswith('"') and value.endswith('"'))
    ):
        return value[1:-1]
    return value


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
            key = _strip_quotes(key.strip())
            value = _strip_quotes(value.strip())
            result[current][key] = value
    return result
