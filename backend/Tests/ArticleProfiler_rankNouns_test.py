import unittest

from backend.Code.Article import Article
from backend.Code.ArticleProfiler import ArticleProfiler


profiler = ArticleProfiler("../Model")

class rankNouns_ideal(unittest.TestCase):

    def setUp(self):
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 4, "lektier": 2})
        self.article2 = Article("1", "testTime", "testAuthor", "", "", "peter peter bil ulykke ulykke ulykke", nouns={"peter": 2, "bil": 1, "ulykke": 3})
        self.article3 = Article("1", "testTime", "testAuthor", "", "", "hans hans hans hans hans hans ulykke ulykke lektier lektier", nouns={"hans": 5, "ulykke": 2, "lektier": 2})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del(self.article1, self.article2, self.article3)

    def runTest(self):
        expectedOutcome = {"skole": 0.04241, "lektier": 0.007826, "peter": 0.003913}
        profiler.rankNouns(self.article1, self.articleList)
        
        for x in range(0, len(expectedOutcome)-1):
            self.assertAlmostEqual(list(expectedOutcome.values())[x], list(self.article1.nounScore.values())[x], places=4)


class rankNouns_overproportional(unittest.TestCase):
    def setUp(self):
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 40, "lektier": 2})
        self.article2 = Article("1", "testTime", "testAuthor", "", "", "peter peter bil ulykke ulykke ulykke", nouns={"peter": 2, "bil": 1, "ulykke": 3})
        self.article3 = Article("1", "testTime", "testAuthor", "", "", "hans hans hans hans hans hans ulykke ulykke lektier lektier", nouns={"hans": 5, "ulykke": 2, "lektier": 2})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del(self.article1, self.article2, self.article3)
        del self.articleList

    def runTest(self):
        expectedOutcome = {"skole": 0.07312, "lektier": 0.001349, "peter": 0.0006747}
        profiler.rankNouns(self.article1, self.articleList)

        for x in range(0, len(expectedOutcome)-1):
            self.assertAlmostEqual(list(expectedOutcome.values())[x], list(self.article1.nounScore.values())[x], places=4)


class rankNouns_homogenous(unittest.TestCase):
    def setUp(self):
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 4, "lektier": 2})
        self.article2 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 4, "lektier": 2})
        self.article3 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 4, "lektier": 2})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.article1, self.article2, self.article3)
        del self.articleList

    def runTest(self):
        expectedOutcome = {"skole": 0, "lektier": 0, "peter": 0}
        profiler.rankNouns(self.article1, self.articleList)

        for x in range(0, len(expectedOutcome)-1):
            self.assertEqual(list(expectedOutcome.values())[x], list(self.article1.nounScore.values())[x])


class rankNouns_oneEmptyInDataset(unittest.TestCase):
    def setUp(self):
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "peter skole skole skole skole lektier lektier", nouns={"peter": 1, "skole" : 4, "lektier": 2})
        self.article2 = Article("1", "testTime", "testAuthor", "", "", "", nouns={})
        self.article3 = Article("1", "testTime", "testAuthor", "", "", "hans hans hans hans hans hans ulykke ulykke lektier lektier", nouns={"hans": 5, "ulykke": 2, "lektier": 2})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.article1, self.article2, self.article3)
        del self.articleList

    def runTest(self):
        expectedOutcome = {"skole": 0.04241, "peter": 0.01060, "lektier": 0.007826}
        profiler.rankNouns(self.article1, self.articleList)

        for x in range(0, len(expectedOutcome)-1):
            self.assertAlmostEqual(list(expectedOutcome.values())[x], list(self.article1.nounScore.values())[x], places=4)


class rankNouns_rankingEmpty(unittest.TestCase):
    def setUp(self):
        self.article1 = Article("1", "testTime", "testAuthor", "", "", "", nouns={})
        self.article2 = Article("1", "testTime", "testAuthor", "", "", "peter peter bil ulykke ulykke ulykke", nouns={"peter": 2, "bil": 1, "ulykke": 3})
        self.article3 = Article("1", "testTime", "testAuthor", "", "", "hans hans hans hans hans hans ulykke ulykke lektier lektier", nouns={"hans": 5, "ulykke": 2, "lektier": 2})
        self.articleList = [self.article1, self.article2, self.article3]

    def tearDown(self):
        del (self.article1, self.article2, self.article3)
        del self.articleList

    def runTest(self):
        expectedOutcome = {}
        profiler.rankNouns(self.article1, self.articleList)

        self.assertEqual(self.article1.nounScore, expectedOutcome)
