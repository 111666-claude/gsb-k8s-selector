"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def one(selector, labels):
    return core.matches(core.parse(selector, core.Counter()), labels, core.Counter())


def run(name):
    if name == "neq":
        _line({"match": one("tier!=web", {"tier": "db"})})
        return 0
    if name == "notin":
        _line({"match": one("tier notin (web,db)", {"tier": "db"})})
        return 0
    if name == "emptyin":
        _line({"match": one("tier in ()", {"tier": "db"})})
        return 0
    if name == "notexists":
        _line({"match": one("!tier", {})})
        return 0
    if name == "work":
        objects = [{"tier": "t%04d" % i} for i in range(800)]
        counter = core.Counter()
        for i in range(800):
            core.search(objects, "tier=t%04d" % i, counter)
        _line({"objects": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
