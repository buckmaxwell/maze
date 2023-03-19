from flask import Blueprint, jsonify, request

from sqlalchemy.orm import sessionmaker

from models.game import Game
from models.user import User
from models.maze import Maze
from models.room import Room
from models.functions.maze import MazeGenerator
from models.functions.maze import save_maze_to_database

from models.base import engine

game_bp = Blueprint("game_bp", __name__)

Session = sessionmaker(bind=engine)


@game_bp.route("/game/create", methods=["POST"])
def create_game():
    session = Session()

    game_name = request.json.get("name", "Unnamed Game")
    game = Game(name=game_name)
    session.add(game)
    session.commit()

    return jsonify({"message": "Game created", "game_id": game.id}), 201


@game_bp.route("/game/join", methods=["POST"])
def join_game():
    session = Session()

    game_id = request.json.get("game_id")
    username = request.json.get("username")
    game = session.query(Game).filter_by(id=game_id).first()

    if not game:
        return jsonify({"message": "Game not found"}), 404

    user = User(username=username, game_id=game.id)
    session.add(user)
    session.commit()

    return jsonify({"message": f"User {username} has joined the game"}), 200


@game_bp.route("/game/start", methods=["POST"])
def start_game():
    session = Session()

    game_id = request.json.get("game_id")
    game = session.query(Game).filter_by(id=game_id).first()

    if not game:
        return jsonify({"message": "Game not found"}), 404

    if game.started:
        return jsonify({"message": "Game already started"}), 400

    number_of_players = len(game.users)
    board_size = number_of_players * 5
    generated_maze = MazeGenerator(board_size, board_size, loop_probability=0.1)
    save_maze_to_database(generated_maze, session, game_id)

    game.started = True
    session.commit()

    return jsonify({"message": "Game started", "maze_id": game.maze.id}), 200
