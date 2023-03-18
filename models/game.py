from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    users = relationship("User", backref="game")

    def __repr__(self):
        return f"<User {self.name}>"
