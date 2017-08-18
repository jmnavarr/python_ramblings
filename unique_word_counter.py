"""
   Author: Juan M Navarro
   Date: 8/16/2017
   Notes: 
      --- From an input paragraph, return a json object with an alphabetized list of words, including how many times each word occurs, and the sentence number where it appears in.
      --- Run unit tests with this command: python -m unittest -v unique_word_counter
      --- Dependencies:
              --- sudo pip install pydictionary   # used to filter out words with similar meaning
"""

import re
import unittest
import json
import sys, os
from sets import Set
from collections import OrderedDict
from PyDictionary import PyDictionary

words_to_exclude = ["a", "the", "and", "of", "in", "be", "also", "as"]

dictionary = PyDictionary()
synonyms = Set()

class UniqueWordCounterTestCases(unittest.TestCase):
   def test_case_1(self):
      test_string = "One. Two. Two. Three."
      result = parse_input_text(test_string)
      expected = OrderedDict({ 
                    'Three': { 'count': 1, 'sentences': [3] }, 
                    'Two': { 'count': 2, 'sentences': [1,2] }, 
                    'One': { 'count': 1, 'sentences': [0] }, 
                 })
      self.assertEqual(result, expected)
   def test_case_2(self):
      test_string = "Here is the first sentence. Here is the second sentence. The third sentence goes here."
      result = parse_input_text(test_string)
      expected = OrderedDict({
                    "first": {"count": 1, "sentences": [0]}, 
                    "goes": {"count": 1, "sentences": [2]}, 
                    "Here": {"count": 2, "sentences": [0, 1]}, 
                    "here": {"count": 1, "sentences": [2]}, 
                    "is": {"count": 2, "sentences": [0, 1]}, 
                    "second": {"count": 1, "sentences": [1]}, 
                    "sentence": {"count": 3, "sentences": [0, 1, 2]}, 
                    "the": {"count": 2, "sentences": [0, 1]}, 
                    "The": {"count": 1, "sentences": [2]}, 
                    "third": {"count": 1, "sentences": [2]}
                 })

# disable
def block_print():
    sys.stdout = open(os.devnull, 'w')

# restore
def enable_print():
    sys.stdout = sys.__stdout__

# https://stackoverflow.com/questions/13249415/can-i-implement-custom-indentation-for-pretty-printing-in-python-s-json-module
def collapse_json(text, indent=12):
    """Compacts a string of json data by collapsing whitespace after the
    specified indent level

    NOTE: will not produce correct results when indent level is not a multiple
    of the json indent level
    """
    initial = " " * indent
    out = []  # final json output
    sublevel = []  # accumulation list for sublevel entries
    pending = None  # holder for consecutive entries at exact indent level
    for line in text.splitlines():
        if line.startswith(initial):
            if line[indent] == " ":
                # found a line indented further than the indent level, so add
                # it to the sublevel list
                if pending:
                    # the first item in the sublevel will be the pending item
                    # that was the previous line in the json
                    sublevel.append(pending)
                    pending = None
                item = line.strip()
                sublevel.append(item)
                if item.endswith(","):
                    sublevel.append(" ")
            elif sublevel:
                # found a line at the exact indent level *and* we have sublevel
                # items. This means the sublevel items have come to an end
                sublevel.append(line.strip())
                out.append("".join(sublevel))
                sublevel = []
            else:
                # found a line at the exact indent level but no items indented
                # further, so possibly start a new sub-level
                if pending:
                    # if there is already a pending item, it means that
                    # consecutive entries in the json had the exact same
                    # indentation and that last pending item was not the start
                    # of a new sublevel.
                    out.append(pending)
                pending = line.rstrip()
        else:
            if pending:
                # it's possible that an item will be pending but not added to
                # the output yet, so make sure it's not forgotten.
                out.append(pending)
                pending = None
            if sublevel:
                out.append("".join(sublevel))
            out.append(line)
    return "\n".join(out)

# parse the input text and return a dictionary of alphabetized words with counts for each word and sentence numbers where word was found
def parse_input_text(input_text):
   result = {}
   global synonyms # we assign to it in this function, so mark it as global
   sentences = input_text.split('.')

   for s, sentence in enumerate(sentences):
      words = sentence.split(' ')
      words = filter(None, words) # remove empty spaces   

      for word in words:
         word = re.sub('^[^a-zA-z]*|[^a-zA-Z]*$', '', word) # remove grammar from beginning or end of word

         # filter out words to exclude, or words with a similar meaning
         if word.lower() in words_to_exclude or word in synonyms:
            continue

         # get synonyms for word, and add it to our list of synonyms
         block_print()
         word_synonyms = Set(dictionary.synonym(word))
         enable_print()
         synonyms = synonyms.union(word_synonyms)

         if word in result:
            result[word]['count'] += 1
            if not s in result[word]['sentences']:
               result[word]['sentences'].append(s)
         else:
            result[word] = { 'count': 1, 'sentences': [s] } 

   # sort dictionary alphabetically, ignoring case
   result = OrderedDict(sorted(result.items(), key=lambda t: t[0].lower()))
   return result

# match the output format of the sample document
def convert_dict_format(dict_to_format):
   result = []

   for k, v in dict_to_format.items():
      word_dict = {
         "word": k,
         "total-occurrences": v['count'],
         "sentence-indexes": v['sentences']
      } 

      # sort in reverse alphabetical order
      word_dict = OrderedDict(sorted(word_dict.items(), key=lambda t: t[0].lower(), reverse=True))
      result.append(word_dict)

   return result

if __name__ == '__main__':
   test_string = "Here is the first sentence. Here is the second sentence. The third sentence goes here."

   result = parse_input_text(test_string) 
   result = convert_dict_format(result)

   json_result = json.dumps({ 'results': result }, indent=2, separators=(',', ': '))
   json_result = collapse_json(json_result, indent=6)
   print json_result  



 
