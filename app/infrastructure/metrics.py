from enum import Enum

from prometheus_client import Counter


class MetricsType(str, Enum):
    CREATED_USER = "CREATED_USER"
    REGISTERED_USER = "REGISTERED_USER"
    DELETED_USER = "DELETED_USER"


class MetricClient:
    def __init__(self) -> None:
        self.metrics = {
            MetricsType.CREATED_USER: Counter("accounts:user:created:count", "Количество пользователей в системе"),
            MetricsType.REGISTERED_USER: Counter(
                "accounts:user:registered:count", "Количество пользователей, зарегистрированных в системе"
            ),
            MetricsType.DELETED_USER: Counter(
                "accounts:user:deleted:count", "Количество пользователей, удаленных из системы"
            ),
        }

    def register_metric(self, account_metric: MetricsType) -> None:
        metric = self.metrics[account_metric]
        if isinstance(metric, Counter):
            metric.inc()
