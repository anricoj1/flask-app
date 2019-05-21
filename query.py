import pymysql
import sq





c = sq.connection.cursor()
def fetchall(query):
    c.execute(query)
    value = c.fetchall()

    return value



def Insert(string):
    c.execute(string)
    sq.connection.commit()

    return string


def Update(string):
    c.execute(string)
    sq.connection.commit()

    return string



def fetchone(query):
    c.execute(query)
    value = c.fetchone()

    return value
