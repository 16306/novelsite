import pymysql


class SaveNovel():

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='343637', db='novel', charset='utf8mb4')

    def addnovels(self, sort, novelname, writername):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO novel(sort,novelname,writername) VALUES ('%d', '%s', '%s')" % (sort, novelname,writername))
        lastrowid = cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid

    def addchaper(self, novelid, chaptername, content):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO chapter(novelid,chaptername,content) VALUES ('%d', '%s', '%s')" % (novelid,
                                                                                                    chaptername, pymysql.escape_string(content)))
        cur.close()
        self.conn.commit()

    def findchapter(self, novelindex, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT novelid,sort FROM novel WHERE novelindex = '%d'" % novelindex)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE novelid = '%d'" % (results[0][0]))
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
        cur.execute("SELECT novelid FROM novel ORDER BY novelid DESC  limit 1")
        results = cur.fetchall()
        if len(results) is not 0:
            return results[0][0]
        else:
            return 0

    def findnovel(self, novelname, text_urls):
        cur = self.conn.cursor()
        cur.execute("SELECT novelid,sort FROM novel WHERE novelname = '%s'" % novelname)
        results = cur.fetchall()
        if len(results) is not 0:
            lastrowid = results[0][0]
            if len(results) is not 0:
                cur.execute("SELECT * FROM chapter WHERE novelid = '%d'" % (results[0][0]))
                results = cur.fetchall()
                if len(results) < text_urls:
                    return text_urls - len(results), lastrowid
                else:
                    return 0
            else:
                return 0
        else:
            return -1
