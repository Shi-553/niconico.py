"""Example of login with session id."""

from niconico import NicoNico

client = NicoNico()

# login with session id (cookie called `user_session` of nicovideo.jp)
client.login_with_session("user_session_~~~~")
