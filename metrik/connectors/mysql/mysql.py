import warnings
import uuid
import datetime
from typing import List, Dict, Union, Any
from metrik.logging import MetrikLogger
from metrik.metrics import MetricStore
from metrik.metrics.types import (
    Event,
    Interval,
    Rate
)
from .mysql_config import MySQLConfig

try:
    import sqlalchemy as sa

    # Aiomysql will raise warnings if a table exists despite us
    # explicitly passing "IF NOT EXISTS", so we're going to
    # ignore them.
    import aiomysql
    warnings.filterwarnings('ignore', category=aiomysql.Warning)

    from aiomysql.sa import create_engine, SAConnection
    from sqlalchemy.schema import CreateTable
    
    has_connector = True

except Exception:
    sqlalchemy = object
    sa = object
    create_engine = object
    CreateTable = object
    SAConnection = object
    OperationalError = object
    has_connector = object



class MySQL:
    has_connector=has_connector

    def __init__(self, config: MySQLConfig) -> None:
        self.host = config.host
        self.database = config.database
        self.username = config.username
        self.password = config.password
        
        self._metrics_table = None

        self.metadata = sa.MetaData()
        self._engine = None
        self._connection = None

        self.session_uuid = str(uuid.uuid4())
        self.metadata_string: str = None
        self.logger = MetrikLogger()
        self.logger.initialize()

        self._store = MetricStore()

    async def connect(self):
        
        self._engine = await create_engine(
            db=self.database,
            host=self.host,
            user=self.username,
            password=self.password
        )

        self._connection: SAConnection = await self._engine.acquire()

    async def load(
        self,
        source_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],     
        timeout: Union[int, float]=None
    ):
        
        table = sa.Table(
            source_name,
            self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('metric_id', sa.VARCHAR(255)),
            sa.Column('name', sa.VARCHAR(255)),
            sa.Column('kind', sa.VARCHAR(255)),
            sa.Column('group', sa.VARCHAR(255)),
            sa.Column('timestamp', sa.DateTime()),
            sa.Column('value', sa.Float()),
        )

        await self._connection.execute(
            CreateTable(
                table,
                if_not_exists=True
            )
        )

        metrics_data: List[Dict[str, Any]] = []

        async for row in self._connection.execute(
            table.select().where(table.c.name == metric.name).order_by(
                table.c.timestamp.desc()
            ).limit(1)
        ):
            metrics_data.append({
                'metric_id': row.metric_id,
                'name': row.name,
                'kind': row.kind,
                'group': row.group,
                'timestamp': row.timestamp,
                'value': row.value,
            })

        return self._store.parse(
            metrics_data[-1]
        )

    async def send(
        self,
        destination_name: str,
        metric: Union[
            Event,
            Interval,
            Rate
        ],     
        timeout: Union[int, float]=None
    ):
        table = sa.Table(
            destination_name,
            self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('metric_id', sa.VARCHAR(255)),
            sa.Column('name', sa.VARCHAR(255)),
            sa.Column('kind', sa.VARCHAR(255)),
            sa.Column('group', sa.VARCHAR(255)),
            sa.Column('timestamp', sa.DateTime()),
            sa.Column('value', sa.Float()),
        )

        await self._connection.execute(
            CreateTable(
                table,
                if_not_exists=True
            )
        )

        async with self._connection.begin() as transaction:

            metric_data = metric.dict()
            metric_data['kind'] = metric.kind.value

            await self._connection.execute(
                table.insert().values(**metric_data)
            )

            await transaction.commit()

    async def close(self):
        await self._connection.close()
    


