from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    content: str
