
import tensorflow as tf
from tensorflow.keras.applications.xception import Xception, preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths to your dataset
train_dir = 'Dataset/train/'
validation_dir = 'Dataset/validation/'

# Initialize the base model
base_model = Xception(weights='imagenet', include_top=False, input_shape=(299, 299, 3))

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(2, activation='softmax')(x)  # Assuming 2 classes: real and fake

model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base_model
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Data augmentation and input preparation
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

# Data generators
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical')

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size)


test_dir = 'Dataset/test/'

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical')

# Evaluate the model on the test data
scores = model.evaluate(test_generator, steps=test_generator.samples // test_generator.batch_size)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
# Evaluate the model on the test data


from tensorflow.keras.preprocessing import image
import numpy as np

def predict_image(image_path):
    img = image.load_img(image_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(img_array_expanded_dims)

    prediction = model.predict(img_preprocessed)
    return prediction

# Example usage
image_path = 'real_49.jpg'
prediction = predict_image(image_path)
print('Prediction:', prediction)

base_model.trainable = True

# It's important to recompile the model after you make any changes to the `trainable` attribute of any layer
model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=1e-5),  # Very low learning rate
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Continue training
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=5,  # Train for more epochs if necessary
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size)