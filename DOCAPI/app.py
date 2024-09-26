from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

def upload_to_azure_storage(connection_string, container_name, file, blob_name):
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Create a container client
    container_client = blob_service_client.get_container_client(container_name)

    # Create a blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the file
    blob_client.upload_blob(file)

@app.route('/upload', methods=['POST'])
def upload_file():
    azure_connection_string = request.form.get('azure_connection_string')
    container_name = request.form.get('container_name')

    if not azure_connection_string or not container_name:
        return jsonify({"error": "Missing required parameters"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    blob_name = secure_filename(file.filename)

    try:
        upload_to_azure_storage(azure_connection_string, container_name, file.stream, blob_name)
        sourceUrl = f"https://storeaudio.blob.core.windows.net/{container_name}/{blob_name}"
        return jsonify({"message": "File uploaded successfully", "blob_name": blob_name, "sourceUrl": sourceUrl}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
