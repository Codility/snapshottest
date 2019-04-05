import pytest


def test_should_not_use_any_snapshot(snapshot):
    snapshot.assert_match(True)
