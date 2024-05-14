# topo-ordered-commits-test-suite

This test suite provides some test cases to help you get on the right track.

However, passing all the test cases here does not guarantee a completely correct implementation.

The real test cases might have similar structures but will not have the same hashes.

Please do the following in order to run the test cases.

```
git clone https://github.com/UCLA-CS-35L/topo-ordered-commits-test-suite.git
cd topo-ordered-commits-test-suite
python3 -m venv venv
source venv/bin/activate
pip3 install -U -r requirements.txt
```

The command `source venv/bin/activate` sets up a virtual environment for Python, 
which you should do every time you open up a shell to run this test suite.

Then, repalce the body of the function `def topo_order_commits():` with your implementation, 
i.e., `topo_order_commits` should be the top level function to kick-start the entire program.
This is so that we can expose the function signature `topo_order_commits` to the test suite.

In order to run the tests, simply type 

```
pytest
```

To check for PEP8 coding style violations:
```
flake8 topo_order_commits.py
```

You can use the autoformatter, `autopep8`, resolve some common formatting issues.

```
# This command will resolve many common formatting issues.
autopep8 --in-place topo_order_commits.py
# Be careful with this command, as it will aggressively overwrite your file.
autopep8 --in-place --aggressive --aggressive topo_order_commits.py
```

You can exit the virtual environment by typing `deactivate`.


## Individual Test Cases
After running `pytest` once, which will unzip the `*.tar.gz` files in `tests/repo_fixture`, you can manually examine each of the test repositories inside the `tests/repo_fixture` directory as a way to debug your implementation. The `example-repo-1` will be the first test repository, etc. After `cd` into the test repository, you can run your `topo_order_commits.py` script to see the output of your implementation on that repository.

In the pytest output, if `test_topo_order_constraint[1]` shows up as a failure, the `[1]` means the test case is based on `example-repo-1`, etc.
