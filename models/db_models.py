# student.py
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey

from db.base import Base


class Training_session(Base):
    __tablename__ = 'trainings_table'

    id = Column(Integer, autoincrement=True, primary_key=True)

    time_key = Column(String)
    muscle_group = Column(String, nullable=False)
    exercise = Column(String, nullable=False)

    tonnage = Column(Integer, nullable=True)

    '''
    def __repr__(self) -> str:
        return f'Student [ID: {self.id}, ФИО: {self.full_name}], ' \
               f'grID: {self.group}, TgID: {self.telegram_id}]'
    '''
