#!/usr/bin/env python3
"""
Main file
"""
from user import User
from db import DB

# print(User.__tablename__)

# for column in User.__table__.columns:
#     print("{}: {}".format(column, column.type))

# my_db = DB()

# user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
# print(user_1.id)

# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id)

from auth import _hash_password

print(_hash_password("Hello Holberton"))
