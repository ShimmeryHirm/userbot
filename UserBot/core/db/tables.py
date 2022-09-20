import datetime

from sqlalchemy import BigInteger, Column, Float, MetaData, String, TIMESTAMP, Boolean, ARRAY
from sqlalchemy.orm import declarative_base

BASE = declarative_base()
METADATA = BASE.metadata  # type: MetaData


class Notes(BASE):
    __tablename__ = 'notes'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    msg_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
