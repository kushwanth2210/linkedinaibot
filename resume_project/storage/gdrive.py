import os
import mimetypes
import shutil
from abc import ABC, abstractmethod
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveManager(ABC):
    """
    Abstract base class for handling Google Drive file management.
    Requires explicit file name input for all actions.
    """

    def __init__(self):
        self.drive = self.authenticate_google_drive()

    @staticmethod
    def upload_client_secrets():
        """Prompt the user to upload the client_secrets.json file if it does not exist."""
        client_secrets_path = input("\U0001F4C2 Enter the full path of your client_secrets.json file: ").strip()

        if not os.path.exists(client_secrets_path):
            raise FileNotFoundError(f"❌ Error: File '{client_secrets_path}' not found.")

        destination_path = os.path.join(os.getcwd(), "client_secrets.json")
        shutil.copy(client_secrets_path, destination_path)
        print(f"✅ client_secrets.json uploaded successfully to {destination_path}")

    @staticmethod
    def authenticate_google_drive():
        """Authenticate and create a PyDrive client."""
        gauth = GoogleAuth()
        client_secrets_path = os.path.join(os.getcwd(), "client_secrets.json")

        if not os.path.exists(client_secrets_path):
            print("⚠️ No client_secrets.json found.")
            GoogleDriveManager.upload_client_secrets()

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

    @abstractmethod
    def upload_file(self, file_path: str, file_name: str):
        """Uploads a file to Google Drive with a specified name."""
        pass

    @abstractmethod
    def list_files(self):
        """Lists files in Google Drive."""
        pass

    @abstractmethod
    def delete_file(self, file_id: str):
        """Deletes a file from Google Drive by file ID."""
        pass


class GoogleDriveHandler(GoogleDriveManager):
    """
    Concrete implementation of GoogleDriveManager to handle file operations.
    """

    def upload_file(self, file_path: str, file_name: str):
        """
        Uploads a file to Google Drive with a user-specified file name.
        Ensures the correct file extension if the user forgets to include it.

        :param file_path: Full path of the file on local disk.
        :param file_name: Custom file name for Google Drive (extension will be ensured).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Error: File '{file_path}' not found.")

        # Extract original extension from the file
        original_extension = os.path.splitext(file_path)[1]

        # If the user does not specify an extension, append the original one
        if not os.path.splitext(file_name)[1]:
            file_name += original_extension

        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        file = self.drive.CreateFile({'title': file_name, 'mimeType': mime_type})
        file.SetContentFile(file_path)
        file.Upload()

        print(f"✅ Uploaded {file_name} to Google Drive (ID: {file['id']})")
        return file['id']

    def list_files(self):
        """Lists all files in Google Drive."""
        file_list = self.drive.ListFile({'q': "trashed=false"}).GetList()

        if not file_list:
            print("📂 No files found in Google Drive.")
        else:
            for file in file_list:
                print(f"📄 File: {file['title']} (ID: {file['id']})")

    def delete_file(self, file_id: str):
        """Deletes a file from Google Drive by file ID."""
        file = self.drive.CreateFile({'id': file_id})
        file.Delete()
        print(f"❌ Deleted file with ID: {file_id}")


# Main Execution
if __name__ == "__main__":
    print("\n🌐 Google Drive Automation Started...")

    drive_handler = GoogleDriveHandler()

    print("\nSelect an option:")
    print("1️⃣ Upload a file to Google Drive")
    print("2️⃣ List files in Google Drive")
    print("3️⃣ Delete a file from Google Drive")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        file_path = input("📄 Enter the full path of the file to upload: ").strip()
        file_name = input("📝 Enter the desired file name for Google Drive (without extension if unsure): ").strip()
        drive_handler.upload_file(file_path, file_name)
    elif choice == "2":
        drive_handler.list_files()
    elif choice == "3":
        file_id = input("❌ Enter the file ID to delete: ").strip()
        drive_handler.delete_file(file_id)
    else:
        print("❌ Invalid choice. Exiting...")
