import collections
import time
import pprint

valuepoints = {
    0: '?',
    1: 'EAIONRTLSU',
    2: 'DG',
    3: 'BCMP',
    4: 'FHVWY',
    5: 'K',
    8: 'JX',
    10: 'QZ'
}

def convert_value_points(l):
    retval = {}
    for i in l:
        for j in valuepoints[i]:
            retval[j] = i
    return retval

def get_word_point_value(word, point_values):
    retval = 0
    for i in word:
        if i.islower():
            retval+=point_values[i.upper()]
    return retval

def evaluate_true_value(word, point_value, lengths, verbose=False):
    #get value of the current word:
    value = get_word_point_value(word,point_value)
    count = 0
    #get values of all words that are composed in this word
    for i in range(len(word)-1,0, -1):
        if not lengths.get(i):
            continue
        for wordword in lengths[i]:
            if wordword in word.lower():
                count+=1
                print ('Found word: {}, count: {}'.format(wordword, count))
                value += get_word_point_value(wordword, point_value)
    return value

def remove_word_from_pool(word, pool):
    poolc = pool
    ret_blanks = ''
    for letter in word:
        if letter.upper() not in poolc:
            if '?' not in poolc:
                raise KeyError('Letter {} missing from pool!'.format(letter))

            poolc = poolc.replace('?', "", 1)
            ret_blanks +=letter.lower()
            continue
        poolc = poolc.replace(letter.upper(), "", 1)
    #print (poolc)
    return poolc, ret_blanks

def is_word_in_pool(word,pool):
    try:
        remove_word_from_pool(word, pool)
    except KeyError as e:
       # print ('{} is not in the pool'.format(word))
        return False
    return True

def main():
    pool = 'E'*12 + 'A'*9 + 'I'*9 +'O'*8+'N'*6 + 'R'*6 + 'T'* 6+ 'L' * 4+'S'*4 + 'U' *4
    pool += 'D'*4 + 'G' * 3 + 'BBCCMMPPFFHHVVWWYYKJXQZ??'
    orig_pool = pool
    point_values = convert_value_points(valuepoints)

    with open('wordlist.txt', 'r') as f:
        lines = f.read()
    words = lines.split()

    lengths = collections.defaultdict(list)
    for i in words:
        lengths[len(i)].append(i)

    '''
    words is the list of words
    lengths is a dict with all of the words indexed by length
    point_values is the point values of each letter
    get_word_point_value is a list of pointvalues for each word 
    '''

    '''
    Calculate True value of a word
    true_value_of_word = {}
    counter = 0
    start = time.time()
    for word in words:
        counter += 1
        true_value_of_word[word] = evaluate_true_value(word, point_values, lengths)
        if counter % 1000 == 0:
            end = time.time()
            print (counter, end-start)
            start = time.time()
    with open ('true_word_list.txt', 'w') as f:
        for i in true_value_of_word:
            f.write('{} {}\n'.format(i, true_value_of_word[i]))
    '''
    with open ('true_word_list.txt', 'r') as f:
        lines = f.readlines()

    word_with_values = []
    for line in lines:
        word_with_values.append(tuple(line.split()))
    word_with_values.sort(key=lambda x: int(x[1]), reverse=True)
    max_score = 0
    max_seq= ''
    for q in range(1):
        pool = orig_pool
        res = ''
        for entry in word_with_values[q:]:
            if is_word_in_pool(entry[0], pool):
                pool, ret_blanks = remove_word_from_pool(entry[0], pool)
                if ret_blanks:
                    for i in ret_blanks:
                        e = entry[0].replace(i.lower(), i.upper(),1)
                        print (e)
                res += ' ' + (e or entry[0])
                e = None

                print (res, pool)


        #print (pool)
        #pool = remove_word_from_pool(word_with_values[0][0], pool)
        #print (is_word_in_pool(word_with_values[0][0], pool))
        score = evaluate_true_value(res.replace(' ', "") + pool.lower(), point_values, lengths, verbose=False)
        print (res, pool, score)
        if score > max_score:
            max_score=score
            max_seq = res  + ' ' + pool.lower()

    print('THE WINNAR IS: {}'.format(max_seq))
    print('Score: {}'.format(max_score))

    print ('!!' + str(evaluate_true_value('unsympatheticallymicroPHotographersreafforestationsreawakeneddeoxidizedbejewellingquantingobiaiouuvv', point_values, lengths, verbose=True)))

if __name__ == "__main__":
    main()
