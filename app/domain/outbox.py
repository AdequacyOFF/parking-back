from dataclasses import dataclass
from uuid import UUID, uuid4

from app.dto.outbox import CreateOutboxMessageCMD, OutboxMessageStatus


@dataclass
class OutboxMessage:
    id: UUID
    header: str
    body: str
    topic: str
    status: OutboxMessageStatus = OutboxMessageStatus.PENDING

    @classmethod
    def create(cls, cmd: CreateOutboxMessageCMD) -> "OutboxMessage":
        return cls(id=uuid4(), header=cmd.header, body=cmd.body, topic=cmd.topic)

    def send(self) -> None:
        self.status = OutboxMessageStatus.SEND
