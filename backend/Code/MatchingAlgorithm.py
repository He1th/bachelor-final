from scipy import spatial


class MatchingAlgorithm:
    userVector = []
    articleVector = []

    def calculateRelevanceScore(self, article, user):
        self.createVectors(article, user)
        if not self.isArticleVectorEmpty():
            cosim = 1 - spatial.distance.cosine(self.userVector, self.articleVector)
        else:
            cosim = 0

        self.userVector = []
        self.articleVector = []
        user.addRecommendedArticle(article, cosim)
        return

    def createVectors(self, article, user):
        for word in user.nounScore:
            self.userVector.append(user.nounScore.get(word))
            if word in article.nounScore:
                if article.nounScore.get(word) is not None:
                    self.articleVector.append(article.nounScore.get(word))
                else:
                    self.articleVector.append(0)
            else:
                self.articleVector.append(0)

    def isArticleVectorEmpty(self):
        for x in self.articleVector:
            if x != 0:
                return False
        return True
