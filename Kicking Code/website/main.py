from flask import Flask, render_template
from session import session
from _visualization import visualize
from _stats import stats

import webbrowser, math


app = Flask(__name__)
app.register_blueprint(session, url_prefix="")
app.register_blueprint(visualize, url_prefix="")
app.register_blueprint(stats, url_prefix="")


@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/session")
def test():
    return render_template('session.html')

@app.route("/comingsoon")
def comingsoon():
    return render_template('coming_soon.html')

@app.route("/stats")
def stats():
    return render_template('stats.html')

@app.route("/visualize")
def visualization():
    return render_template('visualize.html')

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:4000/home")
    
    # Run the Flask app
    app.run('127.0.0.1', 4000, debug=True)