from flask import Flask
from routes.game import game_bp


app = Flask(__name__)

app.register_blueprint(game_bp)


@app.route("/")
def index():
    return "hello"


if __name__ == "__main__":
    app.run(port=10200, debug=True, host="0.0.0.0")
