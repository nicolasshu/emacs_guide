from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Generic, Protocol, TypeVar


class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


T_co = TypeVar("T_co", covariant=True)



# --- Dataclasses ---

@dataclass(slots=True)
class Configuration:
    app_id: str
    max_retries: int = 3
    debug_mode: bool = False
    tags: list[str] = field(default_factory=list)

    def is_production(self) -> bool:
        return not self.debug_mode and "prod" in self.tags


# --- Classic Classes & Inheritance ---

class DataProcessor:
    def __init__(self, name: str, status: Status = Status.PENDING) -> None:
        self.name = name
        self.status = status
        self._processed_count: int = 0

    @property
    def processed_count(self) -> int:
        return self._processed_count

    def process_item[T](self, item: T) -> T:
        self._processed_count += 1
        return item


class AsyncPipeline(DataProcessor):
    def __init__(self, name: str, batch_size: int = 64) -> None:
        super().__init__(name=name, status=Status.ACTIVE)
        self.batch_size = batch_size

    @classmethod
    def create_default(cls) -> "AsyncPipeline":
        return cls(name="default_pipeline", batch_size=128)

    @staticmethod
    def validate_batch(batch: list[int]) -> bool:
        return len(batch) > 0 and all(isinstance(x, int) for x in batch)


# --- Standalone Functions with Varied Signature Styles ---

def transform_records[K, V](
    records: dict[K, V],
    transformer: Callable[[V], V],
    *,
    filter_none: bool = True
) -> dict[K, V]:
    transformed: dict[K, V] = {}
    for key, value in records.items():
        new_value = transformer(value)
        if filter_none and new_value is None:
            continue
        transformed[key] = new_value
    return transformed


def calculate_metrics(*values: float, precision: int = 2) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "total": 0.0}

    total = sum(values)
    mean = total / len(values)
    return {
        "total": round(total, precision),
        "mean": round(mean, precision)
    }
