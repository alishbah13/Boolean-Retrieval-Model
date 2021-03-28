from nltk.tokenize import RegexpTokenizer, word_tokenize
import json
from nltk.stem import snowball


#retrieve indexes
with open("inverted_index.txt") as file1:
    i_index = json.load(file1)


with open("positional_index.txt") as file2:
    p_index = json.load(file2)

raw_query = str(input('Enter query: '))
# print(query)
tok_query = word_tokenize(raw_query)
print(tok_query)

def normalize(word):
    low = word.lower()
    stemmer = snowball.SnowballStemmer('english')
    stemmed = stemmer.stem(word)
    return stemmed

def not_tok(word):
    superset = set([i for i in range(1,51)])
    docs = set(i_index[word])
    return superset - docs
    
query = []
for i in tok_query:
    query.append(normalize(i))
    
## one word
if len(tok_query) == 1:
    result = i_index[tok_query[0]]
    # del result[0]
# elif len(tok_query) == 2 and tok_query[0] == not:


print(result)

### proximity
# for x in tok_query:
#     if '/' in x:
#         print('true')