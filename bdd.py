import psycopg2
con = psycopg2.connect("dbname='CVTeque' user='postgres' host='localhost' password='admin'")

def getCursor():
    cursor = con.cursor()
    return cursor

def getConnection():
    return con