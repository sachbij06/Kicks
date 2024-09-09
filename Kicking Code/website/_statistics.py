from flask import Flask, request, render_template, Blueprint

import json, math, _data
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
stats = Blueprint("stats", __name__, static_folder="static", template_folder="templates")


@stats.route('/show')
def show_results():
  
  attempts = _data.get_all_data()

  left_hash_made = []
  left_middle_made = []
  right_hash_made = []
  right_middle_made = []
  middle_made = []

  left_hash_missed = []
  left_middle_missed = []
  right_hash_missed = []
  right_middle_missed = []
  middle_missed = []

  total_attempts = len(attempts)
  total_makes = 0

  avg_abs_value = 0
  aggregate_precision_scores = 0

  left_hash_precision_score = 0
  left_aggregate_precision_scores = 0

  left_middle_precision_score = 0
  left_middle_aggregate_precision_scores = 0

  right_hash_precision_score = 0
  right_aggregate_precision_scores = 0

  right_middle_precision_score = 0
  right_middle_aggregate_precision_scores = 0

  middle_precision_score = 0
  middle_aggregate_precision_scores = 0
  total_euclidean_distance = 0


  for fg in made_field_goals:

    if fg[1] == 'College Left Hash':
      left_hash_made.append(fg)

    if fg[1] == 'Left Middle':
      left_middle_made.append(fg)

    elif fg[1] == 'College Right Hash':
      right_hash_made.append(fg)

    if fg[1] == 'Right Middle':
      right_middle_made.append(fg)

    elif fg[1] == 'Middle':
      middle_made.append(fg)

  for fg in missed_field_goals:

    if fg[1] == 'College Left Hash':
      left_hash_missed.append(fg)

    if fg[1] == 'Left Middle':
      left_middle_missed.append(fg)

    elif fg[1] == 'College Right Hash':
      right_hash_missed.append(fg)

    if fg[1] == 'Right Middle':
      right_middle_missed.append(fg)

    elif fg[1] == 'Middle':
      middle_missed.append(fg)
      

  for attempt in attempts:
    avg_abs_value += abs(attempt[5][0])
    aggregate_precision_scores += (attempt[5][0])
    total_euclidean_distance += math.sqrt((abs(abs(attempt[5][0]) - 0) * abs(abs(attempt[5][0]) - 0)) + (abs(abs(attempt[5][1]) - 10) * abs(abs(attempt[5][1]) - 10)))
    
    
    if attempt[1] == 'College Right Hash':
      right_hash_precision_score += abs(attempt[5][0])
      right_aggregate_precision_scores += (attempt[5][0])

    elif attempt[1] == 'Right Middle':
      right_middle_precision_score += abs(attempt[5][0])
      right_middle_aggregate_precision_scores += (attempt[5][0])

    elif attempt[1] == 'College Left Hash':
      left_hash_precision_score += abs(attempt[5][0])
      left_aggregate_precision_scores += (attempt[5][0])

    elif attempt[1] == 'Left Middle':
      left_middle_precision_score += abs(attempt[5][0])
      left_middle_aggregate_precision_scores += (attempt[5][0])
    
    elif attempt[1] == 'Middle':
      middle_precision_score += abs(attempt[5][0])
      middle_aggregate_precision_scores += (attempt[5][0])
      
      
    if attempt[4] == 'make':
      total_makes += 1

  # general stats
  avg_euclidean_distance = total_euclidean_distance / total_attempts
  average_precision_score = avg_abs_value / total_attempts
  average_to_find_preferred_side = aggregate_precision_scores / total_attempts

  pct_made = total_makes / total_attempts * 100
  make_ratio = f"{total_makes}/{total_attempts}"


  # right hash stats
  right_hash_average_precision_score = right_hash_precision_score / (len(right_hash_made) + len(right_hash_missed))
  right_average_to_find_preferred_side = right_aggregate_precision_scores / (len(right_hash_made) + len(right_hash_missed))

  right_hash_ratio = f"{len(right_hash_made)}/{(len(right_hash_made) + len(right_hash_missed))}"
  if (len(right_hash_made) + len(right_hash_missed)) != 0:
    right_hash_pct = len(right_hash_made) / (len(right_hash_made) + len(right_hash_missed)) * 100


  # right middle stats
  right_middle_average_precision_score = right_middle_precision_score / (len(right_middle_made) + len(right_middle_missed))
  right_middle_average_to_find_preferred_side = right_middle_aggregate_precision_scores / (len(right_middle_made) + len(right_middle_missed))

  right_middle_ratio = f"{len(right_middle_made)}/{(len(right_middle_made) + len(right_middle_missed))}"
  if (len(right_middle_made) + len(right_middle_missed)) != 0:
    right_middle_pct = len(right_middle_made) / (len(right_middle_made) + len(right_middle_missed)) * 100


  # left hash stats
  left_hash_average_precision_score = left_hash_precision_score /  (len(left_hash_made) + len(left_hash_missed))
  left_average_to_find_preferred_side = left_aggregate_precision_scores /  (len(left_hash_made) + len(left_hash_missed))

  left_hash_ratio = f"{len(left_hash_made)}/{(len(left_hash_made) + len(left_hash_missed))}"
  if (len(left_hash_made) + len(left_hash_missed)) != 0:
    left_hash_pct = len(left_hash_made) / (len(left_hash_made) + len(left_hash_missed)) * 100

  # left middle stats
  left_middle_average_precision_score = left_middle_precision_score / (len(left_middle_made) + len(left_middle_missed))
  left_middle_average_to_find_preferred_side = left_middle_aggregate_precision_scores / (len(left_middle_made) + len(left_middle_missed))

  left_middle_ratio = f"{len(left_middle_made)}/{(len(left_middle_made) + len(left_middle_missed))}"
  if (len(left_middle_made) + len(left_middle_missed)) != 0:
    left_middle_pct = len(left_middle_made) / (len(left_middle_made) + len(left_middle_missed)) * 100

  # middle stats
  middle_average_precision_score = middle_precision_score / (len(middle_made) + len(middle_missed))
  middle_average_to_find_preferred_side = middle_aggregate_precision_scores / (len(middle_made) + len(middle_missed))

  middle_ratio = f"{len(middle_made)}/{(len(middle_made) + len(middle_missed))}"
  if (len(middle_made) + len(middle_missed)) != 0:
    middle_pct = len(middle_made) / (len(middle_made) + len(middle_missed)) * 100




  visual_choice = request.form['visual_choice']

  fig, ax = plt.subplots(figsize=(12, 6))
    
  ax.set_xlim(0, 100)
  ax.set_ylim(10, 120)
  
  #fill
  ax.fill_between([0, 120], 10, 120, color='green')


  #interp is what gives the depth perception from the slanted lines
  ax.plot([np.interp(10, [10, 100], [5, 25]), np.interp(100, [10, 100], [5, 25])], [10, 100], color='white', lw=1.5)  # Left sideline
  ax.plot([np.interp(10, [10, 100], [95, 75]), np.interp(100, [10, 100], [95, 75])], [10, 100], color='white', lw=1.5)  # Right sideline
  
  
  for y in range(20, 110, 10):  # 10 yard lines
      
      #initialization of start_x and end_x
      start_x = np.interp(y, [10, 100], [5, 25])
      end_x = np.interp(y, [10, 100], [95, 75])
      
      ax.plot([start_x, end_x], [y, y], color='white', lw=1)  #10 Yard Lines
      ax.plot([88.3, 11.7], [40, 40], color='white', lw=1.15)  #50 Yard Line
      ax.plot([91.5, 8.5], [25, 25], color='black', lw=0.5)  #35 Yard Line
      
      
      number_size = np.interp(y, [10, 9], [21, 17])
      if y != 50:  # Adjusted 50 yard line separately
          if y == 20:
              ax.text((start_x + 6), y, '30', color='white', fontsize=number_size, ha='left', va='center', rotation=-105)
              ax.text((end_x - 6), y, '30', color='white', fontsize=number_size, ha='right', va='center', rotation=105)
          elif y == 30:
              ax.text((start_x + 6), y, '40', color='white', fontsize=number_size, ha='left', va='center', rotation=-105)
              ax.text((end_x - 6), y, '40', color='white', fontsize=number_size, ha='right', va='center', rotation=105)
          elif y == 80:  
              ax.text((start_x + 6), y, '10', color='white', fontsize=number_size, ha='left', va='center', rotation=-105)
              ax.text((end_x - 6), y, '10', color='white', fontsize=number_size, ha='right', va='center', rotation=105)
          elif y == 90:
              ax.text((start_x + 6), y, '')
              ax.text((end_x - 6), y, '')
          elif y == 100:
              ax.text((start_x + 6), y, '')
              ax.text((end_x - 6), y, '')
          
          else:
              ax.text((start_x + 6), y, f'{90 - y}', color='white', fontsize=number_size, ha='left', va='center', rotation=-105)
              ax.text((end_x - 6), y, f'{90 - y}', color='white', fontsize=number_size, ha='right', va='center', rotation=105)
      else:
          ax.text((start_x + 6), y, '40', color='white', fontsize=number_size, ha='left', va='center', rotation=-105)
          ax.text((end_x - 6), y, '40', color='white', fontsize=number_size, ha='right', va='center', rotation=105)
          
      # Red dot at the line of KO
      new_50_y = 25
      center_x_50 = (np.interp(new_50_y, [10, 100], [5, 25]) + np.interp(new_50_y, [10, 100], [95, 75])) / 2
      ax.plot(center_x_50, new_50_y, 'ro', markersize=4)             
  
  for y in range(15, 95, 5):  #5 yard lines from 15 to 95
      if y % 10 != 0:
          if y != 25:
              start_x = np.interp(y, [10, 100], [5, 25])
              end_x = np.interp(y, [10, 100], [95, 75])
              ax.plot([start_x, end_x], [y, y], color='white', lw=0.5)         
          
  for y in range(10, 90, 1): #Left Hash ticks
      if y % 1 != 1:
          start_x = np.interp(y, [10, 100], [27, 37])
          end_x = np.interp(y, [10, 100], [29, 39])
          ax.plot([start_x, end_x], [y, y], color='white', lw=0.2)
          
  for y in range(10, 90, 1): #Right Hash ticks
      if y % 1 != 1:
          start_x = np.interp(y, [10, 100], [73, 63])
          end_x = np.interp(y, [10, 100], [71, 61])
          ax.plot([start_x, end_x], [y, y], color='white', lw=0.2)

  for y in [30, 50]:  #X's at 40 yard lines
      center_x_40 = (np.interp(y, [10, 100], [5, 25]) + np.interp(y, [10, 100], [95, 75])) / 2
      ax.text(center_x_40, y, 'X', color='white', fontsize=10, ha='center', va='center', fontweight='bold')
      
  

  # Set aspect of the plot and remove axes for better visual appeal
  ax.set_aspect('auto')
  ax.axis('off')


  print("hello")
  plt.plot()
  plt.savefig('Kicking Code/website/static/KO.png', format='png', bbox_inches='tight', pad_inches = -0.6, transparent=True, edgecolor='none')
  return render_template('stats.html', get_plot = True, plot_url='static/KO.png', attempts = attempts)
