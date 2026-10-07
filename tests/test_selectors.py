import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labelsel import core


def one(selector, labels):
    return core.matches(core.parse(selector, core.Counter()), labels, core.Counter())


class SelectorsTest(unittest.TestCase):
    def test_equality(self):
        self.assertTrue(one("tier=web", {"tier": "web"}))

    def test_in_set(self):
        self.assertTrue(one("tier in (web,db)", {"tier": "db"}))

    def test_exists(self):
        self.assertTrue(one("tier", {"tier": "x"}))

    def test_missing_label(self):
        self.assertFalse(one("tier=web", {}))

    def test_empty_selector(self):
        self.assertTrue(one("", {"tier": "x"}))

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse("tier=web", counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
