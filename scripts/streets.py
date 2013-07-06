import MySQLdb as mdb
import _mysql as mysql
import re

class streets:

    __settings = {}
    __con = False

    def __init__(self):
        configfile = "sqlcreds.txt"
        f = open(configfile)
        for line in f:
            # skip comment lines
            m = re.search('^\s*#', line)
            if m:
                continue

            # parse key=value lines
            m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
            if m is None:
                continue

            self.__settings[m.group(1)] = m.group(2)
        f.close()

        # create connection
        self.__con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'], passwd=self.__settings['password'], db=self.__settings['database'])

    def __sanitize(self,valuein):
        if type(valuein) == 'str':
            valueout = mysql.escape_string(valuein)
        else:
            valueout = valuein
        return valuein

    def add(self,rawname,name,streettype,communityid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("INSERT INTO streets(rawname,name,streettype,communityid) VALUES(%s,%s,%s,%s)",(self.__sanitize(rawname),self.__sanitize(name),self.__sanitize(streettype),self.__sanitize(communityid)))
            cur.close()
            newid = cur.lastrowid
        return newid

    def get(self,streetid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM streets WHERE streetid = %s",(streetid))
            row = cur.fetchone()
            cur.close()
        return row

    def getall(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM streets")
            rows = cur.fetchall()
            cur.close()

        _streets = []
        for row in rows:
            _streets.append(row)

        return _streets

    def delete(self,streetid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("DELETE FROM streets WHERE streetid = %s",(streetid))
            cur.close()

    def update(self,streetid,rawname,name,streettype,communityid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("UPDATE streets SET rawname = %s,name = %s,streettype = %s,communityid = %s WHERE streetid = %s",(self.__sanitize(rawname),self.__sanitize(name),self.__sanitize(streettype),self.__sanitize(communityid),self.__sanitize(streetid)))
            cur.close()

##### Application Specific Functions #####
