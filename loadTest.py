import tensorflow as tf


reload = tf.keras.models.load_model("model1")
predictions = reload.predict([10,90])
print(predictions)
