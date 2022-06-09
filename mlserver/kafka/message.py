from typing import Dict, Optional

from pydantic import BaseModel


class KafkaMessage(BaseModel):
    key: Optional[str] = None
    value: str
    headers: Dict[str, str]
