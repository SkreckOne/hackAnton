import datetime
import sqlite3

conn = sqlite3.connect("database.db")

def is_exist(login: str) -> bool:
    """
    Check for existing user (doesn't matter master or slave)

    :param login:
    :return True or false:
    """

    return True


def get_user_id_by_login(login: str) -> int:
    """
    Gets user by login from db

    :param login:
    :return:
    """

    return 1


def get_role(id: int) -> str:
    """
    Returns user role

    :param id:
    :return 'master' or 'slave':
    """

    return 'master'


def get_fullname(id: int) -> str:
    """
    Returns fullname

    :param id:
    :return:
    """

    return 'Василий Владмирович Панин'


def create_group(name: str, token: str, master_id: int) -> int:
    """
    Creates group

    :param name:
    :return group's id:
    """


def set_salve_to_group(group_id: int, slave_id: int) -> None:
    """
    Sets slave to group

    :param group_id:
    :param slave_id:
    :return None:
    """


def create_task(name: str, date_start: datetime.date, date_end: datetime.date, time_start: datetime.time, time_end: datetime.time) -> int:
    """
    Create task

    :param name:
    :param date_start:
    :param date_end:
    :param time_start:
    :param time_end:
    :return task's id:
    """


def delete_group(group_id: int) -> None:
    conn.execute(f"DELETE FROM Group WHERE id = {group_id};")
    return None


def report_for_success(slave_id: int) -> None:
    """
    Sets flag tells system that slave completed him job

    :param slave_id:
    :return:
    """
    
delete_group(1)