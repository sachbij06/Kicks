from flask import Flask, request, render_template, Blueprint
import _data, math
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import json  # Import json module to read session data

app = Flask(__name__)
visualize = Blueprint("visualize", __name__, static_folder="static", template_folder="templates")


@visualize.route('/visualize', methods=['GET', 'POST'])
def submit_form():
  if request.method == 'POST':
    # Check if 'session_index' is in the form data
    session_index = request.form.get('session_index', None)
    location_choice = request.form.get('location_choice', "1")
    distance_choice = request.form.get('distance_choice', "1")

    if session_index is not None:
        # Handle visualization for the specific session
        session_index = int(session_index)
        # Load the sessions data
        with open('Kicking Code/website/static/session.json', 'r') as f:
            sessions_data = json.load(f)
        # Get the specific session's kicks
        session = sessions_data[session_index]
        attempts = session['kicks']
    else:
        # Fetch all the attempts data
        attempts = _data.get_all_data()

    # Now, regardless of whether attempts are from a session or all data, we can proceed to apply filters

    # Initialize metrics
    sum_of_precision_scores = 0
    visualized_total_attempts = 0
    visualized_total_makes = 0
    sum_of_abs_value = 0
    sum_of_euclidean_distances = 0
    sum_of_heights = 0

    # Function to filter attempts based on the selected distance range
    def is_within_distance(attempt, distance_choice):
        distance = attempt[0]  # Assuming attempt[0] is the distance
        if distance_choice == "1":  # All Distances
            return True
        elif distance_choice == "2" and 20 <= distance <= 29:
            return True
        elif distance_choice == "3" and 30 <= distance <= 39:
            return True
        elif distance_choice == "4" and 40 <= distance <= 49:
            return True
        elif distance_choice == "5" and distance >= 50:
            return True
        return False

    # Filter attempts by both location and distance
    filtered_attempts = []
    for attempt in attempts:
        if is_within_distance(attempt, distance_choice):
            if location_choice == "1":  # All locations
                filtered_attempts.append(attempt)
            elif location_choice == "2" and attempt[1] in ["Left Hash", "Left Middle"]:
                filtered_attempts.append(attempt)
            elif location_choice == "3" and attempt[1] == "Middle":
                filtered_attempts.append(attempt)
            elif location_choice == "4" and attempt[1] in ["Right Hash", "Right Middle"]:
                filtered_attempts.append(attempt)

    # Now process the filtered_attempts

    # Check if there are any filtered attempts
    visualized_total_attempts = len(filtered_attempts)

    if visualized_total_attempts > 0:
        # Process filtered attempts
        for attempt in filtered_attempts:
            sum_of_precision_scores += attempt[4][0]
            sum_of_abs_value += abs(attempt[4][0])
            sum_of_heights += attempt[4][1]
            if attempt[3] == 'make':
                visualized_total_makes += 1

            # Calculate Euclidean distance for each attempt
            precision_score = attempt[4][0]  # x-coordinate
            distance_height_score = attempt[4][1]  # y-coordinate
            euclidean_distance = math.sqrt((precision_score - 0) ** 2 + (distance_height_score - 10) ** 2)
            sum_of_euclidean_distances += euclidean_distance
        avg_height = sum_of_heights / visualized_total_attempts
        # Calculate averages
        visualized_pct_made = visualized_total_makes / visualized_total_attempts * 100
        visualized_directional = sum_of_precision_scores / visualized_total_attempts
        visualized_deviation_from_middle = sum_of_abs_value / visualized_total_attempts
        avg_euclidean_distance = sum_of_euclidean_distances / visualized_total_attempts
    else:
        # No attempts found for the given filter; set default values
        visualized_pct_made = 0
        visualized_directional = 0
        visualized_deviation_from_middle = 0
        avg_euclidean_distance = None
        avg_height = 0

    # Proceed to generate the plot as before, using filtered_attempts

    # Plotting the stats only if there are filtered attempts
    fig, ax = plt.subplots(figsize=(15, 10))
    plt.axis('off')  # Turns off the x and y axes

    if visualized_total_attempts > 0:
        # Display basic stats with Euclidean distance
        ax.text(3, 70, f"FG: {visualized_pct_made:.2f}%  -  {visualized_total_makes}/{visualized_total_attempts}\n"
                        f"Precision: ±{visualized_deviation_from_middle:.2f}\n"
                        f"Average Height: {avg_height:.2f}\n"
                        f"Directional Bias: {visualized_directional:.2f}\n"
                        f"Average Euclidean Distance: {avg_euclidean_distance:.2f}\n",
                fontsize=12, color='white')
    else:
        # Display no data message
        ax.text(3, 115, "No field goal attempts found for the selected filters.", fontsize=16, color='white')

    # Plot the field
    ax.add_patch(patches.Rectangle((0, 0), 53.3, 60, facecolor='mediumseagreen')) # Adds a green rectangle for the field
   
    # Plot the end zone 
    ax.add_patch(patches.Rectangle((0, 50), 53.3, 10, facecolor='seagreen')) # Adds a green rectangle for the end zone
    ax.add_patch(patches.Rectangle((0, 60), 53.3, 70, facecolor='black')) # Adds a black rectangle as background
    
    # Plot the goal posts
    ax.plot([26.65, 26.65], [71, 60], color='yellow', linewidth=3)  # Base goalpost
    ax.plot([20, 20], [101, 71], color='yellow', linewidth=3)  # Left upright
    ax.plot([33.3, 33.3], [101, 71], color='yellow', linewidth=3)  # Right upright
    ax.plot([21.33, 21.33], [101, 71], color='orange', linewidth=3)  # Left College upright
    ax.plot([31.97, 31.97], [101, 71], color='orange', linewidth=3)  # Right College upright
    ax.plot([20, 33.3], [71, 71], color='yellow', linewidth=3)  # Plot the crossbar 

    
    # Plot the yard lines and hash marks
    
      # 10 Yard lines
    for yard_line in range(60, 0, -10):
      ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=1)
    
      # Yard numbers
    for yard_line in range(0, 55, 10):
      ax.text(5, yard_line - 3, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Left
      ax.text(48.3, yard_line - 3, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Right
    
      # 5 Yard lines  
    for yard_line in range(50, 0, -5):
      ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=0.5)

    
      # Left Hash Mark
    ax.plot([13.325, 13.325], [0, 50], color='white', linewidth=1) # HS Left Hash
    ax.plot([17.75, 17.75], [0, 50], color='orange', linewidth=1, alpha = 0.75) # Left Hash
    
      # Left hash marks
    for yard_line in range(50, 0, -1):
      ax.plot([12, 14.65], [yard_line, yard_line], color='white', linewidth=0.25)
    
      # Right Hash Mark
    ax.plot([39.975, 39.975], [0, 50], color='white', linewidth=1) # HS Right Hash
    ax.plot([35.55, 35.55], [0, 50], color='orange', linewidth=1, alpha = 0.75) # Right Hash
    
      # Right hash marks
    for yard_line in range(50, 0, -1):
      ax.plot([38.65, 41.3], [yard_line, yard_line], color='white', linewidth=0.25)

    
    for attempt in filtered_attempts:
      if not is_within_distance(attempt, distance_choice):
        continue  # Skip if the attempt is not within the selected distance
      xLocationOnField = 0 #xLocationOnField initialization
      xForFieldGoal = 0 #xForFieldGoal initialization
      
      yForFieldGoal = 71 + (attempt[4][1] * 3)
      distance = attempt[0]
      yPositionOnField = 60 - distance #convert distance to y-axis position

      plotcolor = "white"
      linestyle = ''
      linewidth = 1
      

      if location_choice == "1":

        if attempt[1] == 'Left Hash':
          xLocationOnField = 17.75
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)


        elif attempt[1] == 'Left Middle':
          xLocationOnField = 22.2
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)


        elif attempt[1] == 'Middle':
          xLocationOnField = 26.65
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)

        
        elif attempt[1] == 'Right Middle':
          xLocationOnField = 31.1
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)


        elif attempt[1] == 'Right Hash':
          xLocationOnField = 35.55
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)    
      
      elif location_choice == "2":

        if attempt[1] == 'Left Hash':
          xLocationOnField = 17.75

          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)

        elif attempt[1] == 'Left Middle':
          xLocationOnField = 22.2
          
          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)

        elif attempt[1] == 'Middle':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'Right Middle':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'Right Hash':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

      elif location_choice == "3":

        if attempt[1] == 'Left Hash':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'Left Middle':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'Middle':
          xLocationOnField = 26.65

          if attempt[4][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[4][0] != 0:
            xForFieldGoal = 26.65 + (attempt[4][0] * .665)

        elif attempt[1] == 'Right Middle':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'Right Hash':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

      elif location_choice == "4":
          
          if attempt[1] == 'Left Hash':
              xLocationOnField = 0
              xForFieldGoal = 0
              yForFieldGoal = 0
              yPositionOnField = 0

          elif attempt[1] == 'Middle':
              xLocationOnField = 0
              xForFieldGoal = 0
              yForFieldGoal = 0
              yPositionOnField = 0

          elif attempt[1] == 'Left Middle':
            xLocationOnField = 0
            xForFieldGoal = 0
            yForFieldGoal = 0
            yPositionOnField = 0

          elif attempt[1] == 'Right Middle':
            xLocationOnField = 31.1
          
            if attempt[4][0] == 0:
              xForFieldGoal = 26.65

            elif attempt[4][0] != 0:
              xForFieldGoal = 26.65 + (attempt[4][0] * .665)

          elif attempt[1] == 'Right Hash':
              xLocationOnField = 35.55

              if attempt[4][0] == 0:
                xForFieldGoal = 26.65

              elif attempt[4][0] != 0:
                xForFieldGoal = 26.65 + (attempt[4][0] * .665)
      

      if attempt[3] == 'make':
        plotcolor = 'green'
        linestyle = 'solid'
        linewidth = 0.75
        
      elif attempt[3] == 'miss':
        plotcolor = 'red'
        linestyle = 'dotted'
        linewidth = 0.75
    

      # circle on field
      ax.scatter(xLocationOnField, yPositionOnField, s = 50, color = plotcolor)
      
      # circle on field goal
      ax.scatter(xForFieldGoal, yForFieldGoal, s = 50, color = plotcolor)
    
      # line between field and field goal
      ax.plot([xLocationOnField, xForFieldGoal], [yPositionOnField, yForFieldGoal], color = plotcolor , linewidth = linewidth, linestyle = linestyle)
    plt.plot()
    plt.savefig('Kicking Code/website/static/chart.png', format='png', bbox_inches='tight', pad_inches = -0.6, transparent=True, edgecolor='none')
    
    return render_template('visualize.html', get_plot = True, plot_url='static/chart.png', attempts = attempts)
    
  else:
      return render_template('visualize.html')
  
