import datetime
import sqlite3
from typing import List, Any

conn = sqlite3.connect('database.db')
cur = conn.cursor()


def is_exist(login: str) -> bool:
    a = cur.execute(f"""SELECT * FROM master WHERE login = '{login}';""").fetchone() is not None
    b = cur.execute(f"""SELECT * FROM slave WHERE login = '{login}';""").fetchone() is not None
    return a or b


def get_user_id_by_login(login: str) -> int:
    a = cur.execute(f"""SELECT id FROM master WHERE login = '{login}';""").fetchone()
    if a:
        return a[0]
    b = cur.execute(f"""SELECT id FROM slave WHERE login = '{login}';""").fetchone()
    return b[0]


def get_role(login: str) -> str:
    if cur.execute(f"""SELECT id FROM master WHERE login = '{login}';""").fetchone():
        return 'master'
    else:
        return "slave"


def get_fullname(login: str) -> str:
    a = cur.execute(f"""SELECT name FROM master WHERE login = '{login}';""").fetchone()
    if a:
        return a[0]
    else:
        b = cur.execute(f"""SELECT name FROM slave WHERE login = '{login}';""").fetchone()
        return b[0]


def create_group(name: str, token: str, master_id: int) -> int:
    cur.execute(f'''
    INSERT INTO "group" (name, masterid, token)
    VALUES ('{name}', {master_id}, '{token}');''')
    conn.commit()
    return cur.execute(f"""SELECT id FROM "group" WHERE token = '{token}';""").fetchone()[0]


def get_masters_groups(master_id: int) -> list[Any]:
    return cur.execute(f'''
    SELECT * FROM "group" WHERE masterid = {master_id}''').fetchall()


def set_salve_to_group(group_id: int, slave_id: int) -> None:
    cur.execute(f"""UPDATE slave SET groupid = '{group_id}' WHERE id = '{slave_id}';""")
    conn.commit()


def create_task(text: str, date_start: datetime.date, date_end: datetime.date, time_start: datetime.time,
                time_end: datetime.time) -> int:
    cur.execute(f'''
    INSERT INTO task (task_text, date_start, time_start, date_end, time_end, masterid)
    VALUES ('{text}', '{str(date_start)}', '{str(time_start)}', '{str(date_end)}', '{str(time_end)}', 2);''')
    conn.commit()


def create_subtask(tsak_id: int, slave_id: int) -> int:
    """
    Creates subtask for main task

    :param tsak_id:
    :param slvae_id:
    :return:
    """


def get_group_id_by_name(name: str):
    res = cur.execute(f'''
    SELECT * FROM "group" WHERE name = '{name}';''').fetchone()
    if res:
        return res
    else:
        return None


def get_group_by_token(token: str):
    res = cur.execute(f'''
    SELECT * FROM "group" WHERE token = '{token}';''').fetchone()
    if res:
        print(res)
        return res
    else:
        return None


def get_slave(slave_id: int):
    res = cur.execute(f'''
    SELECT * FROM slave WHERE id = {slave_id}''').fetchone()
    return res


def get_group_slaves(group_id: int):
    res = cur.execute(f'''
    SELECT * FROM slave WHERE groupid = {group_id}''').fetchall()
    return res


def delete_group(group_id: int) -> None:
    cur.execute(f"DELETE FROM \"group\" WHERE id = {group_id};")
    conn.commit()
    return None


def report_for_success(slave_id: int) -> None:
    cur.execute(f"""UPDATE subtask SET done = true WHERE slave_id = '{slave_id}';""")
    conn.commit()
