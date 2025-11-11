from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2)  # Using 20% of data for validation

train_generator = train_datagen.flow_from_directory(
    directory='Dataset/train',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',  # for binary classification
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    directory='Dataset/train',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',  # for binary classification
    subset='validation')


from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
base_model.trainable = False  # Freeze the base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# history = model.fit(
#     train_generator,
#     steps_per_epoch=train_generator.samples // train_generator.batch_size,
#     validation_data=validation_generator,
#     validation_steps=validation_generator.samples // validation_generator.batch_size,
#     epochs=10)


import numpy as np
from tensorflow.keras.preprocessing import image

def predict_fake(image_path):
    img = image.load_img(image_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    img_preprocessed = img_array_expanded_dims / 255.
    
    prediction = model.predict(img_preprocessed)
    return "Fake" if prediction[0] > 0.5 else "Real"

# Example
# print(predict_fake('ttt.jpg'))
