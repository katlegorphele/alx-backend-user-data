#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    # Implement add user method, takes in email and hashed_password
    # and returns a User object

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        # new_user.email = email
        # new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    # Implement find user method, takes in email and returns the
    # first row found in the users table as filtered by email. If
    # no row is found, returns None

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by a given attribute

        Args:
            kwargs ([type]): Attribute to search for

        Raises:
            InvalidRequestError: If kwargs is empty or if any of the
            attributes don't match the User object
            NoResultFound: If no results are found in the database

        Returns:
            User: User object found in the database
        """

        # if not kwargs:
        #     raise InvalidRequestError

        # if not all(
        #     hasattr(User, k) for k in kwargs.keys()
        # ):
        #     raise InvalidRequestError

        # user = self._session.query(User).filter_by(**kwargs).first()

        # if user is None:
        #     raise NoResultFound

        # return user
        for k in kwargs.keys():
            if k not in User.__dict__.keys():
                raise InvalidRequestError
        query = self._session.query(User).filter_by(**kwargs)
        # get the first row of user
        user = query.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user attributes

        Args:
            user_id (int): User id

        Raises:
            ValueError: If any of the attributes don't match the User object
            NoResultFound: If no results are found in the database

        Returns:
            None
        """

        for k in kwargs.keys():
            if k not in User.__dict__.keys():
                raise ValueError

        user = self.find_user_by(id=user_id)

        for k, v in kwargs.items():
            setattr(user, k, v)
        self._session.commit()
