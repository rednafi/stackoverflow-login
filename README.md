# stackoverflow-login

[![codecov](https://img.shields.io/codecov/c/github/rednafi/stackoverflow-login?style=flat-square)](https://codecov.io/gh/rednafi/stackoverflow-login)
[![License](https://img.shields.io/github/license/rednafi/stackoverflow-login?style=flat-square)](https://github.com/rednafi/stackoverflow-login/blob/main/LICENSE)


This is a simple script that logs into StackOverflow and just waits there for 5 seconds.
The GitHub action in this repo is configured to run it every day at 00:00 UTC. I created
it to get the Fanatic badge without putting in the work ¯\\_(ツ)_/¯.

## Run the script locally

* Clone the repo and head out to the root directory.
* Create and activate a Python 3.10 virtual environment:

    ```
    python3.10 -m venv .venv && source .venv/bin/activate
    ```
* Install the dependencies:

    ```
    pip install -r requirements.txt
    ```
* Set up StackOverflow credentials as environment variables:

    ```
    export STACKOVERFLOW_EMAIL=<stackoverflow-email>
    export STACKOVERFLOW_PASSOWRD=<stackoverflow-password>
    ```
* Run the script:

    ```
    python -m src.login
    ```

    If the login is successful, you'll see something similar to this:

    ```
    INFO:root:Login successful!
    INFO:root:Now sleeping for 5 seconds...
    ```

## Run the tests

* In an active virtual environment, install the dev dependencies:

    ```
    pip install -r requirements-dev.txt
    ```
* Run the tests:

    ```
    pytest -v -s --cov --cov-report term-missing
    ```

    You'll see the following output:

    ```
    =================== test session starts ===================
    collected 3 items

    tests/test_login.py::test_login_ok PASSED
    tests/test_login.py::test_login_error PASSED
    tests/test_login.py::test_main_retry PASSED

    ---------- coverage: platform linux, python 3.10.4-final-0 -----------
    Name                  Stmts   Miss  Cover   Missing
    ---------------------------------------------------
    src/__init__.py           0      0   100%
    src/login.py             35      0   100%
    tests/__init__.py         0      0   100%
    tests/test_login.py      33      0   100%
    ---------------------------------------------------
    TOTAL                    68      0   100%


    =================== 3 passed in 0.24s ===================
    ```
