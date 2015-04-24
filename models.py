# models.py - the ORM aspect of the program that describes the database structure
import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, SmallInteger, String, Time
from database import Base


class Job(Base):
    __tablename__ = 'job'
    id = Column('id', String, primary_key=True)
    status = Column('status', Enum('INCOMPLETE','IN_PROGRESS','COMPLETED'))
    url = Column('url', String, nullable=False)
    result = Column('result', String, nullable=False)
    priority = Column('priority', SmallInteger, nullable=False)
    created = Column('created', DateTime, default=datetime.datetime.now())
    updated = Column('updated', DateTime, onupdate=datetime.datetime.now())

    def __init__(self, id, status, url, priority, result):
        self.id = id
        self.status = status
        self.url = url
        self.priority = priority
        self.result = result

    def __repr__(self):
        return "<job(url='%s', status='%s', created='%s', updated='%s')>" % (self.url, self.status, self.created, self.updated)
