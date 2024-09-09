from flask import Flask, request, jsonify, render_template, Blueprint
import _data

app = Flask(__name__)

attempts = _data.get_all_data()

session = Blueprint("session", __name__, static_folder="static", template_folder="templates")


@session.route('/submit-session', methods=['GET', 'POST'])
def submit_session():
    if request.method == 'POST':
        data = request.json
        session_kicks = data['session_kicks']
        session_date = data['sessionDate']
        print(data)
        print(session_kicks)
        print(session_date)

        kicks_data = data['kicksData']
        distances = []
        locationsOnField = []
        xs = []
        ys = []
        precision_scores = []
        distance_scores = []

        for kick in kicks_data:
            distances.append(kick['distance'])
            locationsOnField.append(kick['location'])
            x = int(float(kick['inputX']))
            y = int(float(kick['inputY']))

            precision_score = (x - 300) / (233) * 10
            distance_score = -(y - 440) / (300) * 10

            print(precision_score)
            print(distance_score)
            
            xs.append(x)
            ys.append(y)
            precision_scores.append(precision_score)
            distance_scores.append(distance_score)

            
            kicks = []

        

        return jsonify({"status": "success", "message": "Data received"}), 200
