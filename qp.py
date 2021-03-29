from nltk.tokenize import RegexpTokenizer, word_tokenize
import json
from nltk.stem import snowball
import operator
from collections import defaultdict

def process_query(raw_query):
    #retrieve indexes
    i_index = defaultdict()
    with open("inverted_index.txt") as file1:
        i_index = json.load(file1)

    p_index = defaultdict()
    with open("positional_index.txt") as file2:
        p_index = json.load(file2)

    def not_tok(word):
        superset = set([i for i in range(1,51)])
        docs = set(i_index[word][1])
        return list(superset - docs)

    def and_tok(words):
        temp = set(i_index[words[0]][1])
        for i in range(1, len(words)):
            set_y = set(i_index[words[i]][1])
            temp = temp & set_y
        result = temp
        return list(result)


    def or_tok(words):
        temp = set(i_index[words[0]][1])
        for i in range(1, len(words)):
            set_y = set(i_index[words[i]][1])
            temp = temp | set_y
        result = temp
        return list(result)

    ## dk if needed 
    def descending_freq(words):
        freq = {words[0]:i_index[words[0]][0],
                words[1]:i_index[words[1]][0],
                words[2]:i_index[words[2]][0]}
        desc = sorted(freq.items(),key=operator.itemgetter(1),reverse=True)
        # desc[0][0] , desc[0][1] are words in desc order
        return desc

    ## proximity check utility
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


    ###### get query

    # raw_query = str(input('Enter query: '))
    tok_query = word_tokenize(raw_query)
    query = [w.lower() for w in tok_query]
    print(tok_query)


    prox_q = tok_query
    stemmer = snowball.SnowballStemmer('english')
    # query = list( sorted( set([stemmer.stem(x) for x in tok_query])) )
    query = tok_query
    result = []
    # priority of processing -> NOT > AND > OR > /k :. accordingly weighted
        #process NOT
    if len(query) == 1:
        result = i_index[query[0]][1]
    if 'not' in query:
        positions = [i for i, x in enumerate(query) if x == 'not']
        for nt in range(len(positions)):
            print("xxx" ,query)
            query[nt+1] = not_tok(query[nt+1])
            # del query[nt]
            if len(query)==2:
                result = query[1]
            del query[nt]
    #process AND
    if 'and' in query:
        and_positions = [i for i, x in enumerate(query) if x == 'and']
        for an in and_positions:
            if type(query[an-1]) == str and type(query[an+1]) == str:
                result =list( and_tok([query[an-1], query[an+1]]))
            elif type(query[an-1]) == list and type(query[an+1]) == list:
                result = list(query[an-1] & query[an+1])
            elif type(query[an-1]) == list and type(query[an+1]) == str:
                set_temp = set(i_index[query[an+1]][1])
                result = list( set(query[an-1]) & set_temp) 
            elif type(query[an+1]) == list and type(query[an-1]) == str:
                set_temp = set(i_index[query[an-1]][1])
                result = list(set(query[an-1]) & set_temp)
    # process OR            
    if 'or' in query:
        or_positions = [i for i, x in enumerate(query) if x == 'or']
        for an in or_positions:
            if type(query[an-1]) == list and type(query[an+1]) == list:
                result = list( query[an-1] | query[an+1])
            elif type(query[an-1]) == str and type(query[an+1]) == str:
                result = list( or_tok([query[an-1], query[an+1]]) )
            elif type(query[an-1]) == list and type(query[an+1]) == str:
                set_temp = set(i_index[query[an+1]][1])
                result = list(set(query[an-1]) | set_temp)
            elif type(query[an+1]) == list and type(query[an-1]) == str:
                set_temp = set(i_index[query[an-1]][1])
                result = list(set(query[an-1]) | set_temp)
    # process /k            
    if '/' in str(query):
        prx_positions = [i for i, x in enumerate(prox_q) if x[:1] == '/']
        for p in prx_positions:
            diff = int(prox_q[p][1:len(prox_q[p])+1])
            term1 = p_index[prox_q[p-1]][1] #dictionary of docs
            term2 = p_index[prox_q[p-2]][1]
            common_docs = ( term1.keys() & term2.keys() )
            for i in common_docs:
                found = find_diff(term1[i][1], term2[i][1], diff)
                if found:
                    result.append(i)
    return result

