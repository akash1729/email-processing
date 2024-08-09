import sqlite3
from models.email import Email
from datastore.datastore_interface import EmailDataStore
import os
import datetime

create_table_query = """
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_add VARCHAR NOT NULL,
        subject TEXT NOT NULL,
        content TEXT NOT NULL,
        received_time TIMESTAMP NOT NULL,
        email_clients VARCHAR NOT NULL,
        reference_id VARCHAR UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""


class SQLiteManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()


class SQLiteEmailManager(EmailDataStore):

    def __init__(self, db_name="emails.db"):

        db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.db_path = db_path
        self.initialize_database(self.db_path)

    @staticmethod
    def initialize_database(db_name: str):
        with SQLiteManager(db_name) as cursor:
            cursor.execute(create_table_query)

    def add_email(self, email: Email):
        with SQLiteManager(self.db_path) as cursor:
            cursor.execute(
                """
            INSERT INTO emails (from_add, subject, content, received_time, email_clients, reference_id)
            VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(reference_id) DO NOTHING
            """,
                (
                    email.from_add,
                    email.subject,
                    email.message,
                    email.received_time,
                    email.client,
                    email.reference_id,
                ),
            )

    def get_all_emails(self):
        with SQLiteManager(self.db_path) as cursor:
            cursor.execute(
                "SELECT id, from_add, subject, content, received_time, email_clients, reference_id  FROM emails"
            )
            emails = cursor.fetchall()

        email_objs = []
        for email in emails:
            email_obj = Email(
                from_add=email[1],
                subject=email[2],
                message=email[3],
                received_time=datetime.datetime.strptime(
                    email[4], "%Y-%m-%d %H:%M:%S%z"
                ),
                email_client=email[5],
                reference_id=email[6],
            )
            email_objs.append(email_obj)

        return email_objs
