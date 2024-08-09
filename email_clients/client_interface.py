from abc import ABC, abstractmethod
from typing import List, Dict, Any


class EmailClient(ABC):

    @abstractmethod
    def login(self, credential_path: str) -> None:
        pass

    @abstractmethod
    def fetch_emails(
        self, user_id: str = "me", max_results: int = 10, query: str = ""
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def mark_as_read(self, msg_id: str, user_id: str = "me") -> None:
        pass

    @abstractmethod
    def mark_as_unread(self, msg_id: str, user_id: str = "me") -> None:
        pass

    @abstractmethod
    def move_message(self, msg_id: str, destination: str, user_id: str = "me") -> None:
        pass

    @property
    @abstractmethod
    def client_name(self) -> str:
        pass
