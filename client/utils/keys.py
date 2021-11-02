import json
import os
from os import path


def create_file():
    file_path = 'data/keys.json'
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)


def __write(data: dict) -> None:
    """
    Write data to the users json file
    :param data: The data that need to be written to the json file
    """
    with open('data/keys.json', 'w') as file:
        json.dump(data, file)


def read() -> dict:
    """
    Read the users json file
    :return: Dictionary of the users from the users json file
    """
    create_file()

    with open('data/keys.json') as file:
        return json.load(file)


def update(ip_addr: str, public_key: tuple, private_key: tuple) -> None:
    """
    Insert a new user to the users json file
    :param ip_addr: The user's IP address
    :param public_key: The user's public key
    :param private_key: The user's private key
    """
    keys = read()
    if not keys or not (list(keys.keys())[0] == ip_addr):
        keys['ip'] = ip_addr
        keys['public'] = public_key
        keys['private'] = private_key
        __write(keys)


def get_keys() -> tuple:
    """
    Get the user's public and private key
    :return: The user's public and private key -> (public, private)
    """
    keys = read()
    public_key = tuple(keys['public'])
    private_key = tuple(keys['private'])

    return public_key, private_key
