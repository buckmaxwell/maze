from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    users = relationship("User", backref="game")
    maze = relationship("Maze", back_populates="game", uselist=False)
    started = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.name}>"
