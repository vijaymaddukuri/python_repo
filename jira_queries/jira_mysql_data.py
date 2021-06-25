import pymysql
import json
import sys

class Mysql(object):
    def __init__(self):
        """ Mysql connector """
        self.conn = pymysql.connect(host='bz3-db3.eng.vmware.com', user='mts', password='mts', database='bugzilla')
        self.cursor = self.conn.cursor()

    def fetch_data(self, qry):
        """ Fetch data """
        try:
            self.cursor.execute(qry)
        except mysql.connector.Error as err:
            print(err)
            sys.exit(1)
        return list(self.cursor)

    def __del__(self):
        """ Clean up """
        self.conn.close()

bugzilla = Mysql()