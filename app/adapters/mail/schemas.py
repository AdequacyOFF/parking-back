from app.utils.model import AppBaseModel


class MASendMessageCommand(AppBaseModel):
    title: str
    body: str
