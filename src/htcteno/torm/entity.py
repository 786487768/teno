from sqlalchemy import Column
from sqlalchemy.types import String, SmallInteger, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    user = Column(String)
    slurm_id = Column(Integer)
    task_type = Column(SmallInteger)
    state = Column(SmallInteger)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    redis_host = Column(String)
    redis_port = Column(Integer)
    total_jobs = Column(Integer)
    command = Column(String)


class Jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf-8'
    }

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    celery_id = Column(String)
    state = Column(SmallInteger)
    end_time = Column(DateTime)
    command = Column(String)


if __name__ == '__main__':
    engine = create_engine(
        "mysql+mysqlconnector://ll:816543@localhost:3306/tasks_info")
    DBsession = sessionmaker(bind=engine)
    start_time = datetime.datetime.now()
    new_task = Tasks(user=1000, slurm_id=7, task_type=0, state=0,
                     start_time=start_time, redis_host='localhost')
    new_job = Jobs(task_id=1, celery_id="45154321-SD445FJL",
                   state=0, end_time=start_time, command="/bin/hostname")
    session = DBsession()
    result = session.query(Tasks.id).filter_by(user=10000).one()
    print(result[0])
    session.commit()
    session.close()
