from enum import Enum


class ConnectorTypes(Enum):
    AWSLambda='aws_lambda'
    AWSTimestream='aws_timestream'
    BigQuery='bigquery'
    BigTable='bigtable'
    Cassandra='cassandra'
    Cloudwatch='cloudwatch'
    CosmosDB='cosmosdb'
    CSV='csv'
    Datadog='datadog'
    DogStatsD='dogstatsd'
    GCS='gcs'
    Graphite='graphite'
    Honeycomb='honeycomb'
    InfluxDB='influxdb'
    JSON='json'
    Kafka='kafka'
    MongoDB='mongodb'
    MySQL='mysql'
    Netdata='netdata'
    NewRelic='newrelic'
    Postgres='postgres'
    Prometheus='prometheus'
    Redis='redis'
    S3='s3'
    Snowflake='snowflake'
    SQLite='sqlite'
    StatsD='statsd'
    Telegraf='telegraf'
    TelegrafStatsD='telegraf_statsd'
    TimescaleDB='timescaledb'
    XML='xml'