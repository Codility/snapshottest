import os
from termcolor import colored

from .module import SnapshotModule


def reporting_lines(testing_cli, strict=False):
    successful_snapshots = SnapshotModule.stats_successful_snapshots()
    bold = ['bold']
    if successful_snapshots:
        yield (
            colored('{} snapshots passed', attrs=bold) + '.'
        ).format(successful_snapshots)
    new_snapshots = SnapshotModule.stats_new_snapshots()
    if new_snapshots[0]:
        yield (
            colored('{} snapshots written', 'green', attrs=bold) + ' in {} test suites.'
        ).format(*new_snapshots)
    inspect_str = colored(
        'Inspect your code or run with `{} --snapshot-update` to update them.'.format(testing_cli),
        attrs=['dark']
    )
    failed_snapshots = SnapshotModule.stats_failed_snapshots()
    if failed_snapshots[0]:
        yield (
            colored('{} snapshots failed', 'red', attrs=bold) + ' in {} test suites. '
            + inspect_str
        ).format(*failed_snapshots)
    unvisited_snapshots = SnapshotModule.all_unvisited_snapshots()
    if unvisited_snapshots:
        if strict:
            error_msg = colored(f'ERROR: {len(unvisited_snapshots)} snapshots unused.', 'red', attrs=bold)
            comment = colored("In strict mode all snapshots must be used.",attrs=['dark'])
            yield f"{error_msg} {comment}"
            yield colored("Unused snapshots:", "red", attrs=bold)
            yield from unvisited_snapshots

        else:
            yield (
                colored('{} snapshots deprecated', 'yellow', attrs=bold) + ' in {} test suites. '
                + inspect_str
            ).format(*unvisited_snapshots)


def diff_report(left, right):
    return [
        'stored snapshot should match the received value',
        '',
        colored('> ') +
        colored('Received value', 'red', attrs=['bold']) +
        colored(' does not match ', attrs=['bold']) +
        colored('stored snapshot `{}`'.format(
            left.snapshottest.test_name,
        ), 'green', attrs=['bold']) +
        colored('.', attrs=['bold']),
        colored('') + '> ' + os.path.relpath(left.snapshottest.module.filepath, os.getcwd()),
        '',
    ] + left.get_diff(right)
