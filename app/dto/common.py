from pydantic import BaseModel


class Event:
    pass


class Command(BaseModel):
    pass


Message = Event | Command
