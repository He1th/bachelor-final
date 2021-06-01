import unittest

from backend.Code.Article import Article
from backend.Code.ArticleProfiler import ArticleProfiler

profiler = ArticleProfiler("../Model", headlineWeight=2, excerptWeight=1.5, textWeight=1, nounWeight=1, personWeight=1.1, locationWeight=1.2, organisationWeight=1.3)


class filterNouns_ideal(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Der kom en soldat marcherende hen ad landevejen:" \
                            "én, to! én, to! Han havde sit tornyster på ryggen og en sabel ved siden," \
                            "for han havde været i krigen, og nu skulle han hjem."
        sentenceNouns = {"soldat": 1,
                         "landevej": 1,
                         "tornyster": 1,
                         "ryg": 1,
                         "sabel": 1,
                         "krig": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_emptyText(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        sentenceNouns = {}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_punctuation(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Der. kom, en; soldat: marcherende' hen ad landevejen:" \
                            "én, to! én, to! Han havde sit tornyster? på´ ryggen! og en sabel' ved siden," \
                            "for han havde været i! krigen, og nu skulle han hjem."

        sentenceNouns = {"soldat": 1,
                         "landevej": 1,
                         "tornyster": 1,
                         "ryg": 1,
                         "sabel": 1,
                         "krig": 1}
        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_multiples(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Der kom en soldat marcherende. En soldat med en tornyster på ryggen. Den tornyster var fyldt med sten."

        sentenceNouns = {"soldat": 2,
                         "tornyster": 2,
                         "ryg": 1,
                         "sten": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_homogenousText(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "soldat soldat soldat soldat soldat soldat soldat soldat soldat soldat soldat"

        sentenceNouns = {"soldat": 11}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_filterHeadline(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.headline = "Der kom en soldat marcherende. En soldat med en tornyster på ryggen. Den tornyster var fyldt med sten."

        sentenceNouns = {"soldat": 4,
                         "tornyster": 4,
                         "ryg": 2,
                         "sten": 2}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_filterExcerpt(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.excerpt = "Der kom en soldat marcherende. En soldat med en tornyster på ryggen. Den tornyster var fyldt med sten."

        sentenceNouns = {"soldat": 3,
                         "tornyster": 3,
                         "ryg": 1.5,
                         "sten": 1.5}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_filterNames(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Peter kom gående på vejen. Her mødte han Frederikke som Peter kender fra skolen."

        sentenceNouns = {"peter": 2.2,
                         "vej": 1,
                         "frederikke": 1.1,
                         "skole": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_filterLocations(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Odense er en af de største byer i danmark. Hovedstaden af Sverige er Oslo."

        sentenceNouns = {"odense": 1.2,
                         "by": 1,
                         "danmark": 1.2,
                         "hovedstad": 1,
                         "sverige": 1.2,
                         "oslo": 1.2}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_filterOrganisations(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Socialdemokratiet er et parti i folketinget. Danfoss er et firma i landet"

        sentenceNouns = {"socialdemokratiet": 1.3,
                         "parti": 1,
                         "folketing": 1,
                         "danfoss": 1.3,
                         "firma": 1,
                         "land": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)


class filterNouns_mixedWeights(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.headline = "Vestas i tyskland. Patrick på toppen."
        self.article.excerpt = "Danfoss i sverige. Søren på gaden."
        self.article.text = "Socialdemokratiet i danmark. Mette i huset."


        sentenceNouns = {"vestas": 2.6,
                         "tyskland": 2.4,
                         "patrick": 2.2,
                         "top": 2,
                         "danfoss": 1.95,
                         "sverige": 1.8,
                         "søren": 1.65,
                         "gade": 1.5,
                         "socialdemokratiet": 1.3,
                         "danmark": 1.2,
                         "mette": 1.1,
                         "hus": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)

class filterNouns_lemmatizer(unittest.TestCase):
    def setUp(self):
        self.article = Article("1", "testTime", "testAuthor", "", "", "")

    def tearDown(self):
        del self.article

    def runTest(self):
        self.article.text = "Nielsen gik på gaden. Han mødte Johannsen fra Socialdemokratiet hvor de spiller med fodbolde"

        sentenceNouns = {"nielsen": 1.1,
                         "gade": 1,
                         "johannsen": 1.1,
                         "socialdemokratiet": 1.3,
                         "fodbold": 1}

        profiler.filterNouns(self.article)
        self.assertEqual(sentenceNouns, self.article.nouns)