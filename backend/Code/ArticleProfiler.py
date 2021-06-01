import ssl
import lemmy.pipe
from danlp.models import load_spacy_model
from . import NounRanker


class ArticleProfiler:
    def __init__(self, model_path="Model", headlineWeight=2, excerptWeight=1.5, textWeight=1, nounWeight=1,
                 personWeight=1.1, locationWeight=1.1, organisationWeight=1.1):

        self.nlp = load_spacy_model(model_path, verbose=True)
        try:
            self.pipe = lemmy.pipe.load('da')
            self.nlp.add_pipe(self.pipe, after="tagger")
        except:
            print("lemmetization has already been added to the pipeline")

        self.headlineWeight = headlineWeight
        self.excerptWeight = excerptWeight
        self.textWeight = textWeight

        self.nounWeight = nounWeight
        self.personWeight = personWeight
        self.locationWeight = locationWeight
        self.organisationWeight = organisationWeight

    ssl._create_default_https_context = ssl._create_unverified_context

    def filterNouns(self, article):
        nouns = {}
        doc = self.nlp(article.text)
        headDoc = self.nlp(article.headline)
        excerptDoc = self.nlp(article.excerpt)

        for token in doc:
            useLemma = False
            tokenText = token.text.lower().replace("\\", "")
            if (token.pos_ == "NOUN" or token.ent_type_ != "" and len(tokenText) > 1):
                if (token.ent_type_ == "PER"):
                    frequency = self.personWeight * self.textWeight
                elif (token.ent_type_ == "LOC"):
                    frequency = self.locationWeight * self.textWeight
                elif (token.ent_type_ == "ORG"):
                    frequency = self.organisationWeight * self.textWeight
                else:
                    frequency = self.nounWeight * self.textWeight
                    useLemma = True

                if useLemma:
                    self.insertIntoNouns(token._.lemmas[0].lower(), nouns, frequency)
                else:
                    self.insertIntoNouns(tokenText, nouns, frequency)

        for token in excerptDoc:
            useLemma = True
            tokenText = token.text.lower().replace("\\", "")
            if (token.pos_ == "NOUN" or token.ent_type_ != "" and len(tokenText) > 1):
                if (token.ent_type_ == "PER"):
                    frequency = self.personWeight * self.excerptWeight
                elif (token.ent_type_ == "LOC"):
                    frequency = self.locationWeight * self.excerptWeight
                elif (token.ent_type_ == "ORG"):
                    frequency = self.organisationWeight * self.excerptWeight
                else:
                    frequency = self.nounWeight * self.excerptWeight
                    useLemma = True

                if useLemma:
                    self.insertIntoNouns(token._.lemmas[0].lower(), nouns, frequency)
                else:
                    self.insertIntoNouns(tokenText, nouns, frequency)

        for token in headDoc:
            useLemma = False
            tokenText = token.text.lower().replace("\\", "")
            if (token.pos_ == "NOUN" or token.ent_type_ != "" and len(tokenText) > 1):
                if (token.ent_type_ == "PER"):
                    frequency = self.personWeight * self.headlineWeight
                elif (token.ent_type_ == "LOC"):
                    frequency = self.locationWeight * self.headlineWeight
                elif (token.ent_type_ == "ORG"):
                    frequency = self.organisationWeight * self.headlineWeight
                else:
                    frequency = self.nounWeight * self.headlineWeight
                    useLemma = True

                if useLemma:
                    self.insertIntoNouns(token._.lemmas[0].lower(), nouns, frequency)
                else:
                    self.insertIntoNouns(tokenText, nouns, frequency)

        article.nouns = nouns

    def rankNouns(self, article, dataset):
        articleLength = (len(article.text) + len(article.headline) + len(article.excerpt))
        article.nounScore = NounRanker.rankNouns(article.nouns, dataset, articleLength)

    def insertIntoNouns(self, tokenText, nouns, frequency):
        if tokenText in nouns:
            nouns[tokenText] = nouns.get(tokenText) + round(frequency, 2)
        else:
            nouns[tokenText] = round(frequency, 2)

    def updateParameters(self, hl=None, ex=None, tx=None, noun=None, name=None, loc=None, org=None):
        self.headlineWeight = float(hl) if hl is not None else float(self.headlineWeight)
        self.excerptWeight = float(ex) if ex is not None else float(self.excerptWeight)
        self.textWeight = float(tx) if tx is not None else float(self.textWeight)
        self.nounWeight = float(noun) if noun is not None else float(self.nounWeight)
        self.personWeight = float(name) if name is not None else float(self.personWeight)
        self.locationWeight = float(loc) if loc is not None else float(self.locationWeight)
        self.organisationWeight = float(org) if org is not None else float(self.organisationWeight)
