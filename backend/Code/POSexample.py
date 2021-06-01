from danlp.models import load_spacy_model

model_path = "../Model"

nlp = load_spacy_model(model_path, verbose=True)

testSentence = "Hej mit navn er Peter. Jeg arbejder på universitet."
analyzed = nlp(testSentence)
print(testSentence)

for token in analyzed:
    print("%s<%s>" %(token, token.pos_), end=" ")