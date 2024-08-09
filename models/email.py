import datetime


class Email:
    def __init__(
        self,
        from_add: str,
        subject: str,
        message: str,
        received_time: datetime.datetime,
        email_client: str,
        reference_id: str,
    ):
        self.from_add = from_add
        self.subject = subject
        self.message = message
        self.received_time = received_time
        self.client = email_client
        self.reference_id = reference_id

    @classmethod
    def create_email_client(cls, email_dict: dict, client: str):

        if client == "gmail":
            return cls(
                from_add=email_dict.get("from", ""),
                subject=email_dict.get("subject", ""),
                message=email_dict.get("content", ""),
                received_time=email_dict.get("date", datetime.datetime.now()),
                email_client="gmail",
                reference_id=email_dict["id"],
            )
        else:
            raise ValueError("Invalid email email_clients")

    def to_dict(self):
        return {
            "from": self.from_add,
            "subject": self.subject,
            "message": self.message,
            "received_time": self.received_time,
            "email_clients": self.client,
            "reference_id": self.reference_id,
        }
