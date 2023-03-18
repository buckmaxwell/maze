from sqlalchemy import Column, Integer, String, ForeignKey

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    team = Column(String(10), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
