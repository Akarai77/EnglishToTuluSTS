from difflib import get_close_matches
import re
import pandas as pd

def remove_punctuation(word):
    return re.sub(r'[^\w\s]', '', word)

def translate_word(kn_word, source_col, target_col, df):
    matches = get_close_matches(kn_word, df[source_col], n=1, cutoff=0.6)
    
    if matches:
        index = df[df[source_col] == matches[0]].index[0]
        return df.loc[index, target_col]
    else:
        return kn_word

def kn_tcy(kn_text, df):
    kn_words = kn_text.split(' ')
    tcy_text = ''
    
    for kn_word in kn_words:
        kn_word = remove_punctuation(kn_word)
        translated_word = translate_word(kn_word, "Kannada", "Tulu", df)
        tcy_text += translated_word + ' '
    return tcy_text.strip()