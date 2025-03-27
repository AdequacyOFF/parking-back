from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class CreateFileCMD:
    file: UploadFile
