# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot
from snapshottest.file import FileSnapshot


snapshots = Snapshot()

snapshots['not used'] = {}
snapshots['test_should_not_use_any_snapshot 1'] = True
