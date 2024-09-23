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

    session_name = request.form.get('session_name', None)
    location_choice = request.form.get('location_choice', "1")
    distance_choice = request.form.get('distance_choice', "1")


    # Handles visualization for the specific session
    if session_name != "":
      with open('Kicking Code/website/static/session.json', 'r') as f:
        sessions_data = json.load(f)

      session = next((s for s in sessions_data if s['session'] == session_name), None)
      attempts = session['kicks']

        # Now, regardless of whether attempts are from a session or all data, we can proceed to apply filters

      # Initialize metrics
      sum_of_precision_scores = 0
      total_attempts = 0
      total_makes = 0
      sum_of_abs_value = 0
      sum_of_euclidean_distances = 0
      sum_of_heights = 0

        # Function to filter attempts based on the selected distance range
      def is_within_distance(attempt, distance_choice):
          distance = attempt[0]
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
              if location_choice == "1":
                  filtered_attempts.append(attempt)
              elif location_choice == "2" and attempt[1] in ["Left Hash", "Left Middle"]:
                  filtered_attempts.append(attempt)
              elif location_choice == "3" and attempt[1] == "Middle":
                  filtered_attempts.append(attempt)
              elif location_choice == "4" and attempt[1] in ["Right Hash", "Right Middle"]:
                  filtered_attempts.append(attempt)


      # Processing of filtered attempts >

      # Check if there are any filtered attempts 
      total_attempts = len(filtered_attempts)
      if total_attempts > 0: 
          
          for attempt in filtered_attempts:
              # Math for averages
              sum_of_precision_scores += attempt[4][0]   # Gets a total precision score (Directional) that you need to divide by total attempts
              sum_of_abs_value += abs(attempt[4][0])   # Gets a total precision score (Non-Directional) that you need to divide by total attempts
              sum_of_heights += attempt[4][1]   # Gets a total heigh score that you need to divide by total attempts

              if attempt[3] == 'make':
                  total_makes += 1

                # Math for Euclidean distance
              precision_score = attempt[4][0]
              distance_height_score = attempt[4][1]
              euclidean_distance = math.sqrt((precision_score - 0) ** 2 + (distance_height_score - 10) ** 2)   # Gets attempt-by-attempt euclidean distance
              sum_of_euclidean_distances += euclidean_distance   # Gets a total euclidean distance that you need to divide by total attempts

          # Calculate averages
          pct_made = total_makes / total_attempts * 100
          directional_bias = sum_of_precision_scores / total_attempts
          precision_deviation = sum_of_abs_value / total_attempts
          avg_height = sum_of_heights / total_attempts
          avg_euclidean_distance = sum_of_euclidean_distances / total_attempts

      else:
          # No attempts for selected filter; set 0's for values
          pct_made = 0
          directional_bias = 0
          precision_deviation = 0
          avg_euclidean_distance = None
          avg_height = 0



      # Plot Generation

      fig, ax = plt.subplots(figsize=(13, 10))
      plt.axis('off')
      
      if total_attempts > 0:
        ax.text(3, 70, f"FG: {pct_made:.2f}%  -  {total_makes}/{total_attempts}\n"
                      f"Precision: ±{precision_deviation:.2f}\n"
                      f"Average Height: {avg_height:.2f}\n"
                      f"Directional Bias: {directional_bias:.2f}\n"
                      f"Average Euclidean Distance: {avg_euclidean_distance:.2f}\n",
        fontsize=12, color='white')

      else:
        ax.text(3, 115, "No field goal attempts found for the selected filters.", fontsize=16, color='white')   # No attempts for selected filter

      # Field plot
      ax.add_patch(patches.Rectangle((0, -20), 53.3, 80, facecolor='mediumseagreen'))
    
      # Endzone plot
      ax.add_patch(patches.Rectangle((0, 50), 53.3, 10, facecolor='seagreen'))
      ax.add_patch(patches.Rectangle((0, 60), 53.3, 70, facecolor='black'))
      
      # Goal Post Plot
      ax.plot([26.65, 26.65], [71, 60], color='yellow', linewidth=3)  # Base goalpost
      ax.plot([20, 20], [101, 71], color='yellow', linewidth=3)  # Left upright
      ax.plot([33.3, 33.3], [101, 71], color='yellow', linewidth=3)  # Right upright
      ax.plot([21.33, 21.33], [101, 71], color='orange', linewidth=3)  # Left College upright
      ax.plot([31.97, 31.97], [101, 71], color='orange', linewidth=3)  # Right College upright
      ax.plot([20, 33.3], [71, 71], color='yellow', linewidth=3)  # Plot the crossbar 

      
      # Plot the yard lines and hash marks
      
        # 10 Yard lines
      for yard_line in range(60, -20, -10):
        ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=0.4)
      
        # Yard numbers
      for yard_line in range(0, 45, 10):
        ax.text(5, yard_line - 3.5, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Left
        ax.text(48.3, yard_line - 3.5, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Right
      
        # 5 Yard lines  
      for yard_line in range(45, -25, -5):
        ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=0.25)

        # Left Hash Line
      ax.plot([17.75, 17.75], [-30, 50], color='white', linewidth=0.6, alpha = 0.5) # Left Hash
      
        # Left Hash Marks
      for yard_line in range(50, -30, -1):
        ax.plot([16.425, 19.075], [yard_line, yard_line], color='white', linewidth=0.15)
      
        # Right Hash Line
      ax.plot([35.55, 35.55], [-30, 50], color='white', linewidth=0.6, alpha = 0.75) # Right Hash
      
        # Right Hash Marks
      for yard_line in range(50, -30, -1):
        ax.plot([34.225, 36.875], [yard_line, yard_line], color='white', linewidth=0.15)

      ax.text(5, -13.5, "40", ha = 'center', va = 'bottom', color = 'white') # Left
      ax.text(48.3, -13.5, "40", ha = 'center', va = 'bottom', color = 'white') # Right
      
      for attempt in filtered_attempts:

        if not is_within_distance(attempt, distance_choice):
          continue  # Skip if the attempt is not within the selected distance


          # Plot Variable initializations
        xLocationOnField = 0
        xForFieldGoal = 0
        yForFieldGoal = 71 + (attempt[4][1] * 3)

        distance = attempt[0]
        yPositionOnField = 60 - distance   # converts distance to y-axis position

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
      

        # Attempt circle on field
        ax.scatter(xLocationOnField, yPositionOnField, s = 50, color = plotcolor)
        
        # Attempt circle on field goal
        ax.scatter(xForFieldGoal, yForFieldGoal, s = 50, color = plotcolor)
      
        # Attempt line between field and field goal
        ax.plot([xLocationOnField, xForFieldGoal], [yPositionOnField, yForFieldGoal], color = plotcolor , linewidth = linewidth, linestyle = linestyle)


      ax.set_ylim(-30, 130)  # Adjust the lower limit as needed

        
      plt.plot()
      plt.savefig('Kicking Code/website/static/chart.png', format='png', bbox_inches='tight', pad_inches = -0.6, transparent=True, edgecolor='none')
      
      return render_template('visualize_session.html', get_plot = True, plot_url='static/chart.png', attempts = attempts)

    else:
        attempts = _data.get_all_data()

          # Initialize metrics
        sum_of_precision_scores = 0
        total_attempts = 0
        total_makes = 0
        sum_of_abs_value = 0
        sum_of_euclidean_distances = 0
        sum_of_heights = 0

          # Function to filter attempts based on the selected distance range
        def is_within_distance(attempt, distance_choice):
            distance = attempt[0]
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
                if location_choice == "1":
                    filtered_attempts.append(attempt)
                elif location_choice == "2" and attempt[1] in ["Left Hash", "Left Middle"]:
                    filtered_attempts.append(attempt)
                elif location_choice == "3" and attempt[1] == "Middle":
                    filtered_attempts.append(attempt)
                elif location_choice == "4" and attempt[1] in ["Right Hash", "Right Middle"]:
                    filtered_attempts.append(attempt)


        # Processing of filtered attempts >

        # Check if there are any filtered attempts 
        total_attempts = len(filtered_attempts)
        if total_attempts > 0: 
            
            for attempt in filtered_attempts:
                # Math for averages
                sum_of_precision_scores += attempt[4][0]   # Gets a total precision score (Directional) that you need to divide by total attempts
                sum_of_abs_value += abs(attempt[4][0])   # Gets a total precision score (Non-Directional) that you need to divide by total attempts
                sum_of_heights += attempt[4][1]   # Gets a total heigh score that you need to divide by total attempts

                if attempt[3] == 'make':
                    total_makes += 1

                  # Math for Euclidean distance
                precision_score = attempt[4][0]
                distance_height_score = attempt[4][1]
                euclidean_distance = math.sqrt((precision_score - 0) ** 2 + (distance_height_score - 10) ** 2)   # Gets attempt-by-attempt euclidean distance
                sum_of_euclidean_distances += euclidean_distance   # Gets a total euclidean distance that you need to divide by total attempts

            # Calculate averages
            pct_made = total_makes / total_attempts * 100
            directional_bias = sum_of_precision_scores / total_attempts
            precision_deviation = sum_of_abs_value / total_attempts
            avg_height = sum_of_heights / total_attempts
            avg_euclidean_distance = sum_of_euclidean_distances / total_attempts

        else:
            # No attempts for selected filter; set 0's for values
            pct_made = 0
            directional_bias = 0
            precision_deviation = 0
            avg_euclidean_distance = None
            avg_height = 0



        # Plot Generation

        fig, ax = plt.subplots(figsize=(11, 10))
        plt.axis('off')
      
        # Field plot
        ax.add_patch(patches.Rectangle((0, -20), 53.3, 80, facecolor='mediumseagreen'))
      
        # Endzone plot
        ax.add_patch(patches.Rectangle((0, 50), 53.3, 10, facecolor='seagreen'))
        ax.add_patch(patches.Rectangle((0, 60), 53.3, 70, facecolor='black'))
        
        # Goal Post Plot
        ax.plot([26.65, 26.65], [71, 60], color='yellow', linewidth=3)  # Base goalpost
        ax.plot([20, 20], [101, 71], color='yellow', linewidth=3)  # Left upright
        ax.plot([33.3, 33.3], [101, 71], color='yellow', linewidth=3)  # Right upright
        ax.plot([21.33, 21.33], [101, 71], color='orange', linewidth=3)  # Left College upright
        ax.plot([31.97, 31.97], [101, 71], color='orange', linewidth=3)  # Right College upright
        ax.plot([20, 33.3], [71, 71], color='yellow', linewidth=3)  # Plot the crossbar 

        
        # Plot the yard lines and hash marks
        
          # 10 Yard lines
        for yard_line in range(60, -20, -10):
          ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=0.4)
        
          # Yard numbers
        for yard_line in range(0, 45, 10):
          ax.text(5, yard_line - 3.5, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Left
          ax.text(48.3, yard_line - 3.5, str(50 - yard_line), ha = 'center', va = 'bottom', color = 'white') # Right
        
          # 5 Yard lines  
        for yard_line in range(45, -25, -5):
          ax.plot([0, 53.3], [yard_line, yard_line], color='white', linewidth=0.25)

          # Left Hash Line
        ax.plot([17.75, 17.75], [-30, 50], color='white', linewidth=0.6, alpha = 0.5) # Left Hash
        
          # Left Hash Marks
        for yard_line in range(50, -30, -1):
          ax.plot([16.425, 19.075], [yard_line, yard_line], color='white', linewidth=0.15)
        
          # Right Hash Line
        ax.plot([35.55, 35.55], [-30, 50], color='white', linewidth=0.6, alpha = 0.75) # Right Hash
        
          # Right Hash Marks
        for yard_line in range(50, -30, -1):
          ax.plot([34.225, 36.875], [yard_line, yard_line], color='white', linewidth=0.15)

        ax.text(5, -13.5, "40", ha = 'center', va = 'bottom', color = 'white') # Left
        ax.text(48.3, -13.5, "40", ha = 'center', va = 'bottom', color = 'white') # Right
        
        for attempt in filtered_attempts:

          if not is_within_distance(attempt, distance_choice):
            continue  # Skip if the attempt is not within the selected distance


            # Plot Variable initializations
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 71 + (attempt[4][1] * 3)

          distance = attempt[0]
          yPositionOnField = 60 - distance   # converts distance to y-axis position

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
        

          # Attempt circle on field
          ax.scatter(xLocationOnField, yPositionOnField, s = 50, color = plotcolor)
          
          # Attempt circle on field goal
          ax.scatter(xForFieldGoal, yForFieldGoal, s = 50, color = plotcolor)
        
          # Attempt line between field and field goal
          ax.plot([xLocationOnField, xForFieldGoal], [yPositionOnField, yForFieldGoal], color = plotcolor , linewidth = linewidth, linestyle = linestyle)


        ax.set_ylim(-30, 130)  # Adjust the lower limit as needed

          
        plt.plot()
        plt.savefig('Kicking Code/website/static/chart.png', format='png', bbox_inches='tight', pad_inches = -0.6, transparent=True, edgecolor='none')
        
        return render_template('visualize.html', get_plot = True, plot_url='static/chart.png', attempts = attempts)


  else:
      return render_template('visualize.html')
  
