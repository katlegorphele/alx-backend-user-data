#!/usr/bin/env python3
"""
Main module
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Function that registers a user
    """
    url = "http://localhost:5000/users"
    payload = {"email": email, "password": password}
    r = requests.post(url, data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    print("OK")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/sessions"
    payload = {"email": email, "password": password}
    r = requests.post(url, data=payload)
    assert r.status_code == 401
    print("OK")


def profile_unlogged() -> None:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/profile"
    r = requests.get(url)
    assert r.status_code == 403
    print("OK")


def log_in(email: str, password: str) -> str:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/sessions"
    payload = {"email": email, "password": password}
    r = requests.post(url, data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    print("OK")
    return r.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    assert "email" in r.json()
    print("OK")


def log_out(session_id: str) -> None:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    assert r.json() == {}
    print("OK")


def reset_password_token(email: str) -> str:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/reset_password"
    payload = {"email": email}
    r = requests.post(url, data=payload)
    assert r.status_code == 200
    assert len(r.text) == 72
    print("OK")
    return r.text


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Function that checks if the password is valid
    """
    url = "http://localhost:5000/reset_password"
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    r = requests.put(url, data=payload)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}
    print("OK")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
