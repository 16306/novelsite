<<<<<<< HEAD
import pymysql



class SaveNover():

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='343637', db='nover', charset='utf8mb4')

    def addnovers(self, sort, novername, writername, novelindex):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO nover(sort,novername,writername,novelindex) VALUES ('%d', '%s', '%s','%d')" % (sort, novername, writername, novelindex))
        lastrowid = cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid

    def addchaper(self, noverid, chaptername, content):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO chapter(noverid,chaptername,content) VALUES ('%d', '%s', '%s')" % (noverid, chaptername, pymysql.escape_string(content)))
        cur.close()
        self.conn.commit()

    def findchapter(self, novelindex, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid,sort FROM nover WHERE novelindex = '%d'" % novelindex)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE noverid = '%d'" % (results[0][0]))
                results = cur.fetchall()
                if len(results) < text_urls:
                    return text_urls - len(results), lastrowid
                else:
                    return 0
            else:
                return 0
        else:
            return -1

    def findsort(self):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid FROM nover ORDER BY noverid DESC  limit 1")
        results = cur.fetchall()
        if len(results) is not 0:
            return results[0][0]
        else:
            return 0

    def findnovel(self, novelname, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid,sort FROM nover WHERE novername = '%s'" % novelname)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE noverid = '%d'" % (results[0][0]))
                results = cur.fetchall()
                if len(results) < text_urls:
                    return text_urls - len(results), lastrowid
                else:
                    return 0
            else:
                return 0
        else:
            return -1
=======
import pymysql



class SaveNover():

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='343637', db='nover', charset='utf8mb4')

    def addnovers(self, sort, novername, writername, novelindex):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO nover(sort,novername,writername,novelindex) VALUES ('%d', '%s', '%s','%d')" % (sort, novername, writername, novelindex))
        lastrowid = cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid

    def addchaper(self, noverid, chaptername, content):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO chapter(noverid,chaptername,content) VALUES ('%d', '%s', '%s')" % (noverid, chaptername, pymysql.escape_string(content)))
        cur.close()
        self.conn.commit()

    def findchapter(self, novelindex, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid,sort FROM nover WHERE novelindex = '%d'" % novelindex)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE noverid = '%d'" % (results[0][0]))
                results = cur.fetchall()
                if len(results) < text_urls:
                    return text_urls - len(results), lastrowid
                else:
                    return 0
            else:
                return 0
        else:
            return -1

    def findsort(self):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid FROM nover ORDER BY noverid DESC  limit 1")
        results = cur.fetchall()
        if len(results) is not 0:
            return results[0][0]
        else:
            return 0

    def findnovel(self, novelname, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT noverid,sort FROM nover WHERE novername = '%s'" % novelname)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE noverid = '%d'" % (results[0][0]))
                results = cur.fetchall()
                if len(results) < text_urls:
                    return text_urls - len(results), lastrowid
                else:
                    return 0
            else:
                return 0
        else:
            return -1
>>>>>>> f97198a5deb6422ec051ff232620d61d6d09f3ab
