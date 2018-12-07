#!/usr/bin/env python

import pymysql.cursors

conn = pymysql.connect(host='localhost',
        user='root',
        password='12341234',
        charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'CREATE DATABASE STOCKER'
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()

