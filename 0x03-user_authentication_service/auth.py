#!/usr/bin/env python3
'''
'''
from bcrypt import hashpw, gensalt, checkpw
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f'email already exists')
    
    def valid_login(self, email: str, password: str) -> bool:
        '''
        '''
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        
    def create_session(self, email: str) -> str:
        '''
        '''
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()
            setattr(user, 'session_id', uid)
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None
        
    def get_user_from_session_id(self, session_id: str) -> str:
        '''
        '''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
        
    def destroy_session(self, user_id: int) -> None:
        '''
        '''
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, 'session_id', None)
            self._db._session.commit()
        except NoResultFound:
            return None
        

def _hash_password(password: str) -> bytes:
    '''
    '''
    return hashpw(password.encode('utf-8'), gensalt())

def _generate_uuid() -> str:
    '''
    '''
    return str(uuid.uuid4())