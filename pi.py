from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.stem import snowball
from collections import defaultdict
import json

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
word = set([wrd for wrd in lower_words if not wrd in stop_words])
dictionary = list(word)
print(dictionary)


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
    print(docid_words)
    files.append(docid_words)



##### form positional index
 
p_index = defaultdict(dict)
for word in dictionary:
    posting_list = []
    docs = 0
    temp = {}
    for docid in range(1,51):
        positions = [i for i, x in enumerate(files[docid]) if x == word]
        if len(positions) > 0 :
            temp[docid] = [len(positions), positions]
            docs += 1
    p_index[word] = [docs, temp]

with open('positional_index.txt', 'w') as file2:
     file2.write(json.dumps(p_index)) # use `json.loads` to do the reverse
file2.close()