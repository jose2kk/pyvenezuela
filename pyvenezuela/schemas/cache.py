from typing import Any

from pydantic import BaseModel


class CacheValueModel(BaseModel):
    """Cache Value Model."""

    value: Any
    expires_at: float
