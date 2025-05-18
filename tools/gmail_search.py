"""Module defining the main class gmail"""
import datetime
import base64
from tools import auth
import json
from googleapiclient.discovery import build


class GmailClient:
    """Class representing a Gmail object."""

    def __init__(self) -> None:
        """Initializes the GmailClient by authenticating and building the service."""
        self.creds = auth.authenticate()
        self.service = self._build_service()

    def _build_service(self):
        """Builds the Gmail API service object.

        Returns:
            googleapiclient.discovery.Resource: The Gmail API service object, or None if an error occurs.
        """
        if self.creds:
            try:
                service = build('gmail', 'v1', credentials=self.creds)
                print("Gmail service created successfully.")
                return service
            except Exception as error:
                print(f'An error occurred while building the service: {error}')
                return None
        else:
            print("Credentials not available. Cannot build Gmail service.")
            return None

    def get_unread_email_count(self) -> dict:
        """Returns the total number of unread emails in the inbox.

        Returns:
            dict: A dictionary containing the total count of unread emails under the key 'unread_count',
                  or an error dictionary if the service is not initialized or an error occurs.
        """
        if not self.service:
            return {"error": "Gmail service not initialized."}

        try:
            results = self.service.users().messages().list(userId='me', q='is:unread').execute()
            unread_count = results.get('resultSizeEstimate', 0)
            return {"unread_count": unread_count}
        except Exception as error:
            return {"error": f"An error occurred while getting unread count: {error}"}

    def get_latest_unread_primary_email_body(self) -> dict:
        """Returns the request body of the latest unread email in the primary inbox.

        Returns:
            dict: A dictionary containing the 'subject' and 'body' of the latest unread email
                  in the primary inbox. Returns an empty dictionary if no such email is found,
                  or an error dictionary if the service is not initialized or an error occurs.
        """
        if not self.service:
            return {"error": "Gmail service not initialized."}

        try:
            query = 'is:unread category:primary'
            results = self.service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            messages = results.get('messages')

            if messages:
                message_id = messages[0]['id']
                message = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()
                payload = message.get('payload', {})
                headers = payload.get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                body_content = ""

                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            body_content = base64.urlsafe_b64decode(part['body']['data'].encode('utf-8')).decode('utf-8')
                            break  # Prefer plain text
                elif payload.get('body', {}).get('data'):
                    body_content = base64.urlsafe_b64decode(payload['body']['data'].encode('utf-8')).decode('utf-8')

                return {"subject": subject, "body": body_content}
            else:
                return {}  # Return an empty dictionary if no unread primary email is found

        except Exception as error:
            return {"error": f"An error occurred while fetching the latest unread primary email: {error}"}

    def find_email_by_keywords(self, keywords: str) -> dict:
        """Finds an email based on the provided keywords and returns its request body.

        Args:
            keywords (str): The keywords to search for in the email.

        Returns:
            dict: A dictionary containing the 'subject' and 'body' of the first matching email found.
                  Returns an empty dictionary if no matching email is found, or an error dictionary
                  if the service is not initialized or an error occurs.
        """
        if not self.service:
            return {"error": "Gmail service not initialized."}
        if not keywords:
            return {"error": "Keywords are required for searching emails."}

        try:
            query = f'in:all {keywords}'
            results = self.service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            messages = results.get('messages')

            if messages:
                message_id = messages[0]['id']
                message = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()
                payload = message.get('payload', {})
                headers = payload.get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                body_content = ""

                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            body_content = base64.urlsafe_b64decode(part['body']['data'].encode('utf-8')).decode('utf-8')
                            break  # Prefer plain text
                elif payload.get('body', {}).get('data'):
                    body_content = base64.urlsafe_b64decode(payload['body']['data'].encode('utf-8')).decode('utf-8')

                return {"subject": subject, "body": body_content}
            else:
                return {}  # Return an empty dictionary if no email is found with the keywords

        except Exception as error:
            return {"error": f"An error occurred while finding email by keywords: {error}"}