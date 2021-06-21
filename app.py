from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdefghij"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """ Show the homepage / board """

    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    return render_template("index.html", board=board, highscore=highscore, num_plays=num_plays)

@app.route("/check-word")
def check_word():
    """ Check if word is a valid word """

    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({"result": res})

@app.route("/post_score", methods=["POST"])
def post_score():
    """ Post score, highscore, and number of plays """

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    session["highscore"] = max(score, highscore)
    num_plays = session.get("num_plays", 0)
    session["num_plays"] = num_plays + 1

    return render_template("index.html", num_plays=num_plays, newHighscore=score > highscore)