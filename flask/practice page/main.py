from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/greet")
def greet():
    return render_template('greet.html', name = "User")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/userdata")
def user_form():
    return render_template('user_form.html')

@app.route("/result", methods=["GET", "POST"])
def result():
    #print(request.args["data"])
    print(request.form["data"])
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)