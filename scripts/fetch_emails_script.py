import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from email_clients.gmail_client import GmailClient
from datastore.sqlite import SQLiteEmailManager
from services.email_service import EmailService


def main():

    gmail_client = GmailClient()
    credential_path = (
        "/home/akash/WorkingDirectory/happy-fox-assignment/email_clients/credentials.json"
    )
    gmail_client.login(credential_path)

    data_store = SQLiteEmailManager()

    email_service = EmailService(gmail_client, data_store)
    email_service.fetch_and_store_emails()


if __name__ == "__main__":
    main()
