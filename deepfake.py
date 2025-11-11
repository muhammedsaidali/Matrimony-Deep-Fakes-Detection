
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from joblib import dump
from joblib import load
# Function to extract features using pre-trained VGG16 model
def extract_features(image_paths, model):
    features = []
    for path in image_paths:
        image = load_img(path, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        feature = model.predict(image)
        features.append(feature.flatten())
    return np.array(features)

# Function to load dataset and preprocess images
def load_dataset(dataset_dir):
    image_paths = []
    labels = []
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(root, file)
                image_paths.append(image_path)
                if "real" in root:
                    labels.append(0)  # Real face image
                else:
                    labels.append(1)  # Deepfake face image
    return image_paths, labels

# Load pre-trained VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Load dataset
dataset_dir = "Dataset/Train/pgm"
image_paths, labels = load_dataset(dataset_dir)

# Extract features
features = extract_features(image_paths, base_model)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=5)

# Train SVM classifier
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Assuming svm_model is your trained SVM model
model_filename = "svm_model.joblib"
dump(svm_model, model_filename)
print("Model saved as", model_filename)
# Evaluate the model


loaded_model = load("svm_model.joblib")
y_pred = loaded_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Function to detect deepfake face images
def detect_deepfake(image_path, model, base_model):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    feature = base_model.predict(image).flatten()
    prediction = model.predict(feature.reshape(1, -1))
    if prediction == 0:
        return "Real"
    else:
        return "Deepfake"

# Example usage:
prediction = detect_deepfake("real_49.jpg", loaded_model, base_model)
print("Prediction:", prediction)
