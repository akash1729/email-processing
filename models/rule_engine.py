import json

from models.rule import Rule, Condition, Action


class RuleEngine:
    def __init__(self):
        self.rules = []

    def run_rules(self, email, email_client):
        for rule in self.rules:
            rule.run_rule(email, email_client)

    def load_rules_from_json(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
        for rule_data in data["rules"]:

            conditions = []
            for condition_data in rule_data["conditions"]:
                condition = Condition.from_dict(condition_data)
                conditions.append(condition)

            actions = []
            for action_data in rule_data["actions"]:
                action = Action.from_dict(action_data)
                actions.append(action)

            rule = Rule(
                description=rule_data["description"],
                collection_predicate=rule_data["collection_predicate"],
                conditions=conditions,
                actions=actions,
            )

            self.rules.append(rule)
