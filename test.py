from nltk.tokenize import word_tokenize

stopwords = ['to','is','he']
text = "Nick likes to play football, however he is not too fond of tennis. hey Nick"
text_tokens = word_tokenize(text)

tokens_without_sw = [word for word in text_tokens if not word in stopwords]
s = ''
indices = [i for i, x in enumerate(text_tokens) if x == "Nick"]
superset = [i for i in range(1,51)]
print(superset)