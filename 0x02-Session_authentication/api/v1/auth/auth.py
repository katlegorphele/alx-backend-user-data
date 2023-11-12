#!/usr/bin/env python3
""" Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication base class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require path

        Args:
            path (str): path
            excluded_paths (List[str]): excluded path

        Returns:
            bool: TRue or false
        """
        if path is None:
            return True
        if excluded_paths == [] or excluded_paths is None:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Get Authorization header

        Args:
            request (None, optional): Description

        Returns:
            str: Description
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user

        Args:
            request (None, optional): Description

        Returns:
            TypeVar('User'): Description
        """
        return None
