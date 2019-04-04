import subprocess


def test_suite_should_fail_for_unused_snapshots(snapshot):
    completed_process = subprocess.run(
        ["pytest", "--snapshot-strict", "-v", "examples/pytest/unused_snapshot/command.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )

    assert completed_process.returncode == 1
    assert "test_should_not_use_any_snapshot PASSED" in completed_process.stdout
    assert "ERROR: 1 snapshots unused" in completed_process.stdout
