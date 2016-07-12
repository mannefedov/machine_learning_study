import os
from collections import Counter
import string
from math import log

class Chdir():
    """ Контекст менеджер, который меняет
        рабочую директорию на переданную,
        а потом возвращает все на место.
        Написан, чтобы поиграться с контекст-менеджерами.
        :param: path
                Нужный путь.
    """

    def __init__(self, path):
        self.old = os.getcwd()
        self.new = path

    def __enter__(self):
        os.chdir(self.new)

    
    def __exit__(self, exception_type, exception_value, traceback):
        os.chdir(self.old)


def count(text):
    text = [x for x in text.lower().split() if len(x) <= 4 and x.isalpha() and len(x) >= 2]
    c = Counter(text)
    return c.most_common(1)[0][0]


def count_letter(text):
    text = text.lower().split()
    text = [x.strip() for x in text if x.isalpha()]
    c = Counter()
    for word in text:
        a = Counter(word)
        c += a
    return c.most_common(1)[0][0]

def count_upper(text):
    text = text.split()
    c = 0
    for x in text:
        if x != x.lower() and not x.isupper():
            c += 1
    return round(c/len(text), 2)

def average_doubles(text):
    a = text[0].lower()

    c = 0
    for x in text[1:]:
        if x.lower() == a and x.lower() in ['e', 'a']:
            c += 1
            a = x
        else:
            a = x
    return round(log(c/len(text)), 2) if c > 2 else 0


def contains_apostrof(text):
    c = 0
    for x in text:
        if x is "'":
            c += 1
    if c > 1:
        return 1
    else:
        return 0

def zed(text):
    text = text.split()
    for x in text:
        if x[0].lower() == 'z':
            return 1
    return 0

def lh(text):
    c = 0
    for i in range(len(text)-1):
        if text[i:i+2].lower() == 'lh':
            c += 1
    return round(c/len(text.split()), 2)
def contains_i(text):
    c = 0
    for x in text:
        if x.lower() == 'і':
            c += 1

    return round(c/len(text.split()), 2)

def contains_single_y(text):
    text = text.split()
    c = 0
    for x in text:
        if x.lower() == 'y':
            c += 1
    if c > 3:
        return 1
    else:
        return 0


def count_letters(text, n=2):
    text = text.lower()
    c = Counter()
    for i in range(len(text)-n+1):
        for x in string.punctuation:
            if x in text[i:i+n]:
                continue
        if ' ' in text[i:i+n]:
            continue
        a = Counter([text[i:i+n]])
        c += a
    return c.most_common(1)[0][0]


def count_uniq(text):
    text = text.lower().split()
    text = [x.strip() for x in text if x.isalpha()]
    c = Counter()
    for word in text:
        for letter in word:
            c.update(letter)
    c = [x for x in c.most_common() if x[1] > 3]
    return len(c)

def average_len(text):
    
    text = text.split()
    text = [x.strip() for x in text if x.isalpha()]
    x = sum([len(word) for word in text])
    return round((x/len(text))**3, 2)

def punct(text):
    text = text.lower()
    c = 0
    for x in text:
        if x in string.punctuation:
            c += 1
    return round(-log(c/len(text)), 2) if c > 0 else 0


def main():
    with open('result.csv', 'a', encoding='utf-8') as data:
        data.write('language,top_word,top_letter,top_letters,top_l,punct,average_len,num_of_uniq,upper,apost,y, doubles,lh,i,z\n')
    languages = ['en', 'ru', 'cz', 'uk',
                  'vi', 'pl', 'bg', 'de',
                  'es', 'fi', 'nl', 'sv',
                  'fr', 'pt']
    text_r = None
    files = None
    for language in languages:
        with Chdir('lang_recognition\\' + language) as directory:
            files = os.listdir(directory)
            for fil in files:
                text_r = open(fil, encoding='utf-8').read()
                with open('C:\\Users\\ывап\\Desktop\\учеба\\комп линг\\CL_proj1\\result.csv', 'a', encoding='utf-8') as data:
                    top_word = count(text_r)
                    top_letter = count_letter(text_r)
                    top_letters = count_letters(text_r)
                    top_l = count_letters(text_r, n=3)
                    average = average_len(text_r)
                    punctu = punct(text_r)
                    num_uniq = count_uniq(text_r)
                    upper = count_upper(text_r)
                    apost = contains_apostrof(text_r)
                    y = contains_single_y(text_r)
                    doubles = average_doubles(text_r)
                    is_lh = lh(text_r)
                    i = contains_i(text_r)
                    z = zed(text_r)
                    data.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                                language, top_word, top_letter, top_letters, top_l,
                                punctu, average, num_uniq, upper, apost,
                                y, doubles, is_lh, i, z
                                ))


if __name__ == '__main__':
    main()
