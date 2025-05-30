# from : iancward/five_letter_words.py

# stdlib
import re
from collections import Counter
from operator import itemgetter

# third party
import requests

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

# create counter dictionary
word_counter = Counter()

# loop over word_list, counting letters
for result in word_list:
    word = result.lower().rstrip()
    # print('Tabulating: {}'.format(word))
    for letter in set(word):
        word_counter[letter] += 1

# sort output
sorted_letters = sorted(word_counter.items(), key=itemgetter(1), reverse=True)

print("\nLetters sorted by frequency:")
for letter in sorted_letters:
    print('{}: {}'.format(letter[0], letter[1]))