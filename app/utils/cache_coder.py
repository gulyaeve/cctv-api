import pickle
from typing import Any
from fastapi_cache.coder import Coder


class PickleCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return pickle.dumps(value)

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return pickle.loads(value)