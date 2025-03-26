import pandas as pd
from googletrans import Translator #pip install googletrans==4.0.0-rc1
from difflib import get_close_matches
import re

data = pd.read_excel(r"C:\Users\Akarsh\Documents\Documents\Code\MiniProject\app\backend\src\data\kn_tcy.xlsx", engine='openpyxl')

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def simple_translate(word, source_col, target_col, df):
    result = df.loc[df[source_col] == word, target_col]
    
    if not result.empty:
        return result.iloc[0]
    else:
        return -1


def translate_to_kannada(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='kn')
    return translated.text

english_text = []
with open(r'C:\Users\Akarsh\Documents\Documents\Code\MiniProject\app\backend\utils\1.txt', 'r', encoding='utf-8') as en:
    english_text = en.read().split('\n')

for i, en_text in enumerate(english_text, start=1):
    print(f"{i}/{len(english_text)}")
    en_text = remove_punctuation(en_text)
    kn_text = translate_to_kannada(en_text)
    kn_list = kn_text.split(' ')
    for kn_word in kn_list:
        translation = simple_translate(kn_word, source_col="Kannada", target_col="Tulu", df=data)
        if translation != -1:
            print(f"Translation : {kn_word} : {translation}")
        else:
            translation = input(f"Translation Not Found for : {en_text} : {kn_word}! Enter translation: ")
            file_path = r'C:\Users\Akarsh\Documents\Documents\Code\MiniProject\app\backend\src\data\kn_tcy.xlsx'
            
            data_to_append = {
                'Kannada': [kn_word],
                'Tulu': [translation]
            }
            
            df_new = pd.DataFrame(data_to_append)
            try:
                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    df_new.to_excel(writer, sheet_name='Translations', index=False, header=False, startrow=writer.sheets['Translations'].max_row)
            except FileNotFoundError:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df_new.to_excel(writer, sheet_name='Translations', index=False)
