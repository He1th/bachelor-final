import json
import re
from .Article import Article


class JSONParser:
    cleanr = re.compile('<.*?>')

    def createArticleFromJson(self, numberOfArticles):
        articleList = []
        f = open('./article_dump.json', "r")
        for i in range(0, numberOfArticles):
            line = f.readline()
            data = json.loads(line)

            article_id = data["article_uuid"]
            timestamp = data["published"]
            author = data["byline"] if data["byline"] is not None else ""
            headline = data["headline"] if data["headline"] is not None else ""
            excerpt = data["lead"] if data["lead"] is not None else ""
            text = ""

            textLines = data["content"]["parts"]
            for i in textLines:
                string = self.cleanhtml(i["data"].get("text"))
                if string is not None:
                    text += string + " "

            articleList.append(Article(article_id, timestamp, author, headline, excerpt, text))
        return articleList


    def cleanhtml(self, raw_html):
        if (raw_html == None):
            return
        cleantext = re.sub(self.cleanr, '', raw_html)
        return cleantext
