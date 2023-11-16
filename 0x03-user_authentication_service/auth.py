#!/usr/bin/env python3
"""
"""
from bcrypt import hashpw, gensalt, checkpw
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        function that registers a user and returns the new user object

        Args:
            email (str): a string representing the user email
            password (str): a string representing the user password

        Raises:
            ValueError: a ValueError exception if the email already exists

        Returns:
            User: a User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"email already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Function that checks if the password is valid

        Args:
            email (str): a string representing the user email
            password (str): a string representing the user password

        Returns:
            bool: True if the password is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Function that creates a session ID for a user

        Args:
            email (str): a string representing the user email

        Returns:
            str: the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, "session_id", uid)
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        A function that gets the user from the session ID

        Args:
            session_id (str): a string representing the session ID

        Returns:
            str: the user associated with the session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Function that destroys the session of a user

        Args:
            user_id (int): the user ID

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, "session_id", None)
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Function that generates a reset password token

        Args:
            email (str): the user email

        Returns:
            str: the reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, "reset_token", uid)
            self._db._session.commit()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Function that updates the password

        Args:
            reset_token (str): the reset token
            password (str): the user password

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            setattr(user, "hashed_password", hashed_password)
            setattr(user, "reset_token", None)
            self._db._session.commit()
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """
    Function that hashes the password

    Args:
        password (str): the password to hash

    Returns:
        bytes: the hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """
    Function that generates a UUID

    Returns:
        str: the UUID
    """
    return str(uuid.uuid4())
