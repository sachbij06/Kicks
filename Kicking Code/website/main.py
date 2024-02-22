from flask import Flask, render_template
from test import test
from _visualization import visualize


app = Flask(__name__)
app.register_blueprint(test, url_prefix="")
app.register_blueprint(visualize, url_prefix="")


@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/stats")
def stats():
    return render_template('stats.html')

@app.route("/visualize")
def visualization():
    return render_template('visualize.html')

if __name__ == "__main__":
    app.run('127.0.0.1', 4000, debug = True)