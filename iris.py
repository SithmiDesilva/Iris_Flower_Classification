from flask import Flask, render_template, request
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle

app = Flask(__name__)

# Load the Iris dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
column_names = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
iris_data = pd.read_csv(url, names=column_names)

# Prepare the data
x = iris_data.drop("class", axis=1)
y = iris_data["class"]

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# Train the KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train, y_train)

# Save the trained model using pickle
with open("knn_model.pkl", "wb") as model_file:
    pickle.dump(knn, model_file)

# Load the model from the pickle file
def load_model():
    with open("knn_model.pkl", "rb") as model_file:
        return pickle.load(model_file)

knn_model = load_model()

@app.route('/')
def home():
    return render_template('Iris.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the form
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    # Create a DataFrame for the input values
    new_data = pd.DataFrame({
        "sepal_length": [sepal_length],
        "sepal_width": [sepal_width],
        "petal_length": [petal_length],
        "petal_width": [petal_width]
    })

    # Make a prediction using the loaded model
    prediction = knn_model.predict(new_data)
    predicted_class = prediction[0]

    return render_template('Iris.html', prediction_text=f'Predicted Iris Class: {predicted_class}')

if __name__ == '__main__':
    app.run(debug=True)
