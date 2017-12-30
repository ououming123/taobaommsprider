import pymysql;


jdbcIp="127.0.0.1"
jdbcPort=3306
jdbcUsername="neowong"
jdbcPassword="Ning0310"
Db="taobaomm"


def getDB():
    conn = pymysql.connect(host=jdbcIp, user=jdbcUsername, passwd=jdbcPassword, db=Db,
		charset="utf8", cursorclass=pymysql.cursors.DictCursor)
    return conn









