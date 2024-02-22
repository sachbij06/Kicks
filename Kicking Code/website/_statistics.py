import datetime
import json
import os
import math
import _data

from flask import Flask, request, render_template


app = Flask(__name__)


# date logic for weekly charting

start_date = datetime.date(2024, 2, 5)
today = datetime.date.today()

attempts = _data.get_attempts()

day_diff = (today - start_date).days
current_week = (day_diff // 7 + 1)
current_day_of_week = (day_diff % 7) + 1


def show_results():
  if os.path.isfile(stats_file):

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
    else:
      right_hash_pct = "No kicks."


    # right middle stats
    right_middle_average_precision_score = right_middle_precision_score / (len(right_middle_made) + len(right_middle_missed))
    right_middle_average_to_find_preferred_side = right_middle_aggregate_precision_scores / (len(right_middle_made) + len(right_middle_missed))

    right_middle_ratio = f"{len(right_middle_made)}/{(len(right_middle_made) + len(right_middle_missed))}"
    if (len(right_middle_made) + len(right_middle_missed)) != 0:
      right_middle_pct = len(right_middle_made) / (len(right_middle_made) + len(right_middle_missed)) * 100
    else:
      right_middle_pct = "No kicks."


    # left hash stats
    left_hash_average_precision_score = left_hash_precision_score /  (len(left_hash_made) + len(left_hash_missed))
    left_average_to_find_preferred_side = left_aggregate_precision_scores /  (len(left_hash_made) + len(left_hash_missed))

    left_hash_ratio = f"{len(left_hash_made)}/{(len(left_hash_made) + len(left_hash_missed))}"
    if (len(left_hash_made) + len(left_hash_missed)) != 0:
      left_hash_pct = len(left_hash_made) / (len(left_hash_made) + len(left_hash_missed)) * 100
    else:
      left_hash_pct = "No kicks."

    # left middle stats
    left_middle_average_precision_score = left_middle_precision_score / (len(left_middle_made) + len(left_middle_missed))
    left_middle_average_to_find_preferred_side = left_middle_aggregate_precision_scores / (len(left_middle_made) + len(left_middle_missed))

    left_middle_ratio = f"{len(left_middle_made)}/{(len(left_middle_made) + len(left_middle_missed))}"
    if (len(left_middle_made) + len(left_middle_missed)) != 0:
      left_middle_pct = len(left_middle_made) / (len(left_middle_made) + len(left_middle_missed)) * 100
    else:
      left_middle_pct = "No kicks."


    # middle stats
    middle_average_precision_score = middle_precision_score / (len(middle_made) + len(middle_missed))
    middle_average_to_find_preferred_side = middle_aggregate_precision_scores / (len(middle_made) + len(middle_missed))

    middle_ratio = f"{len(middle_made)}/{(len(middle_made) + len(middle_missed))}"
    if (len(middle_made) + len(middle_missed)) != 0:
      middle_pct = len(middle_made) / (len(middle_made) + len(middle_missed)) * 100
    else:
      middle_pct = "No kicks."


    # fg 20 to 29 stats

    fg20_29_make_ratio = f"{len(fg20_29_made)}/{(len(fg20_29_made) + len(fg20_29_missed))}"
    if (len(fg20_29_made) + len(fg20_29_missed)) != 0:
      fg20_29_pct = len(fg20_29_made) / (len(fg20_29_made) + len(fg20_29_missed)) * 100
    else:
      fg20_29_pct = "No kicks."


    # fg 30 to 39 stats
      
    fg30_39_make_ratio = f"{len(fg30_39_made)}/{(len(fg30_39_made) + len(fg30_39_missed))}"
    if (len(fg30_39_made) + len(fg30_39_missed)) != 0:
      fg30_39_pct = len(fg30_39_made) / (len(fg30_39_made) + len(fg30_39_missed)) * 100
    else:
      fg30_39_pct = "No kicks."


    # fg 40 to 49 stats
      
    fg40_49_make_ratio = f"{len(fg40_49_made)}/{(len(fg40_49_made) + len(fg40_49_missed))}"
    if (len(fg40_49_made) + len(fg40_49_missed)) != 0:
      fg40_49_pct = len(fg40_49_made) / (len(fg40_49_made) + len(fg40_49_missed)) * 100
    else:
      fg40_49_pct = "No kicks."

    
    # fg 50+

    fg50_plus_make_ratio = f"{len(fg50_plus_made)}/{(len(fg50_plus_made) + len(fg50_plus_missed))}"
    if (len(fg50_plus_made) + len(fg50_plus_missed)) != 0:
      fg50_plus_pct = len(fg50_plus_made) / (len(fg50_plus_made) + len(fg50_plus_missed)) * 100
    else:
      fg50_plus_pct = "No kicks."


# printing statistics
      
    print("_" * 50)
    print(f"\nWeek {current_week} Results:")

    print("\n\033[3mFG:\033[0m")
    print(make_ratio)
    print(f"{pct_made:.2f}%")
    print(f"\n\nAverage Precision Score: {average_precision_score:.2f}")
    print(f"Favored Direction Per Attempt: {average_to_find_preferred_side:.2f}")
    print(f"Average Euclidean Distance: {avg_euclidean_distance:.2f}")

    print("\n\n\033[3mLocations:\033[0m")

    print(f"Left Hash:")
    print(f"{left_hash_ratio} - {left_hash_pct:.2f}%")
    print(f"Left Precision Score: {left_hash_average_precision_score:.2f}")
    print(f"Left Favored Direction: {left_average_to_find_preferred_side:.2f}")

    print(f"\nLeft Middle:")
    print(f"{left_middle_ratio} - {left_middle_pct:.2f}%")
    print(f"Left Middle Precision Score: {left_middle_average_precision_score:.2f}")
    print(f"Left Middle Favored Direction: {left_middle_average_to_find_preferred_side:.2f}")

    print(f"\nMiddle:")
    print(f"{middle_ratio} - {middle_pct:.2f}%")
    print(f"Middle Precision Score: {middle_average_precision_score:.2f}")
    print(f"Middle Favored Direction: {middle_average_to_find_preferred_side:.2f}")

    print(f"\nRight Middle:")
    print(f"{right_middle_ratio} - {right_middle_pct:.2f}%")
    print(f"Right Middle Precision Score: {right_middle_average_precision_score:.2f}")
    print(f"Right Middle Favored Direction: {right_middle_average_to_find_preferred_side:.2f}")

    print(f"\nRight Hash:")
    print(f"{right_hash_ratio} - {right_hash_pct:.2f}%")
    print(f"Right Precision Score: {right_hash_average_precision_score:.2f}")
    print(f"Right Favored Direction: {right_average_to_find_preferred_side:.2f}")

    print("\n\n\033[3mDistances:\033[0m")

    if fg20_29_pct == 'No kicks.':
      print(f"20-29: {fg20_29_pct}")
    else:
      print(f"20-29: {fg20_29_make_ratio} - {fg20_29_pct:.2f}%")

    if fg30_39_pct == 'No kicks.':
      print(f"30-39: {fg30_39_pct}")
    else:
      print(f"30-39: {fg30_39_make_ratio} - {fg30_39_pct:.2f}%")

    if fg40_49_pct == 'No kicks.':
      print(f"40-49: {fg40_49_pct}")
    else:
      print(f"40-49: {fg40_49_make_ratio} - {fg40_49_pct:.2f}%")

    if fg50_plus_pct == 'No kicks.':
      print(f"50+: {fg50_plus_pct}")
    else:
      print(f"50+: {fg50_plus_make_ratio} - {fg50_plus_pct:.2f}%")


    print("\n\nMissed Field Goals:")
    for fg in missed_field_goals:
      if len(fg) == 5:
        print(f"\n{fg[0]}, {fg[1]} \nYou {fg[4]}")
      else:
        print(f"\n{fg[0]}, {fg[1]}")

    print("_" * 50)

  else:
    print("\nYou have no statistics logged currently.")

# -------------------------- Combined Stats Initialization --------------------------

  combined_makes = 0
  combined_attempts = 0

  combined_college_left_hash_made = 0
  combined_college_left_hash_attempted = 0

  combined_middle_made = 0
  combined_middle_attempted = 0

  combined_college_right_hash_made = 0
  combined_college_right_hash_attempted = 0

  combined_fg_20_29_made_count = 0
  combined_fg_20_29_attempted_count = 0
  combined_fg_30_39_made_count = 0
  combined_fg_30_39_attempted_count = 0
  combined_fg_40_49_made_count = 0
  combined_fg_40_49_attempted_count = 0
  combined_fg_50_plus_made_count = 0
  combined_fg_50_plus_attempted_count = 0

  week_attempts = len(attempts)
  week_makes = 0
  week_aggregate_precision_scores = 0
  for attempt in attempts:
    week_aggregate_precision_scores += abs(attempt[5][0])
    if attempt[4] == 'make':
      week_makes += 1
        
  week_average_precision_score = week_aggregate_precision_scores / week_attempts
  combined_makes += week_makes
  combined_attempts += week_attempts
  week_make_ratio = f"{week_makes}/{week_attempts}"
  
  week_pct_made = week_makes / week_attempts * 100
  
  week_college_left_hash_made = []
  week_college_right_hash_made = []
  week_middle_made = []

  week_college_left_hash_missed = []
  week_college_right_hash_missed = []
  week_middle_missed = []
  

  compare_input = input("\nDo you want to see your week-by-week stats and your total stats? (y/n) > ")
  list_of_week_files = []

  if compare_input == "y":
    for file in os.listdir():
    
      if file.endswith("Stats.json"):
        list_of_week_files.append(file)

    print("\nHere is your comparison:")

    for i in range(len(list_of_week_files)):
      print("_" * 50)
      print(f'\nFG Stats from Week {i+1}')

      with open(list_of_week_files[i]) as f:

        specific_week_data = json.load(f)
        week_made_field_goals = specific_week_data['made_field_goals']
        week_missed_field_goals = specific_week_data['missed_field_goals']
    

# --------------------------------- General Stats ---------------------------------

        for fg in week_made_field_goals:
          if fg[1] == 'College Left Hash':
            week_college_left_hash_made.append(fg)

          elif fg[1] == 'College Right Hash':
            week_college_right_hash_made.append(fg)

          elif fg[1] == 'Middle':
            week_middle_made.append(fg)

        
        for fg in week_missed_field_goals:

          if fg[1] == 'College Left Hash':
            week_college_left_hash_missed.append(fg)

          elif fg[1] == 'College Right Hash':
            week_college_right_hash_missed.append(fg)

          elif fg[1] == 'Middle':
            week_middle_missed.append(fg)

# --------------------------------- Location Stats ---------------------------------

        week_left_hash_ratio = f"{len(week_college_left_hash_made)}/{(len(week_college_left_hash_made) + len(week_college_left_hash_missed))}"
        if (len(week_college_left_hash_made) + len(week_college_left_hash_missed)) != 0:
          week_left_hash_pct = len(week_college_left_hash_made) / (len(week_college_left_hash_made) + len(week_college_left_hash_missed)) * 100
        else:
          week_left_hash_pct = "No kicks."
          
        combined_college_left_hash_made += len(week_college_left_hash_made)
        combined_college_left_hash_attempted += (len(week_college_left_hash_made) + len(week_college_left_hash_missed))


        week_right_hash_ratio = f"{len(week_college_right_hash_made)}/{(len(week_college_right_hash_made) + len(week_college_right_hash_missed))}"
        if (len(week_college_right_hash_made) + len(week_college_right_hash_missed)) != 0:
          week_right_hash_pct = len(week_college_right_hash_made) / (len(week_college_right_hash_made) + len(week_college_right_hash_missed)) * 100
        else:
          week_right_hash_pct = "No kicks."
          
        combined_college_right_hash_made += len(week_college_right_hash_made)
        combined_college_right_hash_attempted += (len(week_college_right_hash_made) + len(week_college_right_hash_missed))


        week_middle_ratio = f"{len(week_middle_made)}/{(len(week_middle_made) + len(week_middle_missed))}"
        if (len(week_middle_made) + len(week_middle_missed)) != 0:
          week_middle_pct = len(week_middle_made) / (len(week_middle_made) + len(week_middle_missed)) * 100
        else:
          week_middle_pct = "No kicks."
          
        combined_middle_made += len(week_middle_made)
        combined_middle_attempted += (len(week_middle_made) + len(week_middle_missed))

        # --------------------------------- Distance Stats ---------------------------------
        
        week_fg_20_29_made = specific_week_data['fg20_29_made']
        week_fg_20_29_missed = specific_week_data['fg20_29_missed']

        combined_fg_20_29_made_count += len(week_fg_20_29_made)
        combined_fg_20_29_attempted_count += (len(week_fg_20_29_made) + len(week_fg_20_29_missed))
        week_fg20_29_make_ratio = f"{len(week_fg_20_29_made)}/{(len(week_fg_20_29_made) + len(week_fg_20_29_missed))}"

        if (len(week_fg_20_29_made) + len(week_fg_20_29_missed)) != 0:
          week_fg20_29_pct = len(week_fg_20_29_made) / (len(week_fg_20_29_made) + len(week_fg_20_29_missed)) * 100
        else:
          week_fg20_29_pct = "No kicks."


        week_fg_30_39_made = specific_week_data['fg30_39_made']
        week_fg_30_39_missed = specific_week_data['fg30_39_missed']
        
        combined_fg_30_39_made_count += len(week_fg_30_39_made)
        combined_fg_30_39_attempted_count += (len(week_fg_30_39_made) + len(week_fg_30_39_missed))
        week_fg30_39_make_ratio = f"{len(week_fg_30_39_made)}/{(len(week_fg_30_39_made) + len(week_fg_30_39_missed))}"

        if (len(week_fg_30_39_made) + len(week_fg_30_39_missed)) != 0:
          week_fg30_39_pct = len(week_fg_30_39_made) / (len(week_fg_30_39_made) + len(week_fg_30_39_missed)) * 100
        else:
          week_fg30_39_pct = "No kicks."


        week_fg_40_49_made = specific_week_data['fg40_49_made']
        week_fg_40_49_missed = specific_week_data['fg40_49_missed']

        combined_fg_40_49_made_count += len(week_fg_40_49_made)
        combined_fg_40_49_attempted_count += (len(week_fg_40_49_made) + len(week_fg_40_49_missed))
        week_fg40_49_make_ratio = f"{len(week_fg_40_49_made)}/{(len(week_fg_40_49_made) + len(week_fg_40_49_missed))}"

        if (len(week_fg_40_49_made) + len(week_fg_40_49_missed)) != 0:
          week_fg40_49_pct = len(week_fg_40_49_made) / (len(week_fg_40_49_made) + len(week_fg_40_49_missed)) * 100
        else:
          week_fg40_49_pct = "No kicks."


        week_fg_50_plus_made = specific_week_data['fg50_plus_made']
        week_fg_50_plus_missed = specific_week_data['fg50_plus_missed']

        combined_fg_50_plus_made_count += len(week_fg_50_plus_made)
        combined_fg_50_plus_attempted_count += (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed))
        week_fg50_plus_make_ratio = f"{len(week_fg_50_plus_made)}/{(len(week_fg_50_plus_made) + len(week_fg_50_plus_missed))}"

        if (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed)) != 0:
          week_fg50_plus_pct = len(week_fg_50_plus_made) / (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed)) * 100
        else:
          week_fg50_plus_pct = "No kicks."

# --------------------------------- Printed Stats ---------------------------------

        print('\nFG:')
        print(f'{week_make_ratio}')
        print(f"{week_pct_made:.2f}%")

        print("\n\033[3mLocations:\033[0m")
        print(f"College Left Hash: {week_left_hash_ratio} - {week_left_hash_pct:.2f}%")
        print(f"Middle: {week_middle_ratio} - {week_middle_pct:.2f}%")
        print(f"College Right Hash: {week_right_hash_ratio} - {week_right_hash_pct:.2f}")

        print("\n\n\033[3mDistances:\033[0m")


        if week_fg20_29_pct == 'No kicks.':
          print(f"20-29: {week_fg20_29_pct}")
        else:
          print(f"20-29: {week_fg20_29_make_ratio} - {week_fg20_29_pct:.2f}%")

        if week_fg30_39_pct == 'No kicks.':
          print(f"30-39: {week_fg30_39_pct}")
        else:
          print(f"30-39: {week_fg30_39_make_ratio} - {week_fg30_39_pct:.2f}%")

        if week_fg40_49_pct == 'No kicks.':
          print(f"40-49: {week_fg40_49_pct}")
        else:
          print(f"40-49: {week_fg40_49_make_ratio} - {week_fg40_49_pct:.2f}%")

        if week_fg50_plus_pct == 'No kicks.':
          print(f"50+: {week_fg50_plus_pct}")
        else:
          print(f"50+: {week_fg50_plus_make_ratio} - {week_fg50_plus_pct:.2f}%")
        

        print(f"\n\nTotal Average Precision Score: {week_average_precision_score:.2f}")

        print(f"\nMissed FG From Week {i+1}")

        for fg in week_missed_field_goals:
          print(f"{fg[0]}, {fg[1]}. This field goal had a precision score of {fg[5][0]:.2f} and a distance score of {fg[5][1]:.2f}.")

        print("_" * 50)

# --------------------------------- Printed Stats ---------------------------------

    combined_ratio = (f"{combined_makes}/{combined_attempts}")
    combined_pct_made = combined_makes / combined_attempts * 100


    combined_left_hash_ratio = (f"{combined_college_left_hash_made}/{combined_college_left_hash_attempted}")
    combined_left_hash_pct = combined_college_left_hash_made / combined_college_left_hash_attempted * 100

    combined_right_hash_ratio = (f"{combined_college_right_hash_made}/{combined_college_right_hash_attempted}")
    combined_right_hash_pct = combined_college_right_hash_made / combined_college_right_hash_attempted * 100

    combined_middle_ratio = (f"{combined_middle_made}/{combined_middle_attempted}")
    combined_middle_pct = combined_middle_made / combined_middle_attempted * 100


    combined_20_29_ratio = (f"{combined_fg_20_29_made_count}/{combined_fg_20_29_attempted_count}")
    combined_30_39_ratio = (f"{combined_fg_30_39_made_count}/{combined_fg_30_39_attempted_count}")
    combined_40_49_ratio = (f"{combined_fg_40_49_made_count}/{combined_fg_40_49_attempted_count}")
    combined_50_plus_ratio = (f"{combined_fg_50_plus_made_count}/{combined_fg_50_plus_attempted_count}")



    if combined_fg_20_29_attempted_count != 0:
      combined_20_29_pct = combined_fg_20_29_made_count / combined_fg_20_29_attempted_count * 100
    else:
      combined_20_29_pct = "No kicks."

    if combined_fg_30_39_attempted_count != 0:
      combined_30_39_pct = combined_fg_30_39_made_count / combined_fg_30_39_attempted_count * 100
    else:
      combined_30_39_pct = "No kicks."
    
    if combined_fg_40_49_attempted_count != 0:
      combined_40_49_pct = combined_fg_40_49_made_count / combined_fg_40_49_attempted_count * 100
    else:
      combined_40_49_pct = "No kicks."
      
    if combined_fg_50_plus_attempted_count != 0:
      combined_50_plus_pct = combined_fg_50_plus_made_count / combined_fg_50_plus_attempted_count * 100
    else:
      combined_50_plus_pct = "No kicks."


    print('\n\033[3mCombined FG:\033[0m')
    print(combined_ratio)
    print(f"{combined_pct_made:.2f}%")

    print("\n\033[3mCombined Locations:\033[0m")
    print(f"College Left Hash: {combined_left_hash_ratio} - {combined_left_hash_pct:.2f}%")
    print(f"Middle: {combined_middle_ratio} - {combined_middle_pct:.2f}%")
    print(f"College Right Hash: {combined_right_hash_ratio} - {combined_right_hash_pct:.2f}%")

    print("\n\n\033[3mDistances:\033[0m")
    if combined_20_29_pct == 'No kicks.':
      print(f"20-29: {combined_20_29_pct}")
    else:
      print(f"20-29: {combined_20_29_ratio}  -  {combined_20_29_pct:.2f}%")
    
    if combined_30_39_pct == 'No kicks.':
      print(f"30-39: {combined_30_39_pct}")
    else:
      print(f"30-39: {combined_30_39_ratio}  -  {combined_30_39_pct:.2f}%")
    
    if combined_40_49_pct == 'No kicks.':
      print(f"40-49: {combined_40_49_pct}")
    else:
      print(f"40-49: {combined_40_49_ratio}  -  {combined_40_49_pct:.2f}%")

    if combined_50_plus_pct == 'No kicks.':
      print(f"50+: {combined_50_plus_pct}")
    else:
      print(f"50+: {combined_50_plus_ratio}  -  {combined_50_plus_pct:.2f}%")

    print("_" * 50)

  else:
    print("")

