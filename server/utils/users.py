import json


def __write(data: dict) -> None:
    """
    Write data to the users json file
    :param data: The data that need to be written to the json file
    """
    with open('data/users.json', 'w') as file:
        json.dump(data, file)


def get_users() -> dict:
    """
    Read the users json file
    :return: Dictionary of the users from the users json file
    """
    with open('data/users.json') as file:
        return json.load(file)


def user_exist(users: dict, ip_addr: str):
    """
    Checks if a user exist in the users dictionary
    :param users: The users dictionary
    :param ip_addr: The user IP address
    :return: True - if th user exist | False - if the user doesn't exist
    """
    for user_ip_addr in users:
        if user_ip_addr == ip_addr:
            return True
    return False


def insert(ip_addr: str, key: tuple) -> None:
    """
    Insert a new user to the users json file
    :param ip_addr: The user's IP address
    :param key: The user's public key
    """
    users = get_users()

    if not user_exist(users, ip_addr):
        users[ip_addr] = key
        __write(users)


def remove(ip_addr: str) -> None:
    """
    Remove a user from the users json file
    :param ip_addr: The user's IP address
    """
    users = get_users()
    users.pop(ip_addr)

    __write(users)


def get_key(ip_addr: str) -> tuple:
    """
    Get a user's public key
    :param ip_addr: The user's IP address
    :return: The user's public key
    """
    users = get_users()
    return tuple(users[ip_addr])
