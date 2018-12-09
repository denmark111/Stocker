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
                articleUrl VARCHAR(600) NOT NULL PRIMARY KEY,
	            stockName VARCHAR(10) NULL DEFAULT NULL,
            	keyWords MEDIUMTEXT NULL,
            	positiveRate FLOAT NULL DEFAULT NULL,
            	negativeRate FLOAT NULL DEFAULT NULL,
            	mixedRate FLOAT NULL DEFAULT NULL,
	            neutralRate FLOAT NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql2='''
            CREATE TABLE nasdaq (
                articleUrl VARCHAR(600) NOT NULL PRIMARY KEY,
	            stockName VARCHAR(10) NULL DEFAULT NULL,
            	keyWords MEDIUMTEXT NULL,
            	positiveRate FLOAT NULL DEFAULT NULL,
            	negativeRate FLOAT NULL DEFAULT NULL,
            	mixedRate FLOAT NULL DEFAULT NULL,
	            neutralRate FLOAT NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
sql3='''
            CREATE TABLE fidelity (
                articleTime varchar(50) NOT NULL PRIMARY KEY,
	            stockName varchar(10) NOT NULL,
	            keyWords mediumtext NULL DEFAULT NULL,
                positiveRate float NULL DEFAULT NULL,
                negativeRate float NULL DEFAULT NULL,
                mixedRate float NULL DEFAULT NULL,
                neutralRate float NULL DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
cursor.execute(sql)
cursor.execute(sql2)
cursor.execute(sql3)
conn.commit()

conn.close()