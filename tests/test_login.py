from unittest.mock import patch

import pytest
from httpx import Response

from src import login


@patch("src.login.time.sleep")
@patch("src.login.httpx.Client", autospec=True)
def test_login_ok(mock_client, mock_sleep):
    mock_client.return_value.post.return_value = Response(200, content="Top Questions")

    url = "https://stackoverflow.com/users/login"
    email = "test@testmail.com"
    password = "testpassword"
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
    login.login(url, email, password)

    mock_client.assert_called_once_with(headers=headers, follow_redirects=True)
    mock_sleep.assert_called_once_with(5)


@patch("src.login.time.sleep")
@patch("src.login.httpx.Client", autospec=True)
def test_login_error(mock_client, mock_sleep):
    mock_client.return_value.post.return_value = Response(
        200,
        content="Human verification",
    )

    url = "https://stackoverflow.com/users/login"
    email = "test@testmail.com"
    password = "testpassword"
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
    with pytest.raises(AssertionError):
        login.login(url, email, password)

    mock_client.assert_called_once_with(headers=headers, follow_redirects=True)
    mock_sleep.assert_not_called()
