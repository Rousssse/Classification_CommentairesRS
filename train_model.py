import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
import os
import pandas as pd

MAX_FEATURES = 200000

def initialize_vectorizer():
    vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                                output_sequence_length=1800,
                                output_mode='int')
    return vectorizer

def train_model():
    df = pd.read_csv(
        os.path.join('train.csv', 'train.csv')
    )

    X = df['comment_text']
    y = df[df.columns[2:]].values
    vectorizer = initialize_vectorizer()
    vectorizer.adapt(X.values)
    vectorizer_text = vectorizer(X.values)
    dataset = tf.data.Dataset.from_tensor_slices((vectorizer_text,y))
    dataset = dataset.cache()
    dataset = dataset.shuffle(160000)
    dataset = dataset.batch(16)
    dataset = dataset.prefetch(8)

    train = dataset.take(int(len(dataset)*.7))
    val = dataset.skip(int(len(dataset)*.7)).take(int(len(dataset)*.2))
    test = dataset.skip(int(len(dataset)*.9)).take(int(len(dataset)*.1))

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dropout, Bidirectional, Dense, Embedding

    model = Sequential()
    model.add(Embedding(MAX_FEATURES+1, 32))
    model.add(Bidirectional(LSTM(32,activation='tanh')))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(6, activation='sigmoid'))

    model.compile(loss='BinaryCrossentropy', optimizer='Adam')
    model.summary()
    history = model.fit(train, epochs=1, validation_data=val)
    history.history

    return model,vectorizer

def save_model(model):
    model.save('trained_model.h5')

def load_model():
    return tf.keras.models.load_model('trained_model.h5')
