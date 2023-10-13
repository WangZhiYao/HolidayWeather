from abc import ABC, abstractmethod

from model import Message


class PushApi(ABC):

    @abstractmethod
    def send_push(self, message: Message) -> bool:
        pass
