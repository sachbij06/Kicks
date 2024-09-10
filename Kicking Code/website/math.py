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

for i in range(len(list_of_week_files)):

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

        
      combined_college_left_hash_made += len(week_college_left_hash_made)
      combined_college_left_hash_attempted += (len(week_college_left_hash_made) + len(week_college_left_hash_missed))


      week_right_hash_ratio = f"{len(week_college_right_hash_made)}/{(len(week_college_right_hash_made) + len(week_college_right_hash_missed))}"
      if (len(week_college_right_hash_made) + len(week_college_right_hash_missed)) != 0:
        week_right_hash_pct = len(week_college_right_hash_made) / (len(week_college_right_hash_made) + len(week_college_right_hash_missed)) * 100

        
      combined_college_right_hash_made += len(week_college_right_hash_made)
      combined_college_right_hash_attempted += (len(week_college_right_hash_made) + len(week_college_right_hash_missed))


      week_middle_ratio = f"{len(week_middle_made)}/{(len(week_middle_made) + len(week_middle_missed))}"
      if (len(week_middle_made) + len(week_middle_missed)) != 0:
        week_middle_pct = len(week_middle_made) / (len(week_middle_made) + len(week_middle_missed)) * 100
        
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



      week_fg_30_39_made = specific_week_data['fg30_39_made']
      week_fg_30_39_missed = specific_week_data['fg30_39_missed']
      
      combined_fg_30_39_made_count += len(week_fg_30_39_made)
      combined_fg_30_39_attempted_count += (len(week_fg_30_39_made) + len(week_fg_30_39_missed))
      week_fg30_39_make_ratio = f"{len(week_fg_30_39_made)}/{(len(week_fg_30_39_made) + len(week_fg_30_39_missed))}"

      if (len(week_fg_30_39_made) + len(week_fg_30_39_missed)) != 0:
        week_fg30_39_pct = len(week_fg_30_39_made) / (len(week_fg_30_39_made) + len(week_fg_30_39_missed)) * 100


      week_fg_40_49_made = specific_week_data['fg40_49_made']
      week_fg_40_49_missed = specific_week_data['fg40_49_missed']

      combined_fg_40_49_made_count += len(week_fg_40_49_made)
      combined_fg_40_49_attempted_count += (len(week_fg_40_49_made) + len(week_fg_40_49_missed))
      week_fg40_49_make_ratio = f"{len(week_fg_40_49_made)}/{(len(week_fg_40_49_made) + len(week_fg_40_49_missed))}"

      if (len(week_fg_40_49_made) + len(week_fg_40_49_missed)) != 0:
        week_fg40_49_pct = len(week_fg_40_49_made) / (len(week_fg_40_49_made) + len(week_fg_40_49_missed)) * 100


      week_fg_50_plus_made = specific_week_data['fg50_plus_made']
      week_fg_50_plus_missed = specific_week_data['fg50_plus_missed']

      combined_fg_50_plus_made_count += len(week_fg_50_plus_made)
      combined_fg_50_plus_attempted_count += (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed))
      week_fg50_plus_make_ratio = f"{len(week_fg_50_plus_made)}/{(len(week_fg_50_plus_made) + len(week_fg_50_plus_missed))}"

      if (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed)) != 0:
        week_fg50_plus_pct = len(week_fg_50_plus_made) / (len(week_fg_50_plus_made) + len(week_fg_50_plus_missed)) * 100


    combined_ratio = (f"{combined_makes}/{combined_attempts}")
    combined_pct_made = combined_makes / combined_attempts * 100


    combined_left_hash_ratio = (f"{combined_college_left_hash_made}/{combined_college_left_hash_attempted}")
    combined_left_hash_pct = combined_college_left_hash_made / combined_college_left_hash_attempted * 100

    combined_right_hash_ratio = (f"{combined_college_right_hash_made}/{combined_college_right_hash_attempted}")
    combined_right_hash_pct = combined_college_right_hash_made / combined_college_right_hash_attempted * 100

    combined_middle_ratio = (f"{combined_middle_made}/{combined_middle_attempted}")
    combined_middle_pct = combined_middle_made / combined_middle_attempted * 100