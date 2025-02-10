import requests
import msal
import mimetypes

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
TENANT_ID = "your-tenant-id"

def authenticate_onedrive():
    """Authenticate with Microsoft Graph API using OAuth 2.0."""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=authority)
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception("Failed to authenticate with OneDrive API")

def upload_to_onedrive(file_path):
    """Uploads a file to OneDrive."""
    access_token = authenticate_onedrive()
    headers = {"Authorization": f"Bearer {access_token}"}
    file_name = file_path.split("/")[-1]
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/content"
    
    with open(file_path, "rb") as file:
        response = requests.put(upload_url, headers=headers, data=file)
    
    if response.status_code in [200, 201]:
        print(f"Uploaded {file_name} to OneDrive")
        return response.json().get("id")
    else:
        print("Error:", response.json())

def list_onedrive_files():
    """Lists files in OneDrive."""
    access_token = authenticate_onedrive()
    headers = {"Authorization": f"Bearer {access_token}"}
    list_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    response = requests.get(list_url, headers=headers)
    
    if response.status_code == 200:
        files = response.json().get("value", [])
        for file in files:
            print(f"File: {file['name']}, ID: {file['id']}")
    else:
        print("Error:", response.json())

def delete_onedrive_file(file_id):
    """Deletes a file from OneDrive by file ID."""
    access_token = authenticate_onedrive()
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
    response = requests.delete(delete_url, headers=headers)
    
    if response.status_code == 204:
        print(f"Deleted file with ID: {file_id}")
    else:
        print("Error:", response.json())

# Example usage
if __name__ == "__main__":
    file_id = upload_to_onedrive("document.json")
    list_onedrive_files()
    delete_onedrive_file(file_id)
