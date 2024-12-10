from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("address", String, primary_key=True, nullable=False)
)
