from abc import ABC, abstractmethod
from models.email import Email


class EmailDataStore(ABC):

    @abstractmethod
    def add_email(self, email: Email):
        pass

    @abstractmethod
    def get_all_emails(self):
        pass
