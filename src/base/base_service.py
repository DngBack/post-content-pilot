from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .base_model import CustomBaseModel as BaseModel


class BaseService(ABC, BaseModel):
    @abstractmethod
    def process(self, inputs: Any) -> Any:
        raise NotImplementedError()
