from __future__ import unicode_literals

import pytest

from snapshottest import Snapshot
from snapshottest.module import SnapshotModule, SnapshotTest


class TestSnapshotModuleLoading(object):
    def test_load_not_yet_saved(self, tmpdir):
        filepath = tmpdir.join("snap_new.py")
        assert not filepath.check()  # file does not exist
        module = SnapshotModule("tests.snapshots.snap_new", str(filepath))
        snapshots = module.load_snapshots()
        assert isinstance(snapshots, Snapshot)

    def test_load_missing_package(self, tmpdir):
        filepath = tmpdir.join("snap_import.py")
        filepath.write_text("import missing_package\n", "utf-8")
        module = SnapshotModule("tests.snapshots.snap_import", str(filepath))
        with pytest.raises(ImportError):
            module.load_snapshots()

    def test_load_corrupted_snapshot(self, tmpdir):
        filepath = tmpdir.join("snap_error.py")
        filepath.write_text("<syntax error>\n", "utf-8")
        module = SnapshotModule("tests.snapshots.snap_error", str(filepath))
        with pytest.raises(SyntaxError):
            module.load_snapshots()



class MockSnapshotTest(SnapshotTest):
    def __init__(self, *, strict=False, module: SnapshotModule, test_name: str) -> None:
        super().__init__(strict=strict)
        self._module = module
        self._test_name = test_name

    @property
    def module(self) -> SnapshotModule:
        return self._module

    @property
    def test_name(self) -> str:
        return self._test_name


class TestStrictSnapshotModule:
    def test_should_fail_if_new_snapshots_appear(self, tmpdir):
        file_with_snapshots = tmpdir.join("snap_new.py")
        module = SnapshotModule(module="tests.snapshots.snap_new", filepath=str(file_with_snapshots))
        test = MockSnapshotTest(strict=True, module=module, test_name="Some test")

        with pytest.raises(AssertionError, match="Saving snapshots not allowed in strict mode."):
            test.assert_match(False)
