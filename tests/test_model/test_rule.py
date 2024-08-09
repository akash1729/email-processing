import unittest
from unittest.mock import Mock, create_autospec
import datetime

from models.rule import Rule, Condition, Action

from email_clients.client_interface import EmailClient
from tests.factories.email import EmailFactory


class TestAction(unittest.TestCase):

    def setUp(self):
        self.email_client = Mock(spec=EmailClient)
        self.email = EmailFactory()

    def test_action_move(self):
        action_type = "move"
        action_param = "spam"
        action = Action(action_type, action_param)
        action.perform_action(self.email, self.email_client)

        self.email_client.move_message.assert_called_with(msg_id=self.email.reference_id, destination=action_param)

    def test_action_mark_as_read(self):
        action_type = "mark as read"
        action = Action(action_type)
        action.perform_action(self.email, self.email_client)

        self.email_client.mark_as_read.assert_called_with(msg_id=self.email.reference_id)

    def test_action_mark_as_unread(self):
        action_type = "mark as unread"
        action = Action(action_type)
        action.perform_action(self.email, self.email_client)

        self.email_client.mark_as_unread.assert_called_with(msg_id=self.email.reference_id)

    def test_action_invalid(self):
        action_type = "invalid"
        with self.assertRaises(ValueError):
            action = Action(action_type)


class TestCondition(unittest.TestCase):

    def test_condition_contains(self):
        email = EmailFactory(subject="this is a spam")
        field_name = "subject"
        predicate = "contains"
        value = "spam"
        condition = Condition(field_name, predicate, value)

        self.assertTrue(condition.check_condition(email))

    def test_condition_eq(self):

        email = EmailFactory(subject="my subject")
        field_name = "subject"
        predicate = "eq"
        value = email.subject
        condition = Condition(field_name, predicate, value)

        self.assertTrue(condition.check_condition(email))

    def test_condition_less_than(self):

        email = EmailFactory(received_time=datetime.datetime.now())
        field_name = "received_time"
        predicate = "less than"
        value = email.received_time + datetime.timedelta(days=1)
        condition = Condition(field_name, predicate, value)

        self.assertTrue(condition.check_condition(email))

    def test_condition_invalid(self):
        field_name = "subject"
        predicate = "invalid"
        value = "spam"
        with self.assertRaises(ValueError):
            Condition(field_name, predicate, value)


class TestRule(unittest.TestCase):

    def setUp(self):
        self.email_client = Mock(spec=EmailClient)
        self.email = EmailFactory()

    def test_rule_all(self):
        condition1 = create_autospec(Condition)
        condition1.check_condition.return_value = True
        condition2 = create_autospec(Condition)
        condition2.check_condition.return_value = True
        condition3 = create_autospec(Condition)
        condition3.check_condition.return_value = False

        rule = Rule("description", "all", [condition1, condition2], [])
        self.assertTrue(rule._run_all_rule(self.email))

        rule = Rule("description", "all", [condition1, condition3], [])
        self.assertFalse(rule._run_all_rule(self.email))

    def test_rule_any(self):
        condition1 = create_autospec(Condition)
        condition1.check_condition.return_value = False
        condition2 = create_autospec(Condition)
        condition2.check_condition.return_value = False
        condition3 = create_autospec(Condition)
        condition3.check_condition.return_value = True

        rule = Rule("description", "any", [condition1, condition2], [])
        self.assertFalse(rule._run_any_rule(self.email))

        rule = Rule("description", "any", [condition1, condition3], [])
        self.assertTrue(rule._run_any_rule(self.email))
