from nltk.tokenize import word_tokenize

# stopwords = ['to','is','he']
# text = "Nick likes to play football, however he is not too fond of tennis. hey Nick"
# text_tokens = word_tokenize(text)

# tokens_without_sw = [word for word in text_tokens if not word in stopwords]
# s = ''
# indices = [i for i, x in enumerate(text_tokens) if x == "Nick"]
# superset = [i for i in range(1,51)]
# print(superset)

def find_diff(large, small, diff):
    if len(small) > len(large):
        temp = large
        large = small
        small = temp
    mem = [False * i for i in range(9999)]
    # result = []
    for i in small:
        mem[abs(i+diff+1)] = True
    for j in large:
        if mem[j] == True:
            # result.append(j) 
            return True
    # return result 
    return False

l1 = [705,1706]
l2 = [701]
print(find_diff(l1,l2,3))