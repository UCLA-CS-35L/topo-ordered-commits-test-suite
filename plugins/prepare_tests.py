# Reference: https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes
import os
import tarfile

from tests.test_example_repos import get_repo_fixture_dir, get_repo_name_from_id


def pytest_configure(config):
    for repo_id in range(1, 9):
        repo_fixture_dir = get_repo_fixture_dir()
        repo_name = get_repo_name_from_id(repo_id)
        untar_repo_if_needed(repo_fixture_dir, repo_name)


def pytest_unconfigure(config):
    pass


def untar_repo_if_needed(repo_fixture_dir, repo_name):
    if not os.path.exists(os.path.join(repo_fixture_dir, repo_name)):
        tar = tarfile.open(os.path.join(repo_fixture_dir, f"{repo_name}.tar.gz"))
        tar.extractall(path=repo_fixture_dir)
        tar.close()
