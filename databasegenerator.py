import sqlite3


def create_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE master
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    login   VARCHAR UNIQUE,
    name    VARCHAR
);""")

    cur.execute("""
    CREATE TABLE "group"
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name     VARCHAR UNIQUE,
    masterid INTEGER,
    token    VARCHAR,
    FOREIGN KEY (masterid) REFERENCES master (id) ON DELETE SET NULL
);""")

    cur.execute("""
    CREATE TABLE subtask
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    slaveid INTEGER,
    taskid  INTEGER,
    done    BOOLEAN,
    FOREIGN KEY (slaveid) REFERENCES slave (id) ON DELETE SET NULL,
    FOREIGN KEY (taskid) REFERENCES task (id) ON DELETE SET NULL
);""")

    cur.execute("""
    CREATE TABLE slave
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    login    VARCHAR UNIQUE,
    name     VARCHAR,
    groupid INTEGER,
    FOREIGN KEY (groupid) REFERENCES master (id) ON DELETE SET NULL
);""")

    cur.execute("""
    CREATE TABLE task
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    task_text VARCHAR,
    date_start DATE,
    time_start TIME,
    date_end DATE,
    time_end TIME,
    masterid  INTEGER,
    groupid   INTEGER,
    FOREIGN KEY (masterid) REFERENCES master (id) ON DELETE SET NULL
    FOREIGN KEY (groupid) REFERENCES "group" (id) ON DELETE SET NULL
);""")
    cur.close()


if __name__ == "__main__":
    create_db()
