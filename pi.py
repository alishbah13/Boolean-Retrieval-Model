from nltk.tokenize import RegexpTokenizer
from nltk.stem import snowball
from collections import defaultdict

#### retrieve stories text AS ONE STRING
stories = ""
for i in range(1,51):
    ss = open( "ShortStories/" + str(i) + ".txt","r")
    for text in ss:
        # stories.append(text.strip())
        stories = stories + " " + text.strip()
    ss.close()    



#### form dictionary - W/O STEMMING

# tokenize raw text (stories) - remove punctuation
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(stories)
# case fold to lowercase
words = [w.lower() for w in tokens]


#### form positional index

## all file data at each index. type = str
files = []
for j in range(1,51):
    text = ""
    f = open( "ShortStories/" + str(j) + ".txt","r")
    for lines in f:
        text = text + lines.strip()
    f.close()
    docid_tokens = tokenizer.tokenize(text)
    # case fold to lowercase
    docid_words = [w.lower() for w in docid_tokens]
    files.append(docid_stem)



