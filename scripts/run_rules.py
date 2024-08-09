
from models.rule_engine import RuleEngine
from email_clients.gmail_client import GmailClient
from datastore.sqlite import SQLiteEmailManager

def run_rules_for_all_emails():

    rule_engine = RuleEngine()
    rule_engine.load_rules_from_json("rules.json")

    email_client = GmailClient()
    email_client.login(
        "/home/akash/WorkingDirectory/happy-fox-assignment/credentials.json"
    )

    data_store = SQLiteEmailManager()
    all_emails = data_store.get_all_emails()

    for email in all_emails:
        rule_engine.run_rules(email, email_client)

run_rules_for_all_emails()