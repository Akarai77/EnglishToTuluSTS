# train_model.py

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, TimeDistributed
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
import pickle

# Load dataset from Excel and get the first 100 rows
data = pd.read_excel(r"C:\Users\Akarsh\Downloads\kn_tcy.xlsx")  # Ensure your Excel file has 'Kannada' and 'Tulu' columns

# Preprocess data (split into source and target sentences)
source_sentences = data['Kannada'].astype(str).values  # Ensure all entries are strings
target_sentences = data['Tulu'].astype(str).values  # Ensure all entries are strings

# Add a start token and end token to target sentences
target_sentences_input = ['\t' + sentence for sentence in target_sentences]  # Adding start token
target_sentences_output = [sentence + '\n' for sentence in target_sentences]  # Adding end token

# Initialize tokenizers
source_tokenizer = Tokenizer(char_level=False)
target_tokenizer = Tokenizer(char_level=False)

# Add start token to the target tokenizer manually before fitting
# Manually add the start token '\t' in the word_index to ensure it's indexed correctly
target_tokenizer.fit_on_texts(target_sentences_input)  # Fit on sentences with '\t' already added

# Ensure the start token ('\t') is included in the target tokenizer
start_token_index = target_tokenizer.word_index.get('\t')
if start_token_index is None:
    # If the start token is not found, manually add it to the word index
    target_tokenizer.word_index['\t'] = len(target_tokenizer.word_index) + 1
    start_token_index = target_tokenizer.word_index['\t']
    print(f"Start token ('\\t') manually added with index {start_token_index}")

# Tokenize Kannada (source) and Tulu (target) sentences
source_tokenizer.fit_on_texts(source_sentences)

# Create vocab size
source_vocab_size = len(source_tokenizer.word_index) + 1
target_vocab_size = len(target_tokenizer.word_index) + 1

# Convert sentences to sequences of integers
source_sequences = source_tokenizer.texts_to_sequences(source_sentences)
target_sequences_input = target_tokenizer.texts_to_sequences(target_sentences_input)
target_sequences_output = target_tokenizer.texts_to_sequences(target_sentences_output)

# Pad sequences to ensure uniform length
max_source_len = max([len(seq) for seq in source_sequences])
max_target_len = max([len(seq) for seq in target_sequences_input])

source_sequences = pad_sequences(source_sequences, maxlen=max_source_len, padding='post')
target_sequences_input = pad_sequences(target_sequences_input, maxlen=max_target_len, padding='post')
target_sequences_output = pad_sequences(target_sequences_output, maxlen=max_target_len, padding='post')

# Split data into training and validation sets (80/20 split)
train_size = int(0.8 * len(source_sentences))
X_train = source_sequences[:train_size]
y_train_input = target_sequences_input[:train_size]
y_train_output = target_sequences_output[:train_size]

X_val = source_sequences[train_size:]
y_val_input = target_sequences_input[train_size:]
y_val_output = target_sequences_output[train_size:]

# Build the Seq2Seq Model

# Encoder
encoder_inputs = Input(shape=(max_source_len,))
encoder_embedding = Embedding(source_vocab_size, 256)(encoder_inputs)
encoder_lstm = LSTM(512, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)

# Decoder
decoder_inputs = Input(shape=(max_target_len,))
decoder_embedding = Embedding(target_vocab_size, 256)(decoder_inputs)
decoder_lstm = LSTM(512, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=[state_h, state_c])

# Output layer
decoder_dense = TimeDistributed(Dense(target_vocab_size, activation='softmax'))
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile the model
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(
    [X_train, y_train_input], np.expand_dims(y_train_output, -1),
    epochs=10,
    batch_size=64,
    validation_data=([X_val, y_val_input], np.expand_dims(y_val_output, -1))
)

# Save the trained model
model.save('kannada_to_tulu_model.h5')

# Save the tokenizers to reuse in the prediction script
with open('source_tokenizer.pkl', 'wb') as f:
    pickle.dump(source_tokenizer, f)

with open('target_tokenizer.pkl', 'wb') as f:
    pickle.dump(target_tokenizer, f)

print("Model training complete and saved.")
