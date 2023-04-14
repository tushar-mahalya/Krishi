const form = document.getElementById('plant-disease-form');
const resultDiv = document.getElementById('result-div');
const errorDiv = document.getElementById('error-div');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const plantType = document.getElementById('plant-type').value;
    const fileInput = document.getElementById('image-file');
    const file = fileInput.files[0];

    if (!file) {
        errorDiv.innerHTML = 'Please select an image file.';
        resultDiv.innerHTML = '';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`https://150f-3-135-152-169.ngrok-free.app/detect-disease?plant_type=${plantType}`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            errorDiv.innerHTML = 'Error occurred while detecting the disease.';
            resultDiv.innerHTML = '';
            return;
        }

        const result = await response.json();
        errorDiv.innerHTML = '';
        resultDiv.innerHTML = `
            <div class="result">
                <p>Detected disease: ${result.disease}</p>
                <p>Accuracy: ${result.accuracy}%</p>
            </div>
        `;
    } catch (error) {
        errorDiv.innerHTML = 'Error occurred while communicating with the server.';
        resultDiv.innerHTML = '';
    }
});
