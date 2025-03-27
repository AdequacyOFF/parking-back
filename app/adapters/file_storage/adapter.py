from typing import Protocol

from aioboto3 import Session

from app.adapters.file_storage.schemas import FSADeleteFilesCMD, FSAGetFileUrlCMD, FSAGetFileUrlResult, FSAUploadFileCMD
from app.settings import FileStorageSettings


class IFileStorageAdapter(Protocol):
    async def upload_file(self, cmd: FSAUploadFileCMD) -> None:
        pass

    async def generate_file_url(self, cmd: FSAGetFileUrlCMD) -> FSAGetFileUrlResult:
        pass

    async def delete_files(self, cmd: FSADeleteFilesCMD) -> None:
        pass


class FileStorageAdapter(IFileStorageAdapter):
    def __init__(self, boto_session: Session, settings: FileStorageSettings):
        self._session = boto_session
        self._settings = settings

    async def upload_file(self, cmd: FSAUploadFileCMD) -> None:
        cmd.file_content.seek(0)
        async with self._session.client(
            service_name="s3",
            endpoint_url=self._settings.url,
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
        ) as client:
            await client.upload_fileobj(
                Fileobj=cmd.file_content,
                Bucket=self._settings.bucket_name,
                Key=f"{self._settings.files_path}/{cmd.file_name}",
            )

    async def generate_file_url(self, cmd: FSAGetFileUrlCMD) -> FSAGetFileUrlResult:
        async with self._session.client(
            service_name="s3",
            endpoint_url=self._settings.url,
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
        ) as client:
            url = await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._settings.bucket_name, "Key": f"{self._settings.files_path}/{cmd.file_name}"},
                ExpiresIn=self._settings.ttl_secs + 60,
            )
        return FSAGetFileUrlResult(url=url)

    async def delete_files(self, cmd: FSADeleteFilesCMD) -> None:
        async with self._session.client(
            service_name="s3",
            endpoint_url=self._settings.url,
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
        ) as client:
            await client.delete_objects(
                Bucket=self._settings.bucket_name,
                Delete={
                    'Objects': [{'Key': f"{self._settings.files_path}/{path}"} for path in cmd.file_paths],
                },
            )
