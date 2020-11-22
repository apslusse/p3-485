"""Insta485 REST API."""

from insta485.api.likes import get_likes
from insta485.api.api import show_resources

import insta485.api  # noqa: E402  pylint: disable=wrong-import-position
import insta485.views  # noqa: E402  pylint: disable=wrong-import-position
import insta485.model  # noqa: E402  pylint: disable=wrong-import-position
