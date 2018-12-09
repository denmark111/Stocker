#!/usr/bin/python3

import pymysql.cursors

conn = pymysql.connect(
        host='localhost',
        user='root',
        password='12341234',
        db='STOCKER',
        autocommit=True)

cursor=conn.cursor()
sql = '''
            CREATE TABLE seeking (
                url varchar(255) NOT NULL PRIMARY KEY,
                stock varchar(255) NOT NULL,
                positive varchar(255),
                negative varchar(255),
                mixed varchar(255),
                neutral varchar(255),
                keyword varchar(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql2='''
            CREATE TABLE nasdaq (
                url varchar(255) NOT NULL PRIMARY KEY,
                stock varchar(255) NOT NULL,
                positive varchar(255),
                negative varchar(255),
                mixed varchar(255),
                neutral varchar(255),
                keyword varchar(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql3='''
            CREATE TABLE fidelity (
                title varchar(255) NOT NULL PRIMARY KEY,
                stock varchar(255) NOT NULL,
                positive varchar(255),
                negative varchar(255),
                mixed varchar(255),
                neutral varchar(255),
                keyword varchar(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
cursor.execute(sql)
cursor.execute(sql2)
cursor.execute(sql3)
conn.commit()

conn.close()