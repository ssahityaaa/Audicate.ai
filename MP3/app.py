from flask import Flask, request, jsonify, send_file
import requests
import zipfile
import os
import io

app = Flask(__name__)

def extract_mp3_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_contents = zip_ref.namelist()
        mp3_files = [file for file in zip_contents if file.endswith('.mp3')]
        if mp3_files:
            mp3_file = mp3_files[0]
            mp3_content = zip_ref.read(mp3_file)
            return mp3_content
        else:
            return None

@app.route('/extract_mp3', methods=['POST'])
def extract_mp3():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    response = requests.get(url)
    
    if response.status_code == 200:
        with open("temp.zip", "wb") as f:
            f.write(response.content)
        
        mp3_content = extract_mp3_from_zip("temp.zip")
        if mp3_content:
            os.remove("temp.zip")  # Remove the temporary zip file
            return send_file(io.BytesIO(mp3_content), mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'No MP3 file found in the zip'}), 404
    else:
        return jsonify({'error': 'Failed to download the zip file'}), 500

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
