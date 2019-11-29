import os
import tarfile
from collections import defaultdict

import pytest

from topo_order_commits import topo_order_commits


@pytest.mark.parametrize("repo_id", [1, 2, 3, 4])
def test_topo_order_constraint(repo_id, capsys):
    run_topo_order_commits_on_repo(repo_id)
    child_to_parent_edges = get_child_to_parent_edges(repo_id)
    output_lines = capsys.readouterr().out.strip().split('\n')
    assigned_commit_order = assign_commit_order_and_detect_duplicates(output_lines)

    for child, parents in child_to_parent_edges.items():
        if child not in assigned_commit_order:
            raise Exception(f'Missing commit hash {child}')
        for p in parents:
            if p not in assigned_commit_order:
                raise Exception(f'Missing commit hash {p}')

            assert assigned_commit_order[child] < assigned_commit_order[p], \
                f'{child} has to precede {p} in a topological order'


@pytest.mark.parametrize("repo_id", [1, 2, 3, 4])
def test_sticky_starts_and_ends(repo_id, capsys):
    run_topo_order_commits_on_repo(repo_id)
    child_to_parent_edges = get_child_to_parent_edges(repo_id)
    parent_to_children = get_parent_to_child_edges(child_to_parent_edges)
    output_lines = capsys.readouterr().out.strip().split('\n')

    num_lines = len(output_lines)
    for i in range(num_lines):
        line = output_lines[i]

        if not line:
            if i == num_lines - 1:
                raise Exception('The last output line should not be empty')
            sticky_start = output_lines[i + 1]
            if not sticky_start.startswith('='):
                raise Exception(
                    f'The line after an empty line should be a stick start line, i.e. starting with an equal sign, '
                    f'but found {sticky_start}'
                )
            children = set(sticky_start[1:].split())
            if i + 2 >= num_lines:
                raise Exception(f'There has to be a commit after the sticky start {sticky_start}')
            parent = output_lines[i + 2].split()[0]
            if children != parent_to_children[parent]:
                raise Exception(f'The sticky start before commit {parent} should contain {parent_to_children[parent]}, '
                                f'but found {children}')

        elif i + 1 < num_lines and output_lines[i + 1] == '':
            # 1. When there is an empty line, check that the line before is a sticky end
            if not line.endswith('='):
                raise Exception(f'The line before the empty line has to end with =, but found {line}')

            if i == 0:
                raise Exception('A sticky end should not be the first line')
            child = output_lines[i - 1].split()[0]
            parents = get_parents_from_sticky_end(output_lines[i])

            if child not in child_to_parent_edges:
                raise Exception(f'Extraneous child found: {child}')

            # 2. When there is a sticky end as indicated by an empty line
            # check that the sticky end contains the correct parents
            if parents != set(child_to_parent_edges[child]):
                raise Exception(
                    f'The sticky end after commit {child} should contain {child_to_parent_edges[child]}, '
                    f'but found {parents}'
                )

            # if i + 2 >= num_lines or not line[i + 2].startswith('='):
            #     raise Exception(f'Sticky start missing for line {i + 1} (1-based indexing)')

        # 3. Check that if the next line is not a sticky end, then the next commit is a parent of the current commit.
        # But ignore the last line, sticky starts even if the next line is not a sticky end.
        elif i + 1 < num_lines and not line.startswith('=') and (i + 2 >= num_lines or output_lines[i + 2] != ''):
            child = line.split()[0]
            if child not in child_to_parent_edges:
                raise Exception(f'Extraneous child found: {child}')

            parent = output_lines[i + 1].split()[0]
            if parent not in child_to_parent_edges[child]:
                raise Exception(f'The commit {parent} after {child} is not its parent')


def get_parents_from_sticky_end(sticky_end):
    return set(sticky_end.strip()[:-1].split())


def run_topo_order_commits_on_repo(repo_id):
    repo_fixture_dir = get_repo_fixture_dir()
    repo_name = get_repo_name_from_id(repo_id)
    untar_repo_if_needed(repo_fixture_dir, repo_name)

    cwd = os.getcwd()
    os.chdir(os.path.join(repo_fixture_dir, repo_name))
    topo_order_commits()
    os.chdir(cwd)


def get_repo_fixture_dir():
    return os.path.join(os.path.dirname(__file__), 'repo_fixture')


def get_repo_name_from_id(repo_id):
    return f'example-repo-{repo_id}'


def untar_repo_if_needed(repo_fixture_dir, repo_name):
    if not os.path.exists(os.path.join(repo_fixture_dir, repo_name)):
        tar = tarfile.open(os.path.join(repo_fixture_dir, f'{repo_name}.tar.gz'))
        tar.extractall(path=repo_fixture_dir)
        tar.close()


def get_child_to_parent_edges(repo_id):
    repo_fixture_dir = get_repo_fixture_dir()
    repo_name = get_repo_name_from_id(repo_id)
    child_to_parents = defaultdict(set)
    with open(os.path.join(repo_fixture_dir, f'{repo_name}-edges.txt'), 'r') as file:
        for line in file:
            if not line:
                continue
            toks = line.split()
            if len(toks) == 1 and toks[0] not in child_to_parents:
                child_to_parents[toks[0]] = set()
            else:
                child_to_parents[toks[0]].add(toks[1])
    return dict(child_to_parents)


def get_parent_to_child_edges(child_to_parent_edges):
    parent_to_children = defaultdict(set)
    for child, parents in child_to_parent_edges.items():
        for p in parents:
            parent_to_children[p].add(child)

    for h in child_to_parent_edges.keys():
        if h not in parent_to_children:
            parent_to_children[h] = set()

    return dict(parent_to_children)


def assign_commit_order_and_detect_duplicates(output_lines):
    assigned_order = {}
    num_lines = len(output_lines)
    for i in range(num_lines):
        line = output_lines[i]

        # ignore sticky starts and ends
        if line.startswith('='):
            continue

        # ignore sticky ends
        if i + 1 < num_lines and output_lines[i + 1] == '':
            if not line.endswith('='):
                raise Exception(f'The line before the empty line has to end with =, but found {line}')
            continue

        if line:
            commit_hash = line.split()[0]
            if commit_hash in assigned_order:
                raise Exception(f'Duplicate commits detected. Commit hash: {commit_hash}')
            assigned_order[commit_hash] = len(assigned_order)
    return assigned_order
