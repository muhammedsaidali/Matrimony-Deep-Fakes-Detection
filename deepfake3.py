import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model

# Load the base model, without the top layers
base_model = tf.keras.applications.Xception(weights='imagenet', include_top=False, input_shape=(299, 299, 3))

# Freeze the base model
base_model.trainable = False

# Create a new model on top
inputs = tf.keras.Input(shape=(299, 299, 3))
x = preprocess_input(inputs)
x = base_model(x, training=False)
x = GlobalAveragePooling2D()(x)
outputs = Dense(2, activation='softmax')(x)  # Assuming 2 classes: real and fake
model = Model(inputs, outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    'Dataset/train/',
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    'Dataset/train/',  # Same directory as training data
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='validation')

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10
)


test_generator = train_datagen.flow_from_directory(
    'Dataset/Test/',
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical')

# Evaluate the model
model.evaluate(test_generator)

# Use model.predict() to make predictions on new images

