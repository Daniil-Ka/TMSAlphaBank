from keras.src.layers import TextVectorization
import tensorflow as tf

model = tf.keras.models.load_model('my_model')

# Load the TextVectorization layer
vectorizer = TextVectorization.from_config(model.get_layer('text_vectorization').get_config())
vectorizer.set_weights(model.get_layer('text_vectorization').get_weights())

# Function to translate sentences
def translate_sentence(sentence, model, vectorizer):
    sequence = vectorizer([sentence]).numpy()
    predicted_sequence = model.predict(sequence)
    predicted_sentence = ' '.join([vectorizer.get_vocabulary()[i] for i in np.argmax(predicted_sequence, axis=2)[0]])
    return predicted_sentence

# Example usage
input_sentence = input("Enter a sentence in nominative case: ")
output_sentence = translate_sentence(input_sentence, model, vectorizer)
print("Translated sentence in another case:", output_sentence)