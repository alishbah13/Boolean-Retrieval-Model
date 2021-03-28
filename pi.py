from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.stem import snowball
from collections import defaultdict


##### stop words list
f = open("Stopword-List.txt","r")
stop_words=[]
for lines in f:
    stop_words.append(lines.strip())
f.close()


#### retrieve stories text AS ONE STRING
stories = ""
for i in range(1,51):
    ss = open( "ShortStories/" + str(i) + ".txt","r")
    for text in ss:
        # stories.append(text.strip())
        stories = stories + text.strip() + " "
    ss.close()    


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



#### form positional index

## all file data at each index. type = 2d arr
files = [[]]
for j in range(1,51):
    text = ""
    f = open( "ShortStories/" + str(j) + ".txt","r")
    for lines in f:
        text = text + lines.strip() + " "
    f.close()
    docid_tokens = tokenizer.tokenize(text)
    # case fold to lowercase
    docid_words = [w.lower() for w in docid_tokens]
    #remove stopwords
    wo_stopwords = [wrd for wrd in docid_words if not wrd in stop_words]
    files.append(wo_stopwords)


##### form positional index 
p_index = defaultdict(dict)

for word in dictionary:
    # p_index[word] = []
    posting_list = []
    docs = 0
    for docid in range(1,51):
        temp = {}
        positions = [i for i, x in enumerate(files[docid]) if x == word]
        if len(positions) > 0 :
            temp[docid] = [len(positions), positions]
            posting_list.append(temp)
            docs += 1
    p_index[word] = [docs, posting_list]

print(p_index['write'])

