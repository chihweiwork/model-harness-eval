"""X1/X2 雙向驗證：原始 fixture 必須 FAIL，套用正解必須 PASS。"""

from bench.tasks import verify_x1, verify_x2
from tests.conftest import fix_x1, fix_x2


class TestX1Officecli:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("X1-officecli")
        ok, _ = verify_x1(d, "")
        assert not ok, "原始碼應該 FAIL（沒有 .txt 輸出檔）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("X1-officecli")
        fix_x1(d)
        ok, detail = verify_x1(d, fix_x1.stdout)
        assert ok, f"正解應該 PASS: {detail}"


class TestX2Opencli:
    def test_original_must_fail(self, copy_fixture):
        d = copy_fixture("X2-opencli")
        ok, _ = verify_x2(d, "")
        assert not ok, "原始碼應該 FAIL（沒有價格資訊）"

    def test_fix_must_pass(self, copy_fixture):
        d = copy_fixture("X2-opencli")
        fix_x2(d)
        ok, detail = verify_x2(d, fix_x2.stdout)
        assert ok, f"正解應該 PASS: {detail}"
