"""Login to stack overflow.com peridically and do nothing.

Before running the script, make sure you've set up your credentials in
the environment variables.

export STACKOVERFLOW_EMAIL=<your email>
export STACKOVERFLOW_PASSWORD=<your password>
"""


import logging
import os
import time
from http import HTTPStatus

import httpx

logging.basicConfig(level=logging.INFO)


def login(url: str, email: str, password: str) -> None:
    """Login to stack overflow.com."""

    headers = {
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        ),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/76.0.3809.100 Safari/537.36"
        ),
        "Origin": "https://stackoverflow.com",
    }
    data = {
        "email": email,
        "password": password,
        "remember": "true",
    }

    # Make a post request with redirect turned on.
    client = httpx.Client(headers=headers, follow_redirects=True)
    response = client.post(url, data=data, headers=headers)

    assert client.cookies.get("prov") is not None
    assert response.status_code == HTTPStatus.OK
    assert "Human verification" not in response.text
    assert "Top Questions" in response.text

    logging.info("Login successful!")
    logging.info("Now sleeping for 5 seconds...")

    time.sleep(5)


def main(retry_after: int = 10 * 60, retry_count: int = 5) -> None:
    """Login to stack overflow.com periodically and do nothing."""

    url = "https://stackoverflow.com/users/login"
    email = os.environ["STACKOVERFLOW_EMAIL"]
    password = os.environ["STACKOVERFLOW_PASSWORD"]
    error_count = 0

    while True:
        try:
            return login(url, email, password)
        except AssertionError:
            logging.error("Login failed!")
            error_count += 1
            logging.info("Retrying in 10 minutes...")
            time.sleep(retry_after)

            if error_count == retry_count:
                logging.error("Too many login failures!")
                raise


if __name__ == "__main__":
    main() # pragma: nocover


