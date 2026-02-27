from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/greet")
def greet():
    return "<h1>Cau!</h1>"


if __name__ == "__main__":
    app.run(debug=True)