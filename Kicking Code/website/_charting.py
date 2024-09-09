import _data

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def render():
  return render_template('charting.html')


@app.route('/submit_data', methods=['POST'])
def generate_field_goal():
  if request.method == 'POST':

    attempts = _data.get_all_data()
    print(attempts)

    session_kicks = int(request.form['sessionKicks'])
    session_date = request.form['sessionDate']
    print(f"{session_kicks}")
    print(session_date)
    kick_result = ''


    for i in range(1, session_kicks + 1):
      distance = int(request.form[f'distance'])
      locationOnField = request.form[f'locationOnField']
      x = int(request.form[f'footballY'])
      y = int(request.form[f'footballX'])
      attempts.append([distance, locationOnField, kick_result, session_date])
      
      precision_score = (x - 350) / (175) * 10
      distance_score = -(y - 440) / (300) * 10
      attempts.append([precision_score, distance_score])
   


    for attempt in attempts:
        
        if abs(attempt[5][0]) >= 8 or attempt[5][1] < 0:
          attempt[4] = 'miss'

          if 20 <= attempt[0] <= 29:
            if attempt not in fg20_29_missed:
              fg20_29_missed.append(attempt)
            if attempt not in missed_field_goals:
              missed_field_goals.append(attempt)
            
          elif 30 <= attempt[0] <= 39:
            if attempt not in fg30_39_missed:
              fg30_39_missed.append(attempt)
            if attempt not in missed_field_goals:
              missed_field_goals.append(attempt)
    
          elif 40 <= attempt[0] <= 49:
            if attempt not in fg40_49_missed:
              fg40_49_missed.append(attempt)
            if attempt not in missed_field_goals:
              missed_field_goals.append(attempt)
    
          elif attempt[0] >= 50:
            if attempt not in fg50_plus_missed:
              fg50_plus_missed.append(attempt)
            if attempt not in missed_field_goals:
              missed_field_goals.append(attempt)

        
        elif abs(attempt[5][0]) < 8 or attempt[5][1] > 0:
          attempt[4] = 'make'

          if 20 <= attempt[0] <= 29:
            if attempt not in fg20_29_made:
              fg20_29_made.append(attempt)
            if attempt not in made_field_goals:
              made_field_goals.append(attempt)
            
          elif 30 <= attempt[0] <= 39:
            if attempt not in fg30_39_made:
              fg30_39_made.append(attempt)
            if attempt not in made_field_goals:
              made_field_goals.append(attempt)

          elif 40 <= attempt[0] <= 49:
            if attempt not in fg40_49_made:
              fg40_49_made.append(attempt)
            if attempt not in made_field_goals:
              made_field_goals.append(attempt)

          elif attempt[0] >= 50:
            if attempt not in fg50_plus_made:
              fg50_plus_made.append(attempt)
            if attempt not in made_field_goals:
              made_field_goals.append(attempt)

    _data.set_data(attempts, fg20_29_made, fg20_29_missed, fg30_39_made, fg30_39_missed, fg40_49_made, fg40_49_missed, fg50_plus_made, fg50_plus_missed, made_field_goals, missed_field_goals)


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)