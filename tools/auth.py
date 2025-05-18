import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CREDENTIALS_FILE = "token.pickle"
SCOPES = "https://www.googleapis.com/auth/gmail.modify"
CLIENT_SECRETS_FILE = "./tools/<NAME OF YOUR CLIENT SECRETS FILE>"


def authenticate():
    """Authenticates with Google using OAuth 2.0 and returns the Credentials object."""
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                os.remove(CREDENTIALS_FILE)
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print(f'Credentials saved to {CREDENTIALS_FILE}')
    return creds


if __name__ == '__main__':
    creds = authenticate()
    if creds:
        print("Authentication successful! Credentials obtained.")
        # You can now use the 'creds' object to build the Gmail service
    else:
        print("Authentication failed.")