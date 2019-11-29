import os
import tarfile

import pytest

from topo_order_commits import topo_order_commits


@pytest.mark.parametrize("repo_id", ['1'])
def test_topo_order_constraint(repo_id, capsys):
    repo_fixture_dir = get_repo_fixture_dir()
    repo_name = get_repo_name_from_id(repo_id)
    untar_repo_if_needed(repo_fixture_dir, repo_name)

    child_to_parent_edges = get_child_to_parent_edges(os.path.join(repo_fixture_dir, f'{repo_name}-edges.txt'))

    cwd = os.getcwd()
    os.chdir(os.path.join(repo_fixture_dir, repo_name))
    topo_order_commits()

    output_lines = capsys.readouterr().out.strip().split('\n')
    assigned_commit_order = assign_commit_order_and_detect_duplicates(output_lines)

    for edge in child_to_parent_edges:
        child, parent = edge

        if child not in assigned_commit_order:
            raise Exception(f'Missing commit hash {child}')
        if parent not in assigned_commit_order:
            raise Exception(f'Missing commit hash {parent}')

        assert assigned_commit_order[child] < assigned_commit_order[parent], \
            f'{child} has to precede {parent} in a topological order'

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


def get_child_to_parent_edges(filepath):
    with open(filepath, 'r') as file:
        return [line.split() for line in file]


def assign_commit_order_and_detect_duplicates(output_lines):
    assigned_order = {}
    for line in output_lines:
        if line and '=' not in line:
            commit_hash = line.split()[0]
            if commit_hash in assigned_order:
                raise Exception(f'Duplicate commits detected. Commit hash: {commit_hash}')
            assigned_order[commit_hash] = len(assigned_order)
    return assigned_order
