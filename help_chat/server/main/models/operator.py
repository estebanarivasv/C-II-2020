from main.config import Base
from sqlalchemy import Column, Integer, String, Boolean


class OperatorModel(Base):

    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    department = Column(String(50))

    def __repr__(self):
        return f"<User({self.id}, {self.host}, {self.department}, {self.role})>"
