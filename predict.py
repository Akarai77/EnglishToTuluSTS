import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load the model
model = tf.keras.models.load_model('kannada_to_tulu_model.h5')

# Load the tokenizers
with open('source_tokenizer.pkl', 'rb') as f:
    source_tokenizer = pickle.load(f)

with open('target_tokenizer.pkl', 'rb') as f:
    target_tokenizer = pickle.load(f)

# Define the max source sequence length (this should be the same as in the training script)
max_source_len = 46  # Replace with the actual value you used for max_source_len during training

def predict_translation(input_sentence, model, source_tokenizer, target_tokenizer, max_source_len, max_target_len):
    # Tokenize the input sentence
    input_sequence = source_tokenizer.texts_to_sequences([input_sentence])
    
    # Pad the input sequence to match the max source length
    input_sequence = pad_sequences(input_sequence, maxlen=max_source_len, padding='post')

    # Prepare the initial target sequence with start token
    target_sequence_input = [target_tokenizer.word_index['\t']]  # Start token index
    target_sequence_input = np.array(target_sequence_input).reshape(1, -1)  # Reshaping for batch size of 1

    # Predict the sequence
    prediction = model.predict([input_sequence, target_sequence_input])

    # Convert the prediction to text (decode the prediction back to words)
    predicted_sequence = np.argmax(prediction[0], axis=-1)
    
    # Convert back to words using target tokenizer
    predicted_sentence = ''
    for idx in predicted_sequence:
        word = target_tokenizer.index_word.get(idx)
        if word == '\n':  # End token
            break
        if word:
            predicted_sentence += ' ' + word

    return predicted_sentence.strip()

# Example usage
input_sentence = "hello"
from en_kn import translate  # Ensure this is correctly imported
translated_sentence = translate(input_sentence)  # Translate the sentence
print(translated_sentence)
predicted_translation = predict_translation(translated_sentence, model, source_tokenizer, target_tokenizer, max_source_len, 50)
print(predicted_translation)
