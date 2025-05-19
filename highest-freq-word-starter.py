import re
from collections import Counter
from operator import itemgetter

import requests

# from : iancward/five_letter_words.py but modified to use https://www.wordunscrambler.net/word-list/wordle-word-list
from bs4 import BeautifulSoup
def fetch_word_list():
    print('Fetching word list')

    # to avoid getting blocked by website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resp = requests.get(
        "https://www.wordunscrambler.net/word-list/wordle-word-list",
        headers=headers
    )
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    word_list = [li.text.strip().lower() for li in soup.select('div.content li') if len(li.text.strip()) == 5]
    
    word_counter = Counter()
    for word in word_list:
        for letter in set(word):
            word_counter[letter] += 1

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