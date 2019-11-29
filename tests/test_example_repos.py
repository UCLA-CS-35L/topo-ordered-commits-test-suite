import os
import tarfile

import pytest

from topo_order_commits import topo_order_commits


@pytest.mark.parametrize("repo_id", ['1'])
def test_repo(repo_id, capsys):
    repo_fixture_dir = os.path.join('tests', 'repo_fixture')
    repo_name = f'example-repo-{repo_id}'
    if not os.path.exists(os.path.join(repo_fixture_dir, repo_name)):
        tar = tarfile.open(os.path.join(repo_fixture_dir, f'{repo_name}.tar.gz'))
        tar.extractall(path=repo_fixture_dir)
        tar.close()
    cwd = os.getcwd()
    os.chdir(os.path.join(repo_fixture_dir, repo_name))
    topo_order_commits()
    output = capsys.readouterr()
    assert output.out.strip() == 'hi'
    os.chdir(cwd)
