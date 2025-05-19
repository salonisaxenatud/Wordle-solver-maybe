import re
from collections import Counter
from operator import itemgetter

import requests


# from : iancward/five_letter_words.py
def fetch_word_list():
    print('Fetching word list')
    # get list of five-letter words from meaningpedia.com
    # found it linked from Wikipedia:
    # https://en.wikipedia.org/wiki/Lists_of_English_words#External_links
    meaningpedia_resp = requests.get(
        "https://meaningpedia.com/5-letter-words?show=all")

    # get list of words by grabbing regex captures of response
    # there's probably a far better way to do this by actually parsing the HTML
    # response, but I don't know how to do that, and this gets the job done

    # compile regex
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    # find all matches
    word_list = pattern.findall(meaningpedia_resp.text)
    word_counter = Counter()
    for result in word_list:
        word = result.lower().rstrip()
        # print('Tabulating: {}'.format(word))
        for letter in set(word):
            word_counter[letter] += 1

    # sort output
    sorted_letters = sorted(word_counter.items(), key=itemgetter(1), reverse=True)
    return word_list, sorted_letters



# finding the word with the highest frequency of letters, no repeats
def find_highest_freq_word(word_list, sorted_letters):
    highest_freq_word = ''
    highest_freq_count = 0
    for word in word_list:
        freq_count = sum([word.count(letter[0]) * letter[1] for letter in sorted_letters])
        if freq_count > highest_freq_count and len(set(word)) == len(word):
            highest_freq_count = freq_count
            highest_freq_word = word
    return highest_freq_word, highest_freq_count

if __name__ == "__main__":
    word_list, sorted_letters = fetch_word_list()
    highest_freq_word, highest_freq_count = find_highest_freq_word(word_list, sorted_letters)
    print(f"Highest frequency word: {highest_freq_word} with count: {highest_freq_count}")