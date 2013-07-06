import MySQLdb as mdb
import _mysql as mysql
import re

class communities:

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

    def add(self,name,hrid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("INSERT INTO communities(name,hrid) VALUES(%s,%s)",(self.__sanitize(name),self.__sanitize(hrid)))
            cur.close()
            newid = cur.lastrowid
        return newid

    def get(self,communityid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM communities WHERE communityid = %s",(communityid))
            row = cur.fetchone()
            cur.close()
        return row

    def getall(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM communities")
            rows = cur.fetchall()
            cur.close()

        _communities = []
        for row in rows:
            _communities.append(row)

        return _communities

    def delete(self,communityid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("DELETE FROM communities WHERE communityid = %s",(communityid))
            cur.close()

    def update(self,communityid,name,hrid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("UPDATE communities SET name = %s,hrid = %s WHERE communityid = %s",(self.__sanitize(name),self.__sanitize(hrid),self.__sanitize(communityid)))
            cur.close()

##### Application Specific Functions #####
