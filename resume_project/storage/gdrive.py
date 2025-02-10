from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes

def authenticate_google_drive():
    """Authenticate and create a PyDrive client."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens a browser for OAuth authentication
    return GoogleDrive(gauth)

def upload_to_google_drive(file_path):
    """Uploads a file to Google Drive."""
    drive = authenticate_google_drive()
    file_name = file_path.split("/")[-1]  # Extract filename from path
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    
    file = drive.CreateFile({'title': file_name, 'mimeType': mime_type})
    file.SetContentFile(file_path)
    file.Upload()
    print(f"Uploaded {file_name} to Google Drive")
    return file['id']  # Returns the file ID

def list_google_drive_files():
    """Lists files in Google Drive."""
    drive = authenticate_google_drive()
    file_list = drive.ListFile({'q': "trashed=false"}).GetList()
    for file in file_list:
        print(f"File: {file['title']}, ID: {file['id']}")

def delete_google_drive_file(file_id):
    """Deletes a file from Google Drive by file ID."""
    drive = authenticate_google_drive()
    file = drive.CreateFile({'id': file_id})
    file.Delete()
    print(f"Deleted file with ID: {file_id}")

# Example usage
if __name__ == "__main__":
    file_id = upload_to_google_drive("document.pdf")
    list_google_drive_files()
    delete_google_drive_file(file_id)
