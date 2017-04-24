import requests
import pickle
import string
import operator
import math
import random
from os.path import exists
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def save_book(book_name, link):
    '''saves text of book under book_name(stirng)
    from link(string) on project gutenberg'''
    f = open(book_name + '.pickle', 'wb')
    book_text = requests.get(link).text
    pickle.dump(book_text, f)
    f.close


def get_book(book_name):
    '''returns text of book saved under book_name(string).pickle'''
    file_name = book_name + '.pickle'
    if not exists(file_name):
        return 'book not saved'
    else:
        f = open(book_name + '.pickle', 'rb')
        text = pickle.load(f)
    return text


def save_and_get_book(book_name, link):
    '''combines save and get book functions (book_name is string)'''
    save_book(book_name, link)
    text = get_book(book_name)
    return text


def read(text):
    '''returns text(string) as list of the words with
    whitespace and punctuatio stripped'''
    text_read = []
    if not text == 'book not saved':
        word = ''
        start = 0
        for i in range(len(text)):
            if text[i] in string.whitespace:
                end = i
                word = text[start:end]
                text_read.append(word)
                start = i + 1
        return text_read
    else:
        print('not a book')


# TODO strip the book text of stuff before/after

def word_frequency(word_list):
    '''takes in word_list(list) and returns dictionary
    with keys=words and values=frequencies'''
    d = dict()
    for w in word_list:
        frequency = d.get(w, 0)
        d[w] = frequency + 1
    return d


def sort_dict(d):
    '''takes in a dictionary and sorts by decreasing order of values'''
    sorted_dict = sorted(d.items(), reverse=True, key=operator.itemgetter(1))
    return sorted_dict


def top_x_words(x, sorted_dict):
    '''prints the x(int) most frequent words in sorted_dict(dictionary)
    sorted by most to least frequent words'''
    for w in sorted_dict[0:x]:
        print(w)


def analyze_sentiment(text):
    ''''''
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)


def analyze(book_name, link):
    ''''''
    save_book(book_name, link)
    text = get_book(book_name)
    read_text = read(text)
    frequency_dict = word_frequency(read_text)
    return frequency_dict


def find_tfidf(dict_list):
    '''finds tfidf from list of dictionaries'''
    res_list = []
    for d in dict_list:
        count = sum([d[i] for i in d.keys()])
        tfidf_dict = dict()
        for w in d.keys():
            # find tf
            tf = d[w]/count
            # find n containing
            n_containing = sum([1 for val in dict_list if w in val])
            # find idf
            idf = math.log(len(dict_list)/(n_containing))
            # tf*idf
            tfidf_dict[w] = tf*idf
        res_list.append(tfidf_dict)
    return res_list

def analyze_tfidf(dict_list):
    '''uses sorts and prints dict_list for TF-IDF dict'''
    sorted_dict_list = []
    for i, d in enumerate(dict_list):
        sorted_dict = sort_dict(d)
        sorted_dict_list = sorted_dict_list + sorted_dict
        print("document {}: ".format(i+1))
        for word, score in sorted_dict[:5]:
            print('\tWord: {}, TF-IDF: {}'.format(word, round(score, 5)))

def markoff_analyis(word_list, length):
    '''takes in list of words, returns dictionary mapping prefixes to suffixes
    length is lenght of prefixes and suffixes'''
    markoff_dict = dict()
    for i, w in enumerate(word_list[:-(length+1)]):
        suffix_list = markoff_dict.get(w + word_list[i+1], [])
        markoff_dict[w] = suffix_list + [word_list[i+length]]
    return markoff_dict

def markoff_chain(length, text_1, text_2):
    markoff_1 = markoff_analyis(text_1, 1)
    markoff_2 = markoff_analyis(text_2, 1)
    keys_1 = list(markoff_1.keys())
    keys_2 = list(markoff_2.keys())

    # Randomly chooses text_1 or text_2 and randomly chooses word from keys of
    # dictionary
    if random.randint(0,10) < 5:
        keys = keys_1
        print(type(keys))
        key = keys[random.randint(0, len(keys))]
        word = markoff_1[key]
    else:
        keys = keys_2
        print(type(keys))
        key = keys[random.randint(0, len(keys))]
        word = markoff_2[key]

    # sets return variable text to randomly chosen word
    text = str(word[0])
    for i in range(length):
        new_word = ''
        if random.randint(0, 10) < 5 and word in keys_1:
            suffixes = markoff_1[word]
        elif word in keys_2:
            suffixes = markoff_2[word]
        else:
            if random.randint(0, 10) > 5:
                suffixes = keys_1
            else:
                suffixes = keys_2
        new_word = suffixes[random.randint(0, len(suffixes))]
        text = text + ' ' + new_word
    print(text)


text = get_book('pride_and_prejudice') + get_book('pride_and_prejudice') + \
       get_book('sense_and_sensibility') + get_book('persuasion')
austen_word_list = read(text)

text = get_book('adventures_of_sherlock') + get_book('study_in_scarlet') + \
       get_book('memiors_of_sherlock') + get_book('sign_of_four')
sherlock_word_list = read(text)

markoff_chain(20, austen_word_list, sherlock_word_list)
