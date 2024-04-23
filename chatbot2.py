import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define your conversational data as a single list of strings
conversations = [
    "Hello",
    "Hi there!",
    "How are you?",
    "I'm doing well, thanks.",
    "What's your name?",
    "I'm a chatbot."
    # Add more conversational pairs as needed
]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(conversations)

vocab_size = len(tokenizer.word_index) + 1

sequences = tokenizer.texts_to_sequences(conversations)
max_sequence_len = max([len(seq) for seq in sequences])

# Pad sequences separately for input and output
X = pad_sequences(sequences, maxlen=max_sequence_len, padding='post')
y = pad_sequences(sequences[1:], maxlen=max_sequence_len, padding='post')  # Use sequences starting from the second one

# Optionally, you might want to remove the last element from y if it's a padding token
# y = y[:, :-1]

print("X shape:", X.shape)
print("y shape:", y.shape)

model = Sequential([
    Embedding(vocab_size, 64, input_length=max_sequence_len, mask_zero=True),
    LSTM(100, return_sequences=True),
    Dense(vocab_size, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
