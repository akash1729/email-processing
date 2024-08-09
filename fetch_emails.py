import os

from email_clients.gmail_client import GmailClient
from datastore.sqlite import SQLiteEmailManager
from models.email_service import EmailService


def main():

    email_count = 10
    email_label = ""

    artifact_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "artifacts"
    )

    credential_path = os.path.join(artifact_directory, "credentials.json")
    if not os.path.exists(credential_path):
        raise FileNotFoundError(f"Credentials file not found at {credential_path}")

    db_path = os.path.join(artifact_directory, "emails.db")

    gmail_client = GmailClient()
    gmail_client.login(credential_path)

    data_store = SQLiteEmailManager(db_name=db_path)

    email_service = EmailService(gmail_client, data_store)
    email_service.fetch_and_store_emails(email_count=email_count, email_label=email_label)


if __name__ == "__main__":
    main()
