from . import NounRanker


class User:

    def __init__(self, user_id, readArticles = None, nounDict = None, nounScore = None, recommendedArticles=None, lengthOfReadArticles=0):
        self.user_id = user_id

        self.readArticles = readArticles if readArticles is not None else []
        self.nounDict = nounDict if nounDict is not None else {}
        self.nounScore = nounScore if nounScore is not None else {}
        self.recommendedArticles = recommendedArticles if recommendedArticles is not None else {}
        self.lengthOfReadArticles = int(lengthOfReadArticles)


    def addReadArticle(self, article, sqlHandler):
        if article.article_id not in self.readArticles:
            self.readArticles.append(article.article_id)
            self.lengthOfReadArticles += len(article.text)

            for word in article.nouns:
                if word in self.nounDict:
                    self.nounDict[word] = self.nounDict[word] + article.nouns[word]
                else:
                    self.nounDict[word] = article.nouns[word]

            if len(self.readArticles) > 2:
                dataset = []
                for article_id in self.readArticles:
                    dataset.append(sqlHandler.retrieveArticle(article_id))

                rankedScore = NounRanker.rankNouns(self.nounDict, dataset, self.lengthOfReadArticles)
                dict_items = rankedScore.items()
                self.nounScore = dict(list(dict_items)[:100])



    # ------------------------------ HELPER FUNCTIONS -----------------------------------------


    def addRecommendedArticle(self, article, score):
        if article.article_id not in self.readArticles:
            self.recommendedArticles[article.article_id] = score

    def removeRecommendedArticle(self, article):
        self.recommendedArticles.pop(article)

    def sortRecommendedArticles(self):
        sortedArticleScores = {}

        sortedkeys = sorted(self.recommendedArticles.items(), key=lambda x: x[1], reverse=True)
        for e in sortedkeys:
            sortedArticleScores[e[0]] = e[1]

        self.recommendedArticles = sortedArticleScores


    # ------------------------------ DEBUG FUNCTIONS -----------------------------------------
    def printNounScore(self, number):
        print("\nNOUNSCORE OF USER: ")
        x = 0
        for n in self.nounScore:
            if x < number:
                print(str(n) + " :\t" + str(self.nounScore[n]))
                x += 1
        print(" ")
