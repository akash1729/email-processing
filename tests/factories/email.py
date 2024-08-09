import factory
from models.email import Email


class EmailFactory(factory.Factory):
    class Meta:
        model = Email

    from_add = factory.Faker("email")
    subject = factory.Faker("sentence")
    message = factory.Faker("text")
    received_time = factory.Faker("date_time")
    email_client = "gmail"
    reference_id = factory.Faker("uuid4")
