class BoggleGameBoard {
    // Make a new game board

    constructor(boardId, seconds=60) {
        this.board = $("#" + boardId);
        this.words = new Set();
        this.score = 0;
        this.seconds = seconds;
        this.displayTimer();
        this.timer = setInterval(this.time.bind(this), 1000)

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    // Display a message

    displayMessage(message, cls) {
        $(".message", this.board).text(message).addClass(`message ${cls}`)     
    }

    // Display valid words

    displayWord(word) {
        $(".words", this.board).append($("<li>", {text:word}));
    }

    // Display the score

    displayScore() {
        $(".score", this.board).text(this.score);
    }

    // Display the timer

    displayTimer() {
        $(".time", this.board).text(this.seconds);
    }

    // Submit the words and check if words are valid

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);
        let word = $word.val();

        if(!word) return;
        if(this.words.has(word)) {
            this.displayMessage(`${word} has already been found!`, "error")
            return;
        }

        const response = await axios.get("/check-word", {params: {word: word}});
        if (response.data.result === "not-word") {
            this.displayMessage(`${word} is not a word!`, "error");
        }
        else if (response.data.result === "not-on-board") {
            this.displayMessage(`${word} is not on the board!`, "error");
        }
        else {
            this.displayWord(word);
            this.score += word.length;
            this.displayScore();
            this.words.add(word);
            this.displayMessage(`${word} has been added`, "success");
        }
        $word.val("");
    }
    
    // End the game

    async finalScore() {
        $(".add-word", this.board).hide();
        const response = await axios.post("/post-score", { score: this.score });
        if (response.data.newHighscore) {
            this.displayMessage(`${this.score} is a New Record!`, "success");
        }
        else {
            this.displayMessage(`${this.score} is your final score!`, "success");
        }
    }

    // Countdown timer
    
    time() {
        this.seconds -= 1;
        this.displayTimer();

        if (this.seconds == 0) {
            this.finalScore();

            clearInterval(this.timer);
        }
    }
}
