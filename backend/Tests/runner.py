from backend.Tests.ArticleProfiler_filterNouns_test import *
from backend.Tests.ArticleProfiler_rankNouns_test import *
from backend.Tests.MatchingAlgorithm_calculateRelevance_test import *

def suite():
    testSuite = unittest.TestSuite()

    # Add filterNouns testCases
    testSuite.addTest(filterNouns_ideal())
    testSuite.addTest(filterNouns_emptyText())
    testSuite.addTest(filterNouns_punctuation())
    testSuite.addTest(filterNouns_multiples())
    testSuite.addTest(filterNouns_homogenousText())
    testSuite.addTest(filterNouns_filterHeadline())
    testSuite.addTest(filterNouns_filterExcerpt())
    testSuite.addTest(filterNouns_filterNames())
    testSuite.addTest(filterNouns_filterLocations())
    testSuite.addTest(filterNouns_filterOrganisations())
    testSuite.addTest(filterNouns_mixedWeights())
    testSuite.addTest(filterNouns_lemmatizer())

    # Add rankNouns testCases
    testSuite.addTest(rankNouns_ideal())
    testSuite.addTest(rankNouns_overproportional())
    testSuite.addTest(rankNouns_homogenous())
    testSuite.addTest(rankNouns_oneEmptyInDataset())
    testSuite.addTest(rankNouns_rankingEmpty())

    # Add calculateRelevance testCases
    testSuite.addTest(calculateRelevance_ideal())
    testSuite.addTest(calculateRelevance_perfectMatch())
    testSuite.addTest(calculateRelevance_noMatch())

    return testSuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
