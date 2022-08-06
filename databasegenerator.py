from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Master(Base):

    __tablename__ = "master"

    id = Column(Integer, primary_key=True)
    gid = relationship("Group")
    name = Column(String)
    OTMslaves = relationship("Slave")
    OTMtasks = relationship("Task")


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    masterid = Column(Integer, ForeignKey("master.id"))
    token = Column(String)


class Task(Base):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True)
    task_text = Column(Text)
    masterid = Column(Integer, ForeignKey("master.id"))
    slave_id = Column(Integer, ForeignKey("slave.id"))
    slave = relationship("Slave", backref=backref("task", uselist=False, nullable=True))
    

class Slave(Base):
    __tablename__ = "slave"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    masterid = Column(Integer, ForeignKey("master.id"))
    

Base.metadata.create_all(engine)