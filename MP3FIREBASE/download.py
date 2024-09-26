import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate("daimn-418605-firebase-adminsdk-z1llb-b1e6f5ecc5.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'daimn-418605.appspot.com'})


# Function to download media file
def download_media(file_path, destination_path):
    try:
        # Get a reference to the storage service, using the default Firebase App
        bucket = storage.bucket()
        blob = bucket.blob(file_path)

        # Download the file to a destination
        blob.download_to_filename(destination_path)
        print("File downloaded successfully.")
    except Exception as e:
        print("Error downloading file:", e)

# Example usage
file_path = "audicateaudio/20240506153719_0001.mp3"
destination_path = r"C:\Users\sahit\Dropbox\PC\Downloads\20240506153719_0001.mp3"
download_media(file_path, destination_path)
