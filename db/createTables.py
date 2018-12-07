#!/usr/bin/python3

import pymysql.cursors

conn = pymysql.connect(
        host='localhost',
        user='root',
        password='12341234',
        db='STOCKER')

cursor=conn.cursor()
sql = '''
            CREATE TABLE seeking (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql2='''
            CREATE TABLE nasdaq (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql3='''
            CREATE TABLE fidelity (
                title varchar(255) NOT NULL PRIMARY KEY,
                date varchar(255) NOT NULL,
                content varchar(255) NOT NULL,
                url varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
cursor.execute(sql)
cursor.execute(sql2)
cursor.execute(sql3)
conn.commit()

conn.close()