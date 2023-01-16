import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import sys

def build_and_compile_model(norm):
    model = tf.keras.Sequential([
        norm,
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
    return model

def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 1])
    plt.xlabel('Epoch')
    plt.ylabel('Error [Speed]')
    plt.legend()
    plt.grid(True)
    plt.show()


conn = psycopg2.connect(database = "intproject", 
                        host = "localhost",
                        user = "intproject",
                        password = "project1234")
cursor = conn.cursor()


cursor.execute("SELECT * FROM boatdata WHERE name='Stormfuglen'")
data_all = np.array(cursor.fetchall())


data = data_all[:,3:]

np.random.shuffle(data)

relative_wind = data[:,1] - ((data[:,2]+180) % 360)

data_input = np.array([data[:,0],relative_wind,data[:,3]]).T
data_input = np.asarray(data_input).astype('float32')
train_data = data_input[:int(np.round(0.9*len(data_input))),:]
test_data = data_input[int(np.round(0.9*len(data_input))):,:]



normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(train_data[:,0:2])

dnn_model = build_and_compile_model(normalizer)
#dnn_model.summary()


history = dnn_model.fit(train_data[:,0:2],train_data[:,2],validation_split=0.2,verbose=0,epochs=100)


plot_loss(history)



dnn_model.save("model1")





conn.close()