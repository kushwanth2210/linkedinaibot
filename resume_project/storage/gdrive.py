from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes
import os
import shutil

def upload_client_secrets():
    """Prompt the user to upload the client_secrets.json file."""
    client_secrets_path = input("\U0001F4C2 Enter the full path of your client_secrets.json file: ").strip()

    if not os.path.exists(client_secrets_path):
        raise FileNotFoundError(f"❌ Error: File '{client_secrets_path}' not found.")

    destination_path = os.path.join(os.getcwd(), "client_secrets.json")
    shutil.copy(client_secrets_path, destination_path)
    print(f"✅ client_secrets.json uploaded successfully to {destination_path}")

def authenticate_google_drive():
    """Authenticate and create a PyDrive client."""
    gauth = GoogleAuth()
    client_secrets_path = os.path.join(os.getcwd(), "client_secrets.json")
    
    if not os.path.exists(client_secrets_path):
        print("⚠️ No client_secrets.json found.")
        upload_client_secrets()

    # Load or create credentials
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    
    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

def upload_to_google_drive(file_path):
    """Uploads a file to Google Drive."""
    drive = authenticate_google_drive()
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Error: File '{file_path}' not found.")
    
    file_name = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    file = drive.CreateFile({'title': file_name, 'mimeType': mime_type})
    file.SetContentFile(file_path)
    file.Upload()
    
    print(f"✅ Uploaded {file_name} to Google Drive (ID: {file['id']})")
    return file['id']

def list_google_drive_files():
    """Lists files in Google Drive."""
    drive = authenticate_google_drive()
    file_list = drive.ListFile({'q': "trashed=false"}).GetList()

    if not file_list:
        print("📂 No files found in Google Drive.")
    else:
        for file in file_list:
            print(f"📄 File: {file['title']} (ID: {file['id']})")

def delete_google_drive_file(file_id):
    """Deletes a file from Google Drive by file ID."""
    drive = authenticate_google_drive()
    file = drive.CreateFile({'id': file_id})
    file.Delete()
    print(f"❌ Deleted file with ID: {file_id}")

# Main execution
if __name__ == "__main__":
    print("\n🌐 Google Drive Automation Started...")
    
    if not os.path.exists("client_secrets.json"):
        upload_client_secrets()
    
    print("\nSelect an option:")
    print("1️⃣ Upload a file to Google Drive")
    print("2️⃣ List files in Google Drive")
    print("3️⃣ Delete a file from Google Drive")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        file_path = input("📄 Enter the full path of the file to upload: ").strip()
        upload_to_google_drive(file_path)
    elif choice == "2":
        list_google_drive_files()
    elif choice == "3":
        file_id = input("❌ Enter the file ID to delete: ").strip()
        delete_google_drive_file(file_id)
    else:
        print("❌ Invalid choice. Exiting...")
