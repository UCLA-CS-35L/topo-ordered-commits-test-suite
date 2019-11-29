# topo-ordered-commits-test-suite

This test suite provides some test cases to help you get on the right track.

However, passing all the test cases here does not guarantee a completely correct implementation.

The real test cases might have similar structures but will not have the same hashes.

Please do the following in order to run the test cases.

```
git clone https://github.com/Rustinante/topo-ordered-commits-test-suite.git
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

You can exit the virtual environment by typing `deactivate`.
