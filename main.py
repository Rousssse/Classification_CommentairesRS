import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pandas as pd
import tensorflow as tf 
from train_model import train_model, save_model, initialize_vectorizer
from test_model import test_model


if not os.path.exists('trained_model.h5'):
    # Entraînement du modèle
    trained_model = train_model()
    save_model(trained_model)

# Test avec un nouveau texte
proposition = 'i will kill u'
vectorizer = initialize_vectorizer()
input_text = vectorizer([proposition]).numpy()
prediction = test_model(input_text)
print(f"Prediction pour '{proposition}': {prediction}")
