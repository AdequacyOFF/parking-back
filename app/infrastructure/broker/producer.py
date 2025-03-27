from asyncio import Event
from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from aiokafka.helpers import create_default_context

from app.infrastructure.broker.exceptions import KafkaException
from app.infrastructure.broker.schemas import KPProduceMessageCMD
from app.settings import EventSettings


class KafkaProducer:
    def __init__(self, settings: EventSettings) -> None:
        self._settings = settings
        self._producer = AIOKafkaProducer(
            bootstrap_servers=f"{self._settings.host}:{self._settings.port}",
            sasl_plain_username=self._settings.username,
            sasl_plain_password=self._settings.password,
            ssl_context=create_default_context(),
            sasl_mechanism="SCRAM-SHA-512",
            security_protocol="SASL_SSL",
        )
        self._shutdown_event = Event()
        self._is_shutdown = Event()

    async def produce_message(self, cmd: KPProduceMessageCMD) -> None:
        await self._producer.start()
        try:
            await self._producer.send_and_wait(cmd.topic, cmd.message, headers=cmd.headers)
        except KafkaError as error:
            raise KafkaException from error

    async def shutdown(self) -> None:
        await self._stop()
        self._shutdown_event.set()
        await self._is_shutdown.wait()

    async def _stop(self) -> None:
        await self._producer.stop()
        self._is_shutdown.set()


async def init_kafka_producer(settings: EventSettings) -> AsyncGenerator[KafkaProducer, None]:
    kafka_producer = KafkaProducer(settings=settings)
    yield kafka_producer
    await kafka_producer.shutdown()
