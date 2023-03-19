from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.orm import Session


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    maze_id = Column(Integer, ForeignKey("mazes.id"))
    maze = relationship("Maze", back_populates="rooms")
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    walls = Column(Integer, nullable=False)
    exit = Column(Boolean, nullable=False, default=False)

    @classmethod
    def get_by_coordinates(cls, session: Session, x: int, y: int, maze_id: int):
        return session.query(cls).filter_by(x=x, y=y, maze_id=maze_id).first()
