"""C1/C2/C3 雙向驗證：原始 fixture 必須 FAIL，套用正解必須 PASS。"""

from bench.tasks import verify_c1, verify_c2, verify_c3
from tests.conftest import fix_c1, fix_c2, fix_c3


class TestC1CrossfileBug:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("C1-crossfile-bug")
        ok, _ = verify_c1(d, "")
        assert not ok, "原始碼應該 FAIL（bug 存在）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("C1-crossfile-bug")
        fix_c1(d)
        ok, detail = verify_c1(d, "")
        assert ok, f"正解應該 PASS: {detail}"


class TestC2RefactorGreen:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("C2-refactor-green")
        ok, _ = verify_c2(d, "")
        assert not ok, "原始碼應該 FAIL（未抽共用邏輯）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("C2-refactor-green")
        fix_c2(d)
        ok, detail = verify_c2(d, "")
        assert ok, f"正解應該 PASS: {detail}"


class TestC3MisleadingTrace:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("C3-misleading-trace")
        ok, _ = verify_c3(d, "")
        assert not ok, "原始碼應該 FAIL（config port 是字串）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("C3-misleading-trace")
        fix_c3(d)
        ok, detail = verify_c3(d, "")
        assert ok, f"正解應該 PASS: {detail}"
