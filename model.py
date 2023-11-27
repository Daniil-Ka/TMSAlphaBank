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

        self.model = tf.keras.models.load_model('my_model.h5')


    def translate_sentence(self, sentence):
        if not self.model:
            raise ValueError('Модель не загружена')

        sequence = self.vectorizer([sentence]).numpy()
        predicted_sequence = self.model.predict(sequence)
        predicted_sentence = ' '.join(
            [self.vectorizer.get_vocabulary()[i] for i in np.argmax(predicted_sequence, axis=2)[0]]
        )
        return predicted_sentence


if __name__ == "__main__":
    m = Model()
    m.load()
    sentences = [
        ["Вагайский городской суд города нижний новгород", "Вагайским городским судом города нижний новгород"],
        ["Бутурлинский межрайонный суд г. екатеринбурга свердловской области","Бутурлинским межрайонным судом г. екатеринбурга свердловской области"],
        ["Армавирский городской суд г.новая ляля","Армавирским городским судом г.новая ляля"],
        ["Азнакаевский городской суд республики саха","Азнакаевским городским судом республики саха"],
        ["Беловский межрайонный суд волгоградской области","Беловским межрайонным судом волгоградской области"]
    ]

    for sent in sentences:
        translated = m.translate_sentence(sent[0])
        print("Оригинал: ", sent[0])
        print("Требуемое: ", sent[1])
        print("Перевод: ", translated)
        print()