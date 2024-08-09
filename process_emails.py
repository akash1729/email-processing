import os
from models.rule_engine import RuleEngine
from email_clients.gmail_client import GmailClient
from datastore.sqlite import SQLiteEmailManager
from models.email_service import EmailService


def run_rules_for_all_emails():

    artifact_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "artifacts"
    )

    rules_json_path = os.path.join(artifact_directory, "rules.json")
    credential_path = os.path.join(artifact_directory, "credentials.json")
    db_path = os.path.join(artifact_directory, "emails.db")

    rule_engine = RuleEngine()
    rule_engine.load_rules_from_json(json_file=rules_json_path)

    email_client = GmailClient()
    email_client.login(credential_path=credential_path)

    data_store = SQLiteEmailManager(db_name=db_path)

    email_service = EmailService(email_client=email_client, data_store=data_store)

    all_emails = email_service.get_all_email_from_datastore()

    for email in all_emails:
        rule_engine.run_rules(email, email_client)


run_rules_for_all_emails()
