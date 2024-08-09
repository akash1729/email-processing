from email_clients.client_interface import EmailClient
from datastore.datastore_interface import EmailDataStore

from models.email import Email


class EmailService:

    def __init__(self, email_client: EmailClient, data_store: EmailDataStore):
        self.email_client = email_client
        self.data_store = data_store

    def fetch_and_store_emails(self):
        emails = self.email_client.fetch_emails()
        for email in emails:
            email_obj = Email.create_email_client(email, self.email_client.client_name)

            self.data_store.add_email(email_obj)

    def store_emails(self, emails):
        self.email_service.store_emails(emails)
