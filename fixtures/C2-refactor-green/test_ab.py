import pytest

from a import register_user
from b import format_badge


def test_register_normalizes():
    users = []
    assert register_user(users, "  ada   lovelace ") == "Ada Lovelace"
    assert users == ["Ada Lovelace"]


def test_register_rejects_duplicate():
    users = ["Ada Lovelace"]
    with pytest.raises(ValueError):
        register_user(users, "ADA LOVELACE")


def test_badge_normalizes():
    assert format_badge("  grace   HOPPER ") == "[Grace Hopper]"
