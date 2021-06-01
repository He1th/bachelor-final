import json
import uuid

import mysql.connector
from .Article import Article
from .JSONParser import JSONParser
from .User import User


class SqlHandler:

    config = {'user': 'root',
              'password': '1234',
              'host': 'host.docker.internal',
              'port': '3306'}

    conn = None
    connected = False

    def __init__(self):
        self.establishConnection()


    def establishConnection(self):
        print("Connecting to database")
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.connected = True
        except:
            print("Connection could not be established")

        if self.connected:
            self.createDatabase()
            self.createTables()
            if not self.isPopulated():
                self.populateDatabase()


    def insertArticle(self, article):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)

            query = '''INSERT INTO articles(id, timestamp, author, headline, excerpt, text, nouns, nounScore)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE
                timestamp = values(timestamp),
                author = values(author),
                headline = values(headline),
                excerpt = values(excerpt),
                text = values(text),
                nouns = values(nouns),
                nounScore = values(nounScore)'''

            datavalues = (article.article_id,
                          article.timestamp,
                          article.author,
                          article.headline,
                          article.excerpt,
                          article.text,
                          json.dumps(article.nouns, ensure_ascii=False),
                          json.dumps(article.nounScore, ensure_ascii=False))

            cur.execute(query, datavalues)
            self.conn.commit()
            cur.close()


    def insertUser(self, user):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)

            query = '''INSERT INTO users(id, readArticles, nounDict, nounScore, recommendedArticles, lengthOfReadArticles)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                readArticles = values(readArticles),
                nounDict = values(nounDict),
                nounScore = values(nounScore),
                recommendedArticles = values(recommendedArticles),
                lengthOfReadArticles = values(lengthOfReadArticles)'''

            datavalues = (user.user_id,
                          json.dumps(user.readArticles, ensure_ascii=False),
                          json.dumps(user.nounDict, ensure_ascii=False),
                          json.dumps(user.nounScore, ensure_ascii=False),
                          json.dumps(user.recommendedArticles, ensure_ascii=False),
                          user.lengthOfReadArticles)

            cur.execute(query, datavalues)
            self.conn.commit()
            cur.close()


    def retrieveArticle(self, article_id):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)

            query = '''SELECT * FROM articles WHERE id = %s'''
            datavalues = (article_id,)

            cur.execute(query, datavalues)
            sqlResponse = cur.fetchall()
            cur.close()

            data = sqlResponse[0]
            return Article(data[0], data[1], data[2], data[3], data[4], data[5], json.loads(data[6]), json.loads(data[7]))


    def retrieveUser(self, user_id):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor()

            query = '''SELECT * FROM users WHERE id = %s'''
            datavalue = (user_id,)

            cur.execute(query, datavalue)
            sqlResponse = cur.fetchall()
            cur.close()

            data = sqlResponse[0]
            return User(data[0], json.loads(data[1]), json.loads(data[2]), json.loads(data[3]), json.loads(data[4]), data[5])

    def retrieveAllUsers(self):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor()
            query = '''SELECT id FROM users'''
            cur.execute(query)
            sqlResponse = cur.fetchall()
            cur.close()

            aList = []

            for x in range(0, len(sqlResponse)):
                data = sqlResponse[x]
                aList.append(data[0])

            return aList


    def retrieveRandomArticles(self, number=5):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)
            query = '''SELECT * FROM articles ORDER BY RAND() LIMIT %s'''
            datavalue = (number,)
            cur.execute(query, datavalue)
            sqlResponse = cur.fetchall()
            cur.close()

            aList = []

            for x in range(0, number):
                data = sqlResponse[x]
                aList.append(Article(data[0], data[1], data[2], data[3], data[4], data[5], json.loads(data[6]), json.loads(data[7])))

            return aList


    def retrieveLatestArticles(self, numberOfArticles=500):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)
            datavalue = (numberOfArticles,)
            query = '''SELECT * FROM articles ORDER BY timestamp DESC LIMIT %s'''

            cur.execute(query, datavalue)
            sqlResponse = cur.fetchall()
            cur.close()

            aList = []

            for x in range(0, len(sqlResponse)):
                data = sqlResponse[x]
                aList.append(Article(data[0], data[1], data[2], data[3], data[4], data[5], json.loads(data[6]), json.loads(data[7])))

            return aList


    def retrieveAllArticles(self):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor()
            query = '''SELECT * FROM articles'''
            cur.execute(query)
            sqlResponse = cur.fetchall()
            cur.close()

            aList = []

            for x in range(0, len(sqlResponse)):
                data = sqlResponse[x]
                aList.append(Article(data[0], data[1], data[2], data[3], data[4], data[5], json.loads(data[6]), json.loads(data[7])))

            return aList



    def searchForArticles(self, searchTerm):
        if not self.connected:
            self.establishConnection()

        if self.connected:

            searchValue = "%" + str(searchTerm) + "%"
            datavalue = (searchValue,)

            cur = self.conn.cursor(prepared=True)

            query = '''SELECT * FROM articles WHERE text LIKE %s'''
            cur.execute(query, datavalue)
            sqlResponse = cur.fetchall()
            cur.close()

            aList = []

            for x in range(0, len(sqlResponse)):
                data = sqlResponse[x]
                aList.append(Article(data[0], data[1], data[2], data[3], data[4], data[5], json.loads(data[6]), json.loads(data[7])))

            return aList

    def insertParameters(self, headlineWeight, excerptWeight, textWeight, nounWeight, nameWeight, locWeight, orgWeight, latestArticles, latestToRecommend):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)

            query = '''INSERT INTO config(id, headlineWeight, excerptWeight, textWeight, nounWeight, nameWeight, locWeight, orgWeight, latestArticles, latestToRecommend)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE
                headlineWeight = values(headlineWeight),
                excerptWeight = values(excerptWeight),
                textWeight = values(textWeight),
                nounWeight = values(nounWeight),
                nameWeight = values(nameWeight),
                locWeight = values(locWeight),
                orgWeight = values(orgWeight),
                latestArticles = values(latestArticles),
                latestToRecommend = values(latestToRecommend)'''

            datavalues = (1, headlineWeight, excerptWeight, textWeight, nounWeight, nameWeight, locWeight, orgWeight, latestArticles, latestToRecommend)
            cur.execute(query, datavalues)
            self.conn.commit()
            cur.close()


    def retrieveParameters(self):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor()

            query = '''SELECT * FROM config WHERE id = 1'''

            cur.execute(query)
            sqlResponse = cur.fetchall()
            cur.close()

            data = sqlResponse[0]
            return data




    def createDatabase(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE DATABASE IF NOT EXISTS RecommenderDB''')
        self.conn.database = "RecommenderDB"
        self.conn.commit()
        cur.close()


    def createTables(self):
        cur = self.conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS articles(id varchar(255) PRIMARY KEY UNIQUE , timestamp varchar(255), author TEXT(65535), headline TEXT(65535), excerpt TEXT(65535), text TEXT(65535), nouns TEXT(65535), nounScore TEXT(65535))''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS users(id varchar(255) PRIMARY KEY UNIQUE , readArticles TEXT(65535), nounDict TEXT(65535), nounScore TEXT(65535), recommendedArticles TEXT(65535), lengthOfReadArticles varchar(255))''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS config(id varchar(255) PRIMARY KEY UNIQUE , headlineWeight varchar(255), excerptWeight varchar(255), textWeight varchar(255), nounWeight varchar(255), nameWeight varchar(255), locWeight varchar(255), orgWeight varchar(255), latestArticles varchar(255), latestToRecommend varchar(255)) ''')

        self.conn.commit()
        cur.close()


    def populateDatabase(self):
        print("Populating Database")
        parser = JSONParser()
        articles = parser.createArticleFromJson(500)

        for a in articles:
            self.insertArticle(a)
        print("Done populating Database")


    def isPopulated(self):
        cur = self.conn.cursor()
        query = '''SELECT COUNT(id) FROM articles'''
        cur.execute(query)
        count = cur.fetchall()
        cur.close()

        if count[0][0] > 0:
            return True
        else:
            return False


    def createArticle(self, article):
        if not self.connected:
            self.establishConnection()

        if self.connected:
            cur = self.conn.cursor(prepared=True)

            query = '''INSERT INTO articles(id, timestamp, author, headline, excerpt, text)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                timestamp = values(timestamp),
                author = values(author),
                headline = values(headline),
                excerpt = values(excerpt),
                text = values(text),'''

            datavalues = (article.article_id,
                          json.dumps(article.timestamp, ensure_ascii=False),
                          json.dumps(article.author, ensure_ascii=False),
                          json.dumps(article.headline, ensure_ascii=False),
                          json.dumps(article.excerpt, ensure_ascii=False),
                          json.dumps(article.text, ensure_ascii=False))

            cur.execute(query, datavalues)
            self.conn.commit()
            cur.close()
