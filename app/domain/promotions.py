from dataclasses import dataclass, field
from datetime import date
from hashlib import sha1
from time import time
from uuid import UUID, uuid4

from fastapi import UploadFile
from PIL import Image

from app.domain.exception import FileInvalidFormatDomainException, InvalidFileExtensionDomainException
from app.dto.promotions import CreatePromotionCMD, PromotionStatus, UpdatePromotionCMD


@dataclass
class Promotion:
    id: UUID
    title: str
    description: str
    short_description: str
    start_date: date
    end_date: date
    url: str | None
    photo_name: str | None = field(default=None)
    status: PromotionStatus = field(default=PromotionStatus.ACTIVE)

    @classmethod
    def create(cls, cmd: CreatePromotionCMD) -> "Promotion":
        return cls(
            id=uuid4(),
            title=cmd.title,
            description=cmd.description,
            url=cmd.url,
            start_date=cmd.start_date,
            end_date=cmd.end_date,
            short_description=cmd.short_description,
        )

    def update(self, cmd: UpdatePromotionCMD) -> None:
        self.title = cmd.title
        self.description = cmd.description
        self.start_date = cmd.start_date
        self.end_date = cmd.end_date
        self.short_description = cmd.short_description
        if cmd.url:
            self.url = cmd.url

    def delete(self) -> None:
        self.status = PromotionStatus.INACTIVE

    def add_photo(self, file: UploadFile) -> None:
        hash_result = sha1(file.file.read() + str(time()).encode(), usedforsecurity=False)
        file_format = self._get_file_format(file=file)
        self.photo_name = f"{self.id}_{hash_result.hexdigest()}.{file_format}"

    @staticmethod
    def _get_file_format(file: UploadFile) -> str:
        try:
            with Image.open(file.file) as img:
                file_format = img.format.lower()
                if file_format in {"png", "jpg", "jpeg"}:
                    return img.format.lower()
                raise InvalidFileExtensionDomainException
        except Exception as e:
            raise FileInvalidFormatDomainException
