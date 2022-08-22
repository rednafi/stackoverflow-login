"""Login to stack overflow.com peridically and do nothing."""


import logging
import os
from http import HTTPStatus

import httpx

logging.basicConfig(level=logging.INFO)


def login(url: str, email: str, password: str) -> None:
    """Login to stack overflow.com. Before running the script,
    make sure you've set up your credentials in the environment variables.

    export STACKOVERFLOW_EMAIL=<your email>
    export STACKOVERFLOW_PASSWORD=<your password>
    """

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

    logging.warning("Login successful!")


if __name__ == "__main__":
    url = "https://stackoverflow.com/users/login"
    email = os.environ["STACKOVERFLOW_EMAIL"]
    password = os.environ["STACKOVERFLOW_PASSWORD"]

    try:
        login(url, email, password)
    except AssertionError:
        logging.error("Login failed!")
        raise
