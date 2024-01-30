import pickle
import numpy as np
import tensorflow as tf 
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense
import random
import os
from keras.models import Sequential, load_model
from discours import Discours

# Check for GPU devices
def check_GPU():
    tf.compat.v1.enable_eager_execution(tf.compat.v1.ConfigProto(log_device_placement=True)) 
    gpu_devices = tf.config.experimental.list_physical_devices('GPU')

    if gpu_devices:
        print("Un GPU est disponible")
        for device in gpu_devices:
            print(f"Device name: {device.name}")
    else:
        print("Aucun GPU trouvé, utilisation du CPU.")


if __name__ == "__main__":
    check_GPU()
    nom = "test"
    sentences = Discours().take_discours_from_users(message_lim=15000)
    sentences = random.sample(sentences, 15000)

    tokenizer = Tokenizer(filters='')
    tokenizer.fit_on_texts(sentences)
    total_mots = len(tokenizer.word_index) + 1

    if not os.path.exists(f"PICS/pik_{nom}.h5"):

        # Génère des séquences de mots
        sequences = []
        for ligne in sentences:
            token_list = tokenizer.texts_to_sequences([ligne])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                sequences.append(n_gram_sequence)

        # Pad les séquences pour qu'elles aient la même longueur
        max_sequence_length = max([len(seq) for seq in sequences])
        sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='pre')

        # Divisez les séquences en données d'entraînement (X) et étiquettes (y)
        X = sequences[:, :-1]
        y = sequences[:, -1]

        # Convertissez les étiquettes en format one-hot
        y = tf.keras.utils.to_categorical(y, num_classes=total_mots)

        # Créez un modèle LSTM simple
        model = Sequential()
        model.add(Embedding(total_mots, 15, input_length=max_sequence_length-1))
        model.add(LSTM(256, dropout=0.1, recurrent_dropout=0.2))
        model.add(Dense(total_mots, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.fit(X, y, epochs=100, verbose=1, validation_split=0.2)
        model.summary()
        # Sauvegarde du model
        model.save(f"PICS/pik_{nom}.h5")
    else:
        model = load_model(f"PICS/pik_{nom}.h5")

    # Fonction pour générer du texte
    def generate_text(seed_text, next_words, model, max_sequence_length, tokenizer):
        for _ in range(next_words):
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
            predicted_probabilities = model.predict(token_list, verbose=0)
            predicted_index = np.argmax(predicted_probabilities)
            output_word = ""
            for word, index in tokenizer.word_index.items():
                if index == predicted_index:
                    output_word = word
                    break
            seed_text += " " + output_word
            if output_word == ".":
                break
        return seed_text

    # Génère du texte à partir d'une phrase d'amorçage
    cond = True

    while cond:
        seed_text = input("Votre phrase : ")
        if seed_text == "kill":
            cond = False
        generated_text = generate_text(seed_text, np.random.randint(5,150), model, max_sequence_length,tokenizer)

        print(f"\n\033[3m{generated_text.replace(seed_text,'').replace('Réponse :','')}\033[0m\n")