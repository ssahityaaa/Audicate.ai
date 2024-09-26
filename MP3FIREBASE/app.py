from flask import Flask, request, jsonify
import requests
import zipfile
import os
import io
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("daimn-418605-firebase-adminsdk-z1llb-b1e6f5ecc5.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'audicate-ai.appspot.com'})

def extract_mp3_from_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_contents = zip_ref.namelist()
            mp3_files = [file for file in zip_contents if file.endswith('.mp3')]
            if mp3_files:
                mp3_file = mp3_files[0]
                mp3_content = zip_ref.read(mp3_file)
                return mp3_content, mp3_file
            else:
                return None, None
    except Exception as e:
        print("Error extracting MP3 file from zip:", e)
        return None, None

@app.route('/extract_mp3', methods=['POST'])
def extract_mp3():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            with open("temp.zip", "wb") as f:
                f.write(response.content)
            
            mp3_content, mp3_filename = extract_mp3_from_zip("temp.zip")
            if mp3_content:
                # Generate a unique filename using timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"audicateaudio/{timestamp}_{mp3_filename}"
                
                # Upload MP3 file to Firebase Storage
                bucket = storage.bucket()
                blob = bucket.blob(filename)
                blob.upload_from_string(mp3_content, content_type='audio/mpeg')

                os.remove("temp.zip")  # Remove the temporary zip file
                
                # Get access token of the uploaded file
                access_token = blob.generate_signed_url(timedelta(days=1), method='GET')
                
                return jsonify({'success': f'MP3 file uploaded to Firebase Storage as {filename}', 'access_token': access_token}), 200
            else:
                return jsonify({'error': 'No MP3 file found in the zip'}), 404
        except Exception as e:
            print("Error processing file:", e)
            return jsonify({'error': 'Failed to process the file'}), 500
        finally:
            if os.path.exists("temp.zip"):
                os.remove("temp.zip")
    else:
        return jsonify({'error': 'Failed to download the zip file'}), 500

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
