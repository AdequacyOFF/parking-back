from tempfile import SpooledTemporaryFile

from pydantic import BaseModel, ConfigDict


class FSAGetFileCMD(BaseModel):
    file_name: str


class FSAUploadFileCMD(BaseModel):
    file_name: str
    file_content: SpooledTemporaryFile[bytes]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class FSAGetFileUrlCMD(BaseModel):
    file_name: str


class FSAGetFileUrlResult(BaseModel):
    url: str


class FSADeleteFilesCMD(BaseModel):
    file_paths: set[str]
