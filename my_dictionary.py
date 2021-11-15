import os
import sys
import re
from pystardict import Dictionary


dicts_dir = os.path.join(os.path.dirname(__file__))
dicts_dir = os.path.join(dicts_dir, 'stardict')
dict1 = Dictionary(os.path.join(dicts_dir, 'stardict-quick_eng-rus-2.4.2',
    'quick_english-russian'))
#dict2 = Dictionary(os.path.join(dicts_dir, 'stardict-quick_rus-eng-2.4.2',
#    'quick_russian-english'))


def translate_words(in_str: str) :
    """ Возвращает перевод слов из строки """
    in_words = in_str.split()
    out_str = ""
    for word in in_words:
        out_str += word
        out_str += " -- "
        try :
            s = dict1[re.sub(r'[^\w\s]','', word.lower())]
            out_str += s
        except KeyError :
            out_str += "(Нет перевода)"
        out_str += "\n"
    return out_str


#print(translate_words("Please, translate this text for me."))