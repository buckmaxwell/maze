import random
from models.maze import Maze
from models.room import Room
from sqlalchemy.orm import Session


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"N": True, "S": True, "E": True, "W": True}


class MazeGenerator:
    def __init__(self, width, height, loop_probability=0.1):
        self.width = width
        self.height = height
        self.loop_probability = loop_probability
        self.maze = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.generate_maze()

    def generate_maze(self):
        start_x, start_y = random.randint(0, self.width - 1), random.randint(
            0, self.height - 1
        )
        self.prim_algorithm(self.maze[start_x][start_y])

    def prim_algorithm(self, start_cell):
        frontier = [start_cell]

        while frontier:
            current_cell = random.choice(frontier)
            current_cell.visited = True

            neighbors = self.get_unvisited_neighbors(current_cell)
            if neighbors:
                neighbor = random.choice(neighbors)
                self.remove_wall_between_cells(current_cell, neighbor)
                frontier.append(neighbor)
            else:
                frontier.remove(current_cell)

        self.add_loops()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = ["N", "S", "E", "W"]

        for direction in directions:
            new_x, new_y = self.get_new_coordinates(cell.x, cell.y, direction)
            if self.is_valid_move(new_x, new_y):
                neighbor = self.maze[new_x][new_y]
                if not neighbor.visited:
                    neighbors.append(neighbor)

        return neighbors

    def remove_wall_between_cells(self, cell1, cell2):
        if cell1.x == cell2.x:
            if cell1.y > cell2.y:
                cell1.walls["N"] = False
                cell2.walls["S"] = False
            else:
                cell1.walls["S"] = False
                cell2.walls["N"] = False
        else:
            if cell1.x > cell2.x:
                cell1.walls["W"] = False
                cell2.walls["E"] = False
            else:
                cell1.walls["E"] = False
                cell2.walls["W"] = False

    def add_loops(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.maze[x][y]
                directions = ["N", "S", "E", "W"]
                random.shuffle(directions)

                for direction in directions:
                    if random.random() < self.loop_probability:
                        new_x, new_y = self.get_new_coordinates(
                            cell.x, cell.y, direction
                        )
                        if self.is_valid_move(new_x, new_y):
                            neighbor = self.maze[new_x][new_y]
                            self.remove_wall_between_cells(cell, neighbor)

    def get_new_coordinates(self, x, y, direction):
        if direction == "N":
            return x, y - 1
        elif direction == "S":
            return x, y + 1
        elif direction == "E":
            return x + 1, y
        elif direction == "W":
            return x - 1, y

    def is_valid_move(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


def save_maze_to_database(generated_maze, session: Session, game_id: int):
    maze = Maze(
        width=generated_maze.width,
        height=generated_maze.height,
        loop_probability=int(generated_maze.loop_probability * 100),
        game_id=game_id,
    )

    for x in range(generated_maze.width):
        for y in range(generated_maze.height):
            cell = generated_maze.maze[x][y]
            walls = 0
            for direction, wall in cell.walls.items():
                if wall:
                    walls |= 1 << "NWSE".index(direction)

            room = Room(x=x, y=y, walls=walls)
            maze.rooms.append(room)

    exit_room_index = random.randint(0, len(maze.rooms) - 1)
    maze.rooms[exit_room_index].exit = True

    session.add(maze)
    session.commit()
