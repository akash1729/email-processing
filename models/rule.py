import datetime

from email_clients.client_interface import EmailClient
from models.email import Email
from typing import Any


class Action:

    def __init__(self, action_type: str, param: str = None):

        self.action_mapping = {
            "move": self._move_email,
            "mark as read": self._mark_as_read,
            "mark as unread": self._mark_as_unread,
        }

        if action_type not in self.action_mapping:
            raise ValueError(f"Invalid action type {action_type}")

        self.action_type = action_type
        self.param = param

    def perform_action(self, email: Email, email_client: EmailClient):
        if self.action_type not in self.action_mapping:
            raise ValueError("Invalid action type.")

        self.action_mapping[self.action_type](email, email_client)

    def _move_email(self, email: Email, email_client: EmailClient):
        email_client.move_message(msg_id=email.reference_id, destination=self.param)

    def _mark_as_read(self, email, email_client: EmailClient):
        email_client.mark_as_read(msg_id=email.reference_id)

    def _mark_as_unread(self, email, email_client: EmailClient):
        email_client.mark_as_unread(msg_id=email.reference_id)

    @classmethod
    def from_dict(cls, data):
        return cls(action_type=data["action"], param=data.get("value", None))


class Condition:

    def __init__(self, field_name: str, predicate: str, value: Any):

        self.condition_function_mapping = {
            "contains": self._contains,
            "eq": self._equals,
            "less than": self._less_than,
        }

        if predicate not in self.condition_function_mapping:
            raise ValueError(f"Invalid predicate {predicate}")

        self.field_name = field_name
        self.predicate = predicate
        self.value = value

    def check_condition(self, email: Email) -> bool:

        email_dict = email.to_dict()
        if self.predicate not in self.condition_function_mapping:
            raise ValueError("Invalid predicate.")

        return self.condition_function_mapping[self.predicate](email_dict)

    def _contains(self, email_dict: dict) -> bool:
        if isinstance(email_dict[self.field_name], str) and isinstance(self.value, str):
            return self.value in email_dict[self.field_name]
        else:
            raise ValueError(
                "Contains condition requires field name and value to be strings."
            )

    def _equals(self, email_dict: dict) -> bool:
        return self.value == email_dict[self.field_name]

    def _less_than(self, email_dict: dict):
        if isinstance(email_dict[self.field_name], int) and isinstance(self.value, int):
            return email_dict[self.field_name] < self.value
        elif isinstance(email_dict[self.field_name], datetime.datetime) and isinstance(
            self.value, datetime.datetime
        ):
            return email_dict[self.field_name] < self.value
        else:
            raise ValueError(
                "Less than condition requires field name and value to be integers or datetime objects."
            )

    @classmethod
    def from_dict(cls, data):

        if data["field_name"] == "received_time":
            received_date = datetime.datetime.strptime(
                data["value"], "%Y-%m-%d %H:%M:%S"
            )
            received_date = received_date.replace(tzinfo=datetime.timezone.utc)
            data["value"] = received_date

        return cls(
            field_name=data["field_name"],
            predicate=data["predicate"],
            value=data["value"],
        )


class Rule:

    def __init__(
        self,
        description: str,
        collection_predicate: str,
        conditions: list[Condition],
        actions: list[Action],
    ):
        self.description = description
        self.collection_predicate = collection_predicate
        self.conditions = conditions
        self.actions = actions

    def run_rule(self, email: Email, email_client: EmailClient):

        condition_met = False
        if self.collection_predicate.upper() == "ALL":
            condition_met = self._run_all_rule(email)
        elif self.collection_predicate.upper() == "ANY":
            condition_met = self._run_any_rule(email)

        if condition_met:
            self._run_actions(email, email_client)

    def _run_all_rule(self, email: Email):
        return all([condition.check_condition(email) for condition in self.conditions])

    def _run_any_rule(self, email: Email):
        return any([condition.check_condition(email) for condition in self.conditions])

    def _run_actions(self, email: Email, email_client: EmailClient):
        for action in self.actions:
            action.perform_action(email, email_client)
