"""A module to interact with the NicoNico API."""

from __future__ import annotations

from logging import Logger, getLogger
from urllib.parse import urlparse

import requests

from niconico.channel import ChannelClient
from niconico.exceptions import LoginFailureError, NicoAPIError
from niconico.user import UserClient
from niconico.video import VideoClient

logger = getLogger("niconico.py")


class NicoNico:
    """A class to interact with the NicoNico API."""

    logger: Logger
    session: requests.Session
    logined: bool
    premium: bool

    video: VideoClient
    user: UserClient
    channel: ChannelClient

    def __init__(self) -> None:
        """Initialize the class."""
        self.logger = logger
        self.session = requests.Session()
        self.logined = False
        self.video = VideoClient(self)
        self.user = UserClient(self)
        self.channel = ChannelClient(self)

    def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a GET request to a URL.

        Args:
            url (str): The URL to send the request to.
            headers (dict[str, str]): Extra headers to send with the request.
                Merged over the default headers.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        return self.session.get(url, headers=req_headers)

    def post(
        self,
        url: str,
        *,
        data: any | None = None,  # type: ignore[valid-type]
        json: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a POST request to a URL.

        Args:
            url (str): The URL to send the request to.
            data (any): The data to send with the request.
            json (object): The data to send with the request.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        if json is None:
            return self.session.post(url, headers=req_headers, data=data)
        return self.session.post(url, headers=req_headers, json=json)

    def delete(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send a DELETE request to a URL.

        Args:
            url (str): The URL to send the request to.
            headers (dict[str, str]): The headers to send with the request.

        Returns:
            requests.Response: The response object.
        """
        parsed_url = urlparse(url)
        req_headers = {
            "User-Agent": "niconico.py",
            "X-Frontend-Id": "6",
            "X-Frontend-Version": "0",
            "X-Niconico-Language": "ja-jp",
            "X-Client-Os-Type": "others",
            "X-Request-With": "https://www.nicovideo.jp",
            "Referer": "https://www.nicovideo.jp/",
            "Host": parsed_url.netloc,
        }
        if headers is not None:
            req_headers.update(headers)
        return self.session.delete(url, headers=req_headers)

    def login_with_session(self, session: str) -> None:
        """Login to NicoNico with a session.

        Args:
            session (str): The session to login with.
        """
        self.logined = False

        self.session.cookies.set("user_session", session)

        res = self.session.get("https://www.nicovideo.jp/")

        if res.url != "https://www.nicovideo.jp/":
            self.session.cookies.clear("", "/", "user_session")
            raise LoginFailureError(message="Login failed")

        if res.headers.get("x-niconico-authflag") == "1":
            self.premium = False
        elif res.headers.get("x-niconico-authflag") == "3":
            self.premium = True
        else:
            self.session.cookies.clear("", "/", "user_session")
            raise LoginFailureError(message="Login failed")

        self.logined = True

    def get_user_session(self) -> str | None:
        """Get the user session.

        Returns:
            str: The user session.
        """
        return self.session.cookies.get("user_session")

    def logout(self, *, revoke: bool = False) -> None:
        """Logout from NicoNico.

        By default this only clears the local session state (the `user_session` cookie and the login flags);
        the session itself stays valid on the server and can be used again with `login_with_session`.

        Args:
            revoke (bool): Also revoke the session on the server, as the web client's logout button does.
                The session becomes unusable everywhere; NicoNico takes up to about two minutes to reject it.
                Defaults to False.

        Raises:
            NicoAPIError: If revoking the session failed.
        """
        if not self.logined:
            self.logger.warning("Not logged in, cannot logout")
            return
        if revoke:
            res = self.delete(
                "https://api.id.nicovideo.jp/v1/sessions/me",
                headers={"Origin": "https://www.nicovideo.jp"},
            )
            # 401 means the server no longer knows the session, which is the state we want
            if res.status_code not in (requests.codes.ok, requests.codes.unauthorized):
                raise NicoAPIError(message=f"Failed to revoke the session: {res.status_code}")
        for cookie in [c for c in self.session.cookies if c.name == "user_session"]:
            self.session.cookies.clear(cookie.domain, cookie.path, cookie.name)
        self.logined = False
        self.premium = False
        self.logger.debug("Logged out from NicoNico")
