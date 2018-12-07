#!/usr/bin/python3

import pymysql.cursors

conn = pymysql.connect(
        host='localhost',
        user='root',
        password='12341234',
        db='STOCKER')

try:
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE seeking (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8

            CREATE TABLE nasdaq (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8

            CREATE TABLE fidelity (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()
