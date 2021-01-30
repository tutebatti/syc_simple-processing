#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# the following list of tuples can be used 
# to transliterate the Syriac text into Latin characters
# -> needs refinement

substitutions = [
    ("ܐ","ʾ"),
    ("ܒ","b"),
    ("ܓ","g"),
    ("ܕ","d"),
    ("ܗ","h"),
    ("ܘ","w"),
    ("ܙ","z"),
    ("ܚ","H"),
    ("ܛ","T"),
    ("ܝ","y"),
    ("ܟ","k"),
    ("ܠ","l"),
    ("ܡ","m"),
    ("ܢ","n"),
    ("ܣ","s"),
    ("ܥ","ʿ"),
    ("ܦ","f"),
    ("ܨ","S"),
    ("ܩ","q"),
    ("ܪ","r"),
    ("ܫ","$"),
    ("ܬ","t"),
    ("ܲ","a"),
    ("ܵ","A"),
    ("ܸ","e"),
    ("ܼ","i"),
    ("ܿ","o"),
    ("ܹ","E"),
    ("̈","~"),
    ]

# the following list of strings can be used 
# to identify possible instances of words with affixed particles
# -> needs refinement

particles = [
    'ܒ',
    'ܒܕ',
    'ܒܕܒ',
    'ܒܕܒܕ',
    'ܒܕܠ',
    'ܒܕܠܕ',
    'ܒܠܒܕ',
    'ܒܠܕܒ',
    'ܕ',
    'ܕܒ',
    'ܕܒܕ',
    'ܕܒܕܒ',
    'ܕܒܕܠ',
    'ܕܒܠܕ',
    'ܕܠ',
    'ܕܠܒܕ',
    'ܕܠܕ',
    'ܕܠܕܒ',
    'ܕܠܕܠ',
    'ܘ',
    'ܘܒ',
    'ܘܒܕ',
    'ܘܒܕܒ',
    'ܘܒܕܠ',
    'ܘܒܠܕ',
    'ܘܕ',
    'ܘܕܒ',
    'ܘܕܒܕ',
    'ܘܕܠ',
    'ܘܕܠܕ',
    'ܘܠ',
    'ܘܠܒܕ',
    'ܘܠܕ',
    'ܘܠܕܒ',
    'ܘܠܕܠ',
    'ܠ',
    'ܠܒܕ',
    'ܠܒܕܠ',
    'ܠܕ',
    'ܠܕܒ',
    'ܠܕܒܕ',
    'ܠܕܠ',
    'ܠܕܠܕ'
    ]

def export_to_file(file, dct):
    """
    Simple function to export dct, preferably to a csv file
    """
    with open(file, "w", encoding="utf8") as current_file:
        for (key, value) in dct.items():
            current_file.write(f"{key},{value}\n")

class Text:
    """
    Basic class to handle text
    """
    def __init__(self, file):
        with open(file, "r", encoding="utf8") as current_file:
            self.imported_text = current_file.read()

    def remove_linebreaks(self, text = None):
        """
        Remove linebreaks (both \n and \r)
        """
        if text == None:
            text = self.imported_text
        self.text_no_linebreaks = text.replace("\n", " ")
        self.text_no_linebreaks = self.text_no_linebreaks.replace("\r", " ")
        self.text_no_linebreaks = self.text_no_linebreaks.replace("  ", " ")

    def remove_punctuation(self, text = None, punctuation_chars = [".", ",", ":", "܆", "܇", "܀"]):
        """
        Remove punctuation from text
        """
        if text == None:
            text = self.text_no_linebreaks
        self.text_no_punctuation = text
        for char in punctuation_chars:
            self.text_no_punctuation = self.text_no_punctuation.replace(char, "")

    def process(self):
        """
        Simple processing:
        remove linebreaks and punctuation with one command
        """
        self.remove_linebreaks()
        self.remove_punctuation()
        self.text = self.text_no_punctuation

    def convert_to_latin(self, text = None):
        """
        Convertion of Syriac characters to Latin ones,
        depends on list of tuples »substitutions« above
        """
        if text == None:
            text = self.text
        self.text_latin = text
        for sub in substitutions:
            self.text_latin = self.text_latin.replace(sub[0],sub[1])

    def export_to_file(self, file, text = None):
        """
        Exports current state of text to file
        """
        if text == None:
            text = self.text
        with open(file, "w", encoding="utf8") as current_file:
            current_file.write(f"{text}")

class CharList:
    """
    Creates list of unique characters in text;
    used for checking consistency
    """
    def __init__(self, text):
        self.char_list = {}
        for char in text:
            if char in self.char_list:
                self.char_list[char] += 1
            else:
                self.char_list[char] = 1
            self.char_list.pop("", None)

class WordList:
    """
    Creates list of unique words in text,
    words are stored in dict, together with frequency
    """
    def __init__(self, text):
        self.word_list = {}
        for word in text.split(" "):
            if word in self.word_list:
                self.word_list[word] += 1
            else:
                self.word_list[word] = 1
            self.word_list.pop("", None)

    def sort_list(self, order):
        """
        Sorts word list either alphabetically or by occurence
        """
        valid_order = ["alefba", "freq"]
        if order not in valid_order:
            raise ValueError(f"argument »order« must be one of {valid_order}.")
        if order == "alefba":
            self.word_list = dict(sorted(self.word_list.items(), key=lambda item: item[0]))
        else:
            self.word_list = dict(sorted(self.word_list.items(), key=lambda item: item[1], reverse=True))

    def search_by_length(self, length, word_list = None):
        """
        Searches words with certain length
        
        Attention: vowels and other diacritic signs are counted as well!
        """
        if word_list == None:
            word_list = self.word_list
        for word in self.word_list.keys():
            if len(word) == length:
                print(word)

    def search_by_pattern(self, pattern, word_list = None):
        """
        Searches words contain certain pattern/string
        
        Attention: vowels and other diacritic signs are to be considered!
        """
        if word_list == None:
            word_list = self.word_list
        for word in self.word_list.keys():
            if pattern in word:
                print(word)

    def filter_vocalized(self, vowels = ["ܲ", "ܵ", "ܸ", "ܼ", "ܿ", "ܹ"], word_list = None):
        """
        Creates a dict each for words with and without vowel signs;
        at the moment, only Eastern vowels are considered
        """
        if word_list == None:
            word_list = self.word_list
        self.vocalized = {}
        self.unvocalized = {}
        for (word, freq) in self.word_list.items():
            if any(vowel in word for vowel in vowels):
                self.vocalized[word] = freq
            else:
                self.unvocalized[word] = freq

    def filter_syame(self, word_list = None):
        """
        Creates a dict for words with syame, i.e. Syriac markers for plural
        """
        if word_list == None:
            word_list = self.word_list
        self.syame = {}
        for (word, freq) in self.word_list.items():
            if "̈" in word:
                self.syame[word] = freq

    def filter_possible_particles(self, word_list = None):
        """
        Creates a dict with possible instances of words with affixed particles,
        each particle from »particles« above is a dict entry,
            with the respective matching words as values;
        at the moment, one should only export the values of one particle to csv
        """
        if word_list == None:
            word_list = self.word_list
        self.possibly_with_particles = {}
        for particle in particles:
            words_starting_with_x = {}
            for (word, freq) in self.word_list.items():
                if word.startswith(particle):
                    words_starting_with_x[word] = freq
            self.possibly_with_particles[particle] = words_starting_with_x