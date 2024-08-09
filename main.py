from email_clients.gmail_client import GmailClient
from datastore.sqlite import SQLiteEmailManager
from services.email_service import EmailService
from models.email import Email


def main():

    gmail_client = GmailClient()
    gmail_client.login(
        "/home/akash/WorkingDirectory/happy-fox-assignment/credentials.json"
    )
    data_store = SQLiteEmailManager()

    email_service = EmailService(gmail_client, data_store)
    email_service.fetch_and_store_emails()


main()
