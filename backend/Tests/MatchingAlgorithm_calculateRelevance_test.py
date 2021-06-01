import unittest
from backend.Code.Article import Article
from backend.Code.User import User
from backend.Code.MatchingAlgorithm import MatchingAlgorithm

matcher = MatchingAlgorithm()


class calculateRelevance_ideal(unittest.TestCase):
    def setUp(self):
        nounScoreUser1 = {"fodbold": 0.26, "tilskuer": 0.01, "københavn": 0.38, "fck": 0.64, "politik": 0.55,
                          "folketinget": 0.22}
        self.user1 = User("1", nounScore=nounScoreUser1)

        nounScoreUser2 = {"coronavirus": 0.63, "kina": 0.17, "sygdom": 0.03, "hospital": 0.44}
        self.user2 = User("2", nounScore=nounScoreUser2)

        # Articles in the system
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "",
                                nounScore={"fodbold": 0.34, "fck": 0.62, "tilskuer": 0.17, "københavn": 0.51})
        self.article2 = Article("2", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.78, "hospital": 0.33, "vaccine": 0.46})
        self.article3 = Article("3", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.24, "fodbold": 0.19, "europamesterskab": 0.42})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.user1, self.user2)
        del (self.article1, self.article2, self.article3)

    def runTest(self):
        for a in self.articleList:
            matcher.calculateRelevanceScore(a, self.user1)
            matcher.calculateRelevanceScore(a, self.user2)

        expectedOrderOfRelevanceUser1 = ["1", "3", "2"]
        expectedOrderOfRelevanceUser2 = ["2", "3", "1"]

        resultOrderOfRelevanceUser1 = list(self.user1.recommendedArticles.keys())
        resultOrderOfRelevanceUser2 = list(self.user2.recommendedArticles.keys())

        self.assertEqual(expectedOrderOfRelevanceUser1, resultOrderOfRelevanceUser1)
        self.assertEqual(expectedOrderOfRelevanceUser2, resultOrderOfRelevanceUser2)


class calculateRelevance_perfectMatch(unittest.TestCase):
    def setUp(self):
        nounScoreUser1 = {"fodbold": 0.34, "fck": 0.62, "tilskuer": 0.17, "københavn": 0.51}
        self.user1 = User("1", nounScore=nounScoreUser1)

        # Articles in the system
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "",
                                nounScore={"fodbold": 0.34, "fck": 0.62, "tilskuer": 0.17, "københavn": 0.51})
        self.article2 = Article("2", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.78, "hospital": 0.33, "vaccine": 0.46})
        self.article3 = Article("3", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.24, "fodbold": 0.19, "europamesterskab": 0.42})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.user1)
        del (self.article1, self.article2, self.article3)

    def runTest(self):
        for a in self.articleList:
            matcher.calculateRelevanceScore(a, self.user1)

        expectedOrderOfRelevanceUser1 = ["1", "3", "2"]
        resultOrderOfRelevanceUser1 = list(self.user1.recommendedArticles.keys())

        # Check if the recommended order is as expected
        self.assertEqual(expectedOrderOfRelevanceUser1, resultOrderOfRelevanceUser1)

        # Check if a perfectly matching article results in a score of 1
        self.assertEqual(list(self.user1.recommendedArticles.values())[0], 1)


class calculateRelevance_noMatch(unittest.TestCase):
    def setUp(self):

        nounScoreUser1 = {"mode": 0.34, "kjoler": 0.62, "sko": 0.17, "gucci": 0.51}
        self.user1 = User("1", nounScore=nounScoreUser1)

        # Articles in the system
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "",
                                nounScore={"fodbold": 0.34, "fck": 0.62, "tilskuer": 0.17, "københavn": 0.51})
        self.article2 = Article("2", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.78, "hospital": 0.33, "vaccine": 0.46})
        self.article3 = Article("3", "testTime", "testAuthor", "", "", "",
                                nounScore={"coronavirus": 0.24, "fodbold": 0.19, "europamesterskab": 0.42})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.user1)
        del (self.article1, self.article2, self.article3)

    def runTest(self):
        for a in self.articleList:
            matcher.calculateRelevanceScore(a, self.user1)

        expectedOrderOfRelevanceUser1 = ["1", "2", "3"]
        resultOrderOfRelevanceUser1 = list(self.user1.recommendedArticles.keys())

        # Check if the recommended order is as expected
        self.assertEqual(expectedOrderOfRelevanceUser1, resultOrderOfRelevanceUser1)

        # Check if every relevance score is 0
        for x in list(self.user1.recommendedArticles.values()):
            self.assertEqual(x, 0)
