from collections import deque

from models.room import Room
from models.maze import Maze
from models.game import Game
from models.user import User

from models.base import engine

from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)


def get_adjacent_rooms(session: Session, room: Room, visited: set):
    directions = ["N", "W", "S", "E"]
    adjacent_rooms = []

    for i, direction in enumerate(directions):
        if not (room.walls & (1 << i)):  # If there is no wall in this direction
            next_x = room.x + (direction == "E") - (direction == "W")
            next_y = room.y + (direction == "S") - (direction == "N")
            next_room = Room.get_by_coordinates(
                session, next_x, next_y, room.maze_id
            )  # Implement this method in your Room model
            if next_room and next_room not in visited:
                adjacent_rooms.append((next_room, direction))

    return adjacent_rooms


def find_exit(session, maze):
    start_room = Room.get_by_coordinates(
        session, 0, 0, maze.id
    )  # Implement this method in your Room model
    visited = set()
    stack = deque([(start_room, "")])

    while stack:
        current_room, path = stack.pop()
        visited.add(current_room)

        if current_room.exit:
            return path

        adjacent_rooms = get_adjacent_rooms(session, current_room, visited)
        for next_room, direction in adjacent_rooms:
            stack.append((next_room, path + direction))

    return None


def test_maze():
    session = Session()

    maze = session.query(Maze).first()

    path_to_exit = find_exit(session, maze)
    num_visited_rooms = len(path_to_exit)

    print(f"Visited {num_visited_rooms} rooms before escaping.")
    raise Exception(f"Visited {num_visited_rooms} rooms before escaping.")
