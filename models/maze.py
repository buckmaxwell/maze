from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base


class Maze(Base):
    __tablename__ = "mazes"

    id = Column(Integer, primary_key=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    loop_probability = Column(Integer, nullable=False)
    rooms = relationship("Room", back_populates="maze")
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship("Game", back_populates="maze")
