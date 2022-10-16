from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pass
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)