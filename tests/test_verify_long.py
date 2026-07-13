"""L1 雙向驗證：原始 fixture 必須 FAIL，套用正解必須 PASS。"""

from bench.tasks import verify_l1
from tests.conftest import fix_l1


class TestL1TodoSpec:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("L1-todo-spec")
        ok, _ = verify_l1(d, "")
        assert not ok, "原始碼應該 FAIL（todo.py 不存在）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("L1-todo-spec")
        fix_l1(d)
        ok, detail = verify_l1(d, "")
        assert ok, f"正解應該 PASS: {detail}"
