document.getElementById('iris-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Clear previous results
    document.getElementById('result').innerHTML = '';

    // Get form data
    const formData = new FormData(event.target);
    const data = {
        sepal_length: parseFloat(formData.get('sepal_length')),
        sepal_width: parseFloat(formData.get('sepal_width')),
        petal_length: parseFloat(formData.get('petal_length')),
        petal_width: parseFloat(formData.get('petal_width'))
    };

    // Send data to the Flask backend using AJAX
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Display the prediction result
        document.getElementById('result').innerHTML = `<h2>Predicted Iris Class: ${result.prediction}</h2>`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<h2>Error: Failed to make prediction.</h2>`;
    });
});