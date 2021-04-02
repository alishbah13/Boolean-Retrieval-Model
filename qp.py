from nltk.tokenize import RegexpTokenizer, word_tokenize
import json
from nltk.stem import snowball
import operator
from collections import defaultdict


#### retrieve indexes ####

i_index = defaultdict(lambda: [])
with open("inverted_index.txt") as file1:
    i_index = json.load(file1)

p_index = defaultdict(lambda: [])
with open("positional_index.txt") as file2:
    p_index = json.load(file2)



#### utilities to process boolean ops #####

stemmer = snowball.SnowballStemmer('english')

def and_tok(words):
    term1= stemmer.stem(words[0]) 
    term2= stemmer.stem(words[1]) 

    pst1 = set( i_index[term1][1])
    pst2 = set( i_index[term2][1])

    return list( pst1 & pst2)

def or_tok(words):
    term1= stemmer.stem(words[0]) 
    term2= stemmer.stem(words[1]) 

    pst1 = set( i_index[term1][1])
    pst2 = set( i_index[term2][1])

    return list( pst1 | pst2)
    
def post_and_str(word, postings):
    word = stemmer.stem(word) 
    w_pst = set( i_index[word][1])
    return list( w_pst & set(postings) )

def post_or_str(word, postings):
    word = stemmer.stem(word) 
    w_pst = set( i_index[word][1])
    return list( w_pst | set(postings) )

def not_post(postings):
    superset = set(i for i in range(1,51))
    return list(superset - set(postings) )

def not_str(word):
    word = stemmer.stem(word) 
    superset = set(i for i in range(1,51))
    postings = set( i_index[word][1] )
    return list(superset - postings)

def find_diff(large, small, diff):
        if len(small) > len(large):
            temp = large
            large = small
            small = temp
        mem = [False * i for i in range(100000)]
        for i in small:
            mem[abs(i+diff+1)] = True
        for j in large:
            if mem[j] == True:
                return True
        return False

def get_proximity(query, p):
    result = []

    diff = int( query[p][ 1 : len(query[p]) + 1] )

    term1 = p_index[query[p-1]][1] #dictionary of docs
    term2 = p_index[query[p-2]][1]

    set_a = set( term1.keys() )
    set_b = set( term2.keys() )

    common_docs = list(set_a & set_b) 
    for i in common_docs:
                found = find_diff(term1[i][1], term2[i][1], diff)
                if found:
                    result.append(i)

    return result
    


#### query_processor ####

## 1. /k
## 2. NOT
## 3. AND
## 4. OR

def query_processor(query):
    
    stemmer = snowball.SnowballStemmer('english')
    result = []

    query = word_tokenize(query)
    query = [w.lower() for w in query]

    print(query)


    if '/' in str(query):
        temp = []
        prx_positions = [i for i, x in enumerate(query) if x[:1] == '/']
        for n in range( len(prx_positions)):
            p = prx_positions[n]
            if query[p-2] == 'and':
                del query[p-2]
                prx_positions = prx_positions[0:n] + [prx_positions[p] - 1 for p in range( n, len(prx_positions) )]
        # for p in prx_positions:
        for p in range( len(prx_positions)):
            q = get_proximity(query,prx_positions[p])
            query[ prx_positions[p] ] = q
            del query[ prx_positions[p] -1 ]
            del query[ prx_positions[p] -2 ]
            prx_positions = prx_positions[0:n] + [prx_positions[p] - 2 for p in range( n, len(prx_positions) )]
        
    
    # query = stemmer.stem(x) for x in query
    result = query

    if len(query) == 1:
        word = stemmer.stem(query[0]) 
        result = [i_index[word][1]]

    if 'not' in query:
        while 'not' in query:
        # not_positions = [i for i, x in enumerate(query) if x == 'not']
            nt = query.index('not')
            # for nt in not_positions:
            if type(query[nt + 1]) == str:
                temp = not_str( query[nt+1] )
            elif type(query[ nt + 1]) == list:
                temp = not_post( query[ nt + 1] )
            
            query[nt+1] = temp
            del query[nt]

    if 'and' in query:
        while 'and' in query:
            an = query.index('and')
            if type(query[an-1]) == str and type(query[an+1]) == str:
                temp = list( and_tok([query[an-1], query[an+1]]))
            elif type(query[an-1]) == list and type(query[an+1]) == list:
                temp = list( set (query[an-1]) &  set(query[an+1]) )
            elif type(query[an-1]) == list and type(query[an+1]) == str:
                temp = post_and_str( query[an+1] , query[an-1] )
            elif type(query[an+1]) == list and type(query[an-1]) == str:
                temp = post_and_str( query[an-1] , query[an+1] )
            
            query[an+1] = temp
            del query[an]
            del query[an-1]

    if 'or' in query:
        while 'or' in query:
            r = query.index('r')
            if type(query[r-1]) == str and type(query[r+1]) == str:
                temp = list( and_tok([query[r-1], query[r+1]]))
            elif type(query[r-1]) == list and type(query[r+1]) == list:
                temp = list( set (query[r-1]) &  set(query[r+1]) )
            elif type(query[r-1]) == list and type(query[r+1]) == str:
                temp = post_and_str( query[r+1] , query[r-1] )
            elif type(query[r+1]) == list and type(query[r-1]) == str:
                temp = post_and_str( query[r-1] , query[r+1] )
            
            query[r+1] = temp
            del query[r]
            del query[r-1]
    
    print(sorted(result[0]))
    return sorted(result[0])


# query_processor(query)
