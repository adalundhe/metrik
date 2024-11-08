from typing import Any, Dict, Optional
from metrik.connectors.common.types import ConnectorTypes
from pydantic import BaseModel


class KafkaConfig(BaseModel):
    host: str='localhost:9092'
    client_id: str='metrik'
    group_id: str='metrik'
    metrics_partition: int=0
    compression_type: Optional[str]
    timeout: int=1000
    idempotent: bool=True
    options: Dict[str, Any]={}
    reporter_type: ConnectorTypes=ConnectorTypes.Kafka