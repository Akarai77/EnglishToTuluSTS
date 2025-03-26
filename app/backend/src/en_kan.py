# from tensorflow.keras.models import load_model
# import numpy as np
# import re
# import os
# import tensorflow as tf
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from unicodedata import normalize
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# en_tokenizer = Tokenizer()
# kn_tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@\\^_`{|}~\t\n')

# try:
#     model = load_model(r'C:\Users\Akarsh\Documents\Documents\Code\MiniProject\models\english_to_kannada_model.h5')
# except Exception:
#     pass

# def clean_text_for_prediction(text):
#     text = normalize('NFD', text.lower())
#     text = re.sub('[^A-Za-z ]+', '', text)
#     return text

# def prepare_input_for_prediction(text, tokenizer, max_len):
#     text = clean_text_for_prediction(text)
#     seq = tokenizer.texts_to_sequences([text])
#     padded_seq = pad_sequences(seq, maxlen=max_len, padding='post')
#     return padded_seq

# en_input_seq = prepare_input_for_prediction('',en_tokenizer,100)

# kn_input_seq = [kn_tokenizer.word_index['[start]']]

# def decode_sequence(sequence, tokenizer):
#     reverse_index = {index: word for word, index in tokenizer.word_index.items()}
#     decoded_text = ' '.join([reverse_index.get(idx, '') for idx in sequence if idx != 0])
#     return decoded_text
from googletrans import Translator
# def en__kn(en_text):
#     predicted_translation = []

#     while True:
#         decoder_input_seq = np.array(kn_input_seq).reshape(1, -1)
#         prediction = model.predict([en_input_seq, decoder_input_seq])

#         predicted_token = np.argmax(prediction[0, -1, :])

#         if predicted_token == kn_tokenizer.word_index['[end]']:
#             break

#         kn_input_seq.append(predicted_token)

#         predicted_translation.append(predicted_token)

#     translated_sentence = decode_sequence(predicted_translation, kn_tokenizer)

def en_kn(en_text):
    translator = Translator()
    translated = translator.translate(en_text, src='en', dest='kn')
    return translated.text