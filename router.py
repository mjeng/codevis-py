from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True, port=5010)
