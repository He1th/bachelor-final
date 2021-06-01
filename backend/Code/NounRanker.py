import math


def rankNouns(nounDict, dataset, tf_compareCount):
    unsortedTerms = {}
    for term in nounDict:
        tf_score = nounDict[term] / tf_compareCount

        count = 0
        for a in dataset:
            if term in a.nouns:
                count += 1

        if count is 0:
            count = 1

        idf_score = math.log10((len(dataset) / count))
        tf_idf_score = tf_score * idf_score
        unsortedTerms[term] = tf_idf_score

    return sortNounScore(unsortedTerms)


def sortNounScore(scores):
    sortedNounScores = {}

    sortedkeys = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for e in sortedkeys:
        sortedNounScores[e[0]] = e[1]

    return sortedNounScores
