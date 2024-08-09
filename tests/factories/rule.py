import factory
import random

from models.rule import Action, Condition, Rule

class ActionFactory(factory.Factory):
    class Meta:
        model = Action

    action_type = factory.LazyAttribute(lambda _: random.choice(['move', 'mark as read', 'mark as unread']))
    params = factory.Faker('word')


class ConditionFactory(factory.Factory):
    class Meta:
        model = Condition

    field_name = factory.Faker('word')
    predicate = factory.LazyAttribute(lambda _: random.choice(['contains', 'eq', 'less than']))
    value = factory.Faker('word')


class RuleFactory(factory.Factory):
    class Meta:
        model = Rule

    description = factory.Faker('sentence')
    collection_predicate = factory.LazyAttribute(lambda _: random.choice(['all', 'any']))
    conditions = factory.List([ConditionFactory()])
    actions = factory.List([ActionFactory()])