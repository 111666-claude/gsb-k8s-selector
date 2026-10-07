"""解析与求值标签选择器。"""


_INDEX_CACHE = []


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
        return ("notin", key.strip(), _values(rest))
    if " in " in text:
        key, _, rest = text.partition(" in ")
        return ("in", key.strip(), _values(rest))
    if "!=" in text:
        key, _, value = text.partition("!=")
        return ("neq", key.strip(), value.strip())
    if "==" in text:
        key, _, value = text.partition("==")
        return ("eq", key.strip(), value.strip())
    if "=" in text:
        key, _, value = text.partition("=")
        return ("eq", key.strip(), value.strip())
    if text.startswith("!"):
        return ("notexists", text[1:].strip(), [])
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
        return key in labels and labels[key] == values
    if kind == "neq":
        return key in labels and labels[key] != values
    if kind == "in":
        return key in labels and labels[key] in values
    if kind == "notin":
        if not values:
            return True
        return key in labels and labels[key] not in values
    if kind == "exists":
        return key in labels
    if kind == "notexists":
        return key not in labels
    return False


def matches(reqs, labels, counter):
    return all(_match_req(req, labels, counter) for req in reqs)


def _index_for(objects, counter):
    if _INDEX_CACHE and _INDEX_CACHE[0] is objects:
        return _INDEX_CACHE[1]
    index = {}
    for i, labels in enumerate(objects):
        counter.scanned += 1
        for key, value in labels.items():
            index.setdefault(key, {}).setdefault(value, []).append(i)
    _INDEX_CACHE[:] = [objects, index]
    return index


def search(objects, selector, counter):
    reqs = parse(selector, counter)
    driver = next((req for req in reqs if req[0] == "eq"), None)
    if driver is not None:
        _, key, value = driver
        candidates = _index_for(objects, counter).get(key, {}).get(value, [])
        return [i for i in candidates if matches(reqs, objects[i], counter)]
    out = []
    for i, labels in enumerate(objects):
        counter.scanned += 1
        if matches(reqs, labels, counter):
            out.append(i)
    return out
