from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
from nltk.stem import snowball


##### stop words list
f = open("Stopword-List.txt","r")
stop_words=[]
for lines in f:
    stop_words.append(lines.strip())
f.close()
# print(stop_words)

# retrieve stories text AS ONE STRING
stories = ""
for i in range(1,51):
    ss = open( "ShortStories/" + str(i) + ".txt","r")
    for text in ss:
        # stories.append(text.strip())
        stories = stories + text.strip() + " "
    ss.close()    
# print(stories)




#### form dictionary

# tokenize raw text (stories) - remove punctuation
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(stories)
# case fold to lowercase
lower_words = [w.lower() for w in tokens]
#remove stop words
words = [wrd for wrd in lower_words if not wrd in stop_words]
# stem and order alphabetically
stemmer = snowball.SnowballStemmer('english')
dictionary = list( sorted( set([stemmer.stem(x) for x in words])) )



#### inverted index

i_index = defaultdict(list)

# all file data at each index. type = str
files = []
for j in range(1,51):
    text = ""
    f = open( "ShortStories/" + str(j) + ".txt","r")
    for lines in f:
        text = text + lines.strip() + " "
    f.close()
    docid_tokens = tokenizer.tokenize(text)
    # case fold to lowercase
    docid_words = [w.lower() for w in docid_tokens]
    wo_stopwords = [wrd for wrd in docid_words if not wrd in stop_words]
    # stem and order alphabetically
    docid_stem = list( sorted( set([stemmer.stem(x) for x in wo_stopwords])) )
    files.append(docid_stem)


for word in dictionary:
    # i_index[word]
    for docid in range(1,51):
        if word in files[docid-1]:
            i_index[word].append(docid)
    l = len(i_index[word])
    # the 0th element of the key-value list = frequency of documents for 'word'
    i_index[word].insert(0,l) 

print(i_index.keys())


