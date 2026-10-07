"""解析与求值标签选择器。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def _values(text):
    inner = text.strip()
    if inner.startswith("("):
        inner = inner[1:]
    if inner.endswith(")"):
        inner = inner[:-1]
    return [part.strip() for part in inner.split(",") if part.strip()]


def _parse_req(text, counter):
    counter.scanned += 1
    text = text.strip()
    if " notin " in text:
        key, _, rest = text.partition(" notin ")
        return ("in", key.strip(), _values(rest))
    if " in " in text:
        key, _, rest = text.partition(" in ")
        values = _values(rest)
        if not values:
            return ("exists", key.strip(), [])
        return ("in", key.strip(), values)
    if "!=" in text:
        key, _, value = text.partition("!=")
        return ("eq", key.strip(), value.strip())
    if "==" in text:
        key, _, value = text.partition("==")
        return ("eq", key.strip(), value.strip())
    if "=" in text:
        key, _, value = text.partition("=")
        return ("eq", key.strip(), value.strip())
    return ("exists", text, [])


def _split(selector):
    out = []
    depth = 0
    current = ""
    for ch in selector:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(current)
            current = ""
        else:
            current += ch
    out.append(current)
    return [part.strip() for part in out if part.strip()]


def parse(selector, counter):
    if not selector.strip():
        return []
    return [_parse_req(part, counter) for part in _split(selector)]


def _match_req(req, labels, counter):
    counter.scanned += 1
    kind, key, values = req
    if kind == "eq":
        return labels.get(key) == values
    if kind == "in":
        return labels.get(key) in values
    if kind == "exists":
        return key in labels
    return False


def matches(reqs, labels, counter):
    return all(_match_req(req, labels, counter) for req in reqs)


def search(objects, selector, counter):
    reqs = parse(selector, counter)
    out = []
    for i, labels in enumerate(objects):
        counter.scanned += 1
        if matches(reqs, labels, counter):
            out.append(i)
    return out
