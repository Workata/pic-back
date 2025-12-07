"""
Script that will create a new user. This app should have only one user which is admin.

export PYTHONPATH=${PYTHONPATH}:${PWD}
python3 ./scripts/create_user.py
"""

from pic_back.utils.auth import create_user

if __name__ == "__main__":
    create_user(username=input(), password=input())
