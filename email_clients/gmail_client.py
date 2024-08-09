from email_clients.client_interface import EmailClient
from google.oauth2.credentials import Credentials
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from typing import List, Dict, Any
import base64

from email.utils import parsedate_to_datetime


from email_clients.errors import ClientConnectionError


class GmailClient(EmailClient):
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self):
        self.email_client_name = "gmail"
        self.token_file_path = os.path.join(
            os.path.dirname(__file__), "token.json"
        )

        self.service = None
        self.credentials = None

    def login(self, credential_path: str) -> None:
        self.credentials = self._get_credentials(credential_path)
        self.service = build("gmail", "v1", credentials=self.credentials)

    def fetch_emails(
        self, user_id: str = "me", max_results: int = 10, query: str = ""
    ) -> List[Dict[str, Any]]:
        messages = []
        inbox_query = "label:inbox " + query

        try:
            request = (
                self.service.users()
                .messages()
                .list(userId=user_id, maxResults=max_results, q=inbox_query)
            )
        except HttpError as error:
            raise ClientConnectionError(
                f"Connection for client {self.client_name} failed: {error}"
            )

        while request is not None:
            response = request.execute()
            messages.extend(response.get("messages", []))
            request = self.service.users().messages().list_next(request, response)

            if len(messages) >= max_results:
                messages = messages[:max_results]
                break

        return [self._get_message_details(user_id, msg["id"]) for msg in messages]

    def _get_credentials(self, credential_path) -> Credentials:
        creds = None
        if os.path.exists(self.token_file_path):
            creds = Credentials.from_authorized_user_file(
                self.token_file_path, self.SCOPES
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file_path, "w") as token:
                token.write(creds.to_json())

        return creds

    def _get_message_details(self, user_id: str, msg_id: str) -> Dict[str, Any]:
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId=user_id, id=msg_id, format="full")
                .execute()
            )
        except HttpError as error:
            raise ClientConnectionError(
                f"Connection for client {self.client_name} failed: {error}"
            )

        payload = message["payload"]
        headers = {header["name"]: header["value"] for header in payload["headers"]}

        parts = payload.get("parts", [])
        body = payload.get("body", {})
        content = self._parse_content(body, parts)

        return {
            "id": message["id"],
            "threadId": message["threadId"],
            "labelIds": message["labelIds"],
            "snippet": message["snippet"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "date": parsedate_to_datetime(headers.get("Date", "")),
            "content": content,
        }

    def _parse_content(self, body: Dict[str, Any], parts: List[Dict[str, Any]]):

        content = ""
        if body.get("data"):
            content += base64.urlsafe_b64decode(body["data"]).decode("utf-8")

        if parts:
            for part in parts:
                mime_type = part.get("mimeType", "")
                if mime_type == "text/plain":
                    data = part["body"].get("data", "")
                    content += base64.urlsafe_b64decode(data).decode("utf-8")
                elif mime_type == "text/html":
                    data = part["body"].get("data", "")
                    content += base64.urlsafe_b64decode(data).decode("utf-8")
                elif "parts" in part:
                    content += self._parse_content(part["body"], part["parts"])

        return content

    def mark_as_read(self, msg_id: str, user_id: str = "me") -> None:
        pass

    def mark_as_unread(self, msg_id: str, user_id: str = "me") -> None:
        pass

    def move_message(self, msg_id: str, destination: str, user_id: str = "me") -> None:
        print("moving message to inbox ", msg_id)

    @property
    def client_name(self) -> str:
        return self.email_client_name


