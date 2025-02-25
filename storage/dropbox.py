import dropbox
import os

ACCESS_TOKEN = "your-dropbox-access-token"

def authenticate_dropbox():
    """Authenticate with Dropbox API."""
    return dropbox.Dropbox(ACCESS_TOKEN)

def upload_to_dropbox(file_path):
    """Uploads a file to Dropbox."""
    dbx = authenticate_dropbox()
    dropbox_path = "/" + os.path.basename(file_path)
    with open(file_path, "rb") as file:
        dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    print(f"Uploaded {dropbox_path} to Dropbox")
    return dropbox_path

def list_dropbox_files():
    """Lists files in Dropbox."""
    dbx = authenticate_dropbox()
    response = dbx.files_list_folder("")
    for file in response.entries:
        print(f"File: {file.name}, Path: {file.path_lower}")

def delete_dropbox_file(file_path):
    """Deletes a file from Dropbox by file path."""
    dbx = authenticate_dropbox()
    dbx.files_delete_v2(file_path)
    print(f"Deleted file: {file_path}")

# Example usage
if __name__ == "__main__":
    file_path = upload_to_dropbox("document.pdf")
    list_dropbox_files()
    delete_dropbox_file(file_path)
