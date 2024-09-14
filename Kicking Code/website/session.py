import json
from flask import Flask, request, jsonify, render_template, Blueprint

app = Flask(__name__)

session = Blueprint("session", __name__, static_folder="static", template_folder="templates")

# File path to store the session data in JSON
JSON_FILE_PATH = "kicking_data.json"




def write_to_json(data, filepath):
    """Write data to a JSON file, either appending or creating a new file."""
    try:
        with open(filepath, 'r+') as file:
            file_data = json.load(file)  # Load existing data
            file_data.append(data)       # Append the new data
            file.seek(0)                 # Move the file pointer to the beginning
            json.dump(file_data, file, indent=4)

    except FileNotFoundError:
        # If the file does not exist, create it and write the data

        with open(filepath, 'w') as file:
            json.dump([data], file, indent=4)





def calculate_session_stats(kicks_data):
    """Calculate session average precision, height, and FG% made."""
    total_precision = 0
    total_height = 0
    makes = 0
    total_attempts = len(kicks_data)

    for kick in kicks_data:
        precision = kick[4][0]
        height = kick[4][1]
        make_or_miss = kick[3]

        total_precision += abs(precision)
        total_height += height

        if make_or_miss == "make":
            makes += 1

    avg_precision = total_precision / total_attempts
    avg_height = total_height / total_attempts
    fg_percentage = (makes / total_attempts) * 100 if total_attempts > 0 else 0

    return avg_precision, avg_height, fg_percentage, total_attempts, makes




def write_session_summary(filepath):
    """Reads kicking data and writes a summary of each session."""
    try:
        with open(filepath, 'r') as file:
            kicks_data = json.load(file)

        all_session_results = []

        # Iterate through each session
        for i, session in enumerate(kicks_data):
            session_date = session[0][2]  # Assuming all kicks in a session share the same date
            avg_precision, avg_height, fg_percentage, total_attempts, makes = calculate_session_stats(session)

            # Create session summary with session number
            session_result = {
                "session": f"Session {i + 1}",
                "date": session_date,
                "avg_precision": avg_precision,
                "avg_height": avg_height,
                "fg_percentage": fg_percentage,
                "fg_attempts": total_attempts,
                "fg_makes": makes,
                "kicks": session
            }

            all_session_results.append(session_result)

         # Write the session summary to session.json
        with open("Kicking Code/website/static/session.json", 'w') as outfile:
            json.dump(all_session_results, outfile, indent=4)

    except FileNotFoundError:
        print("JSON file not found.")

@session.route('/submit-session', methods=['POST'])
def submit_session():
    if request.method == 'POST':
        data = request.json
        session_kicks = data['session_kicks']
        session_date = data['sessionDate']

        kicks_data = data['kicksData']
        session_results = []  # To store the processed data for the session      

        # Process each kick and prepare the result structure
        for kick in kicks_data:
            distance = int(kick['distance'])
            location = kick['location']
            x = int(float(kick['inputX']))
            y = int(float(kick['inputY']))

            # Calculate precision and height (distance score)
            precision = ((x - 49.875) / 327.75) * 20 - 10
            height = (320.635 - y) / (213.76) * 10

            # Determine "make" or "miss"
            make_or_miss = "make" if -8 < precision < 8 and height > 0 else "miss"
            
            # Build the data structure for this kick
            kick_result = [
                distance,               # Distance in yards
                location,               # Location on the field
                session_date,           # Date of the session
                make_or_miss,           # "make" or "miss" based on conditions
                [precision, height]     # Precision and height (distance score)
            ]

            session_results.append(kick_result)

        # Write the session data to the kicking_data.json file
        write_to_json(session_results, JSON_FILE_PATH)

        # After writing the session data, categorize it into buckets
        categorize_kicks_into_buckets(JSON_FILE_PATH)

        # Generate session summary data for session.json
        write_session_summary(JSON_FILE_PATH)

        # Return a success message
        return jsonify({"status": "success", "message": "Data received and stored"}), 200


def categorize_kicks_into_buckets(filepath):
    """Read the JSON file and categorize kicks into buckets based on distance and make/miss."""
    try:
        with open(filepath, 'r') as file:
            kicks_data = json.load(file)
        
        # Define empty buckets
        buckets = {
            "fg20_29_made": [],
            "fg20_29_missed": [],
            "fg30_39_made": [],
            "fg30_39_missed": [],
            "fg40_49_made": [],
            "fg40_49_missed": [],
            "fg50_plus_made": [],
            "fg50_plus_missed": [],
            "attempts": [],
            "made_field_goals": [],
            "missed_field_goals": []
        }

        # Iterate through all kicks
        for session in kicks_data:
            for kick in session:
                distance = kick[0]
                make_or_miss = kick[3]

                # Add to attempts
                buckets["attempts"].append(kick)

                # Add to made or missed field goals
                if make_or_miss == "make":
                    buckets["made_field_goals"].append(kick)
                else:
                    buckets["missed_field_goals"].append(kick)

                # Categorize by distance range and make/miss
                if 20 <= distance <= 29:
                    if make_or_miss == "make":
                        buckets["fg20_29_made"].append(kick)
                    else:
                        buckets["fg20_29_missed"].append(kick)
                elif 30 <= distance <= 39:
                    if make_or_miss == "make":
                        buckets["fg30_39_made"].append(kick)
                    else:
                        buckets["fg30_39_missed"].append(kick)
                elif 40 <= distance <= 49:
                    if make_or_miss == "make":
                        buckets["fg40_49_made"].append(kick)
                    else:
                        buckets["fg40_49_missed"].append(kick)
                elif distance >= 50:
                    if make_or_miss == "make":
                        buckets["fg50_plus_made"].append(kick)
                    else:
                        buckets["fg50_plus_missed"].append(kick)

        # Optionally, write the categorized buckets to a new JSON file
        with open("categorized_kicks.json", 'w') as outfile:
            json.dump(buckets, outfile, indent=4)

    except FileNotFoundError:
        print("JSON file not found.")
