import pickle
from typing import Optional

import numpy as np
import tensorflow as tf
from keras.src.layers import TextVectorization


class Model:
    def __init__(self):
        self.vectorizer: Optional[TextVectorization] = None
        self.model = None


    def load(self):
        cfg = pickle.load(open("vectorizer.pkl", "rb"))
        self.vectorizer = TextVectorization.from_config(cfg['config'])
        self.vectorizer.set_weights(cfg['weights'])

        self.model = tf.keras.models.load_model('my_model.keras')
        pass


    def translate_sentence(self, sentence):
        if not self.model:
            raise ValueError('Модель не загружена')

        sequence = self.vectorizer([sentence]).numpy()
        predicted_sequence = self.model.predict(sequence)
        predicted_sentence = ' '.join(
            [self.vectorizer.get_vocabulary()[i] for i in np.argmax(predicted_sequence, axis=2)[0]]
        )
        return predicted_sentence
