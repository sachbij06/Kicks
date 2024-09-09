from flask import Flask, request, render_template, Blueprint
import _data

import matplotlib.patches as patches
import matplotlib.pyplot as plt


app = Flask(__name__)
visualize = Blueprint("visualize", __name__, static_folder="static", template_folder="templates")


@visualize.route('/')
def render():
  return render_template('visualize.html')


@visualize.route('/submit', methods=['GET', 'POST'])
def submit_form():
  if request.method == 'POST':

    visual_choice = request.form['visual_choice']

    attempts = _data.get_all_data()

    sum_of_precision_scores = 0
    visualized_total_attempts = len(attempts)
    visualized_total_makes = 0
    sum_of_abs_value = 0


    if visual_choice == "1":
      for attempt in attempts:
        sum_of_precision_scores += (attempt[5][0])
        sum_of_abs_value += abs(attempt[5][0])

        if attempt[4] == 'make':
          visualized_total_makes += 1
  

    elif visual_choice == "2":
        visualized_total_attempts = 0
        for attempt in attempts:

          if attempt[1] == "College Left Hash":
              sum_of_precision_scores += (attempt[5][0])
              sum_of_abs_value += abs(attempt[5][0])
              
              visualized_total_attempts += 1

          
              if attempt[4] == 'make':
                visualized_total_makes += 1

          if attempt[1] == "Left Middle":
              sum_of_precision_scores += (attempt[5][0])
              sum_of_abs_value += abs(attempt[5][0])
              
              visualized_total_attempts += 1

          
              if attempt[4] == 'make':
                visualized_total_makes += 1


    elif visual_choice == "3":

      visualized_total_attempts = 0
      for attempt in attempts:
        
        if attempt[1] == "Middle":

          sum_of_precision_scores += (attempt[5][0])
          sum_of_abs_value += abs(attempt[5][0])

          visualized_total_attempts += 1

          if attempt[4] == 'make':
            visualized_total_makes += 1


    elif visual_choice == "4":
      visualized_total_attempts = 0
      for attempt in attempts:
        
        if attempt[1] == "College Right Hash":
          sum_of_precision_scores += (attempt[5][0])
          sum_of_abs_value += abs(attempt[5][0])

          visualized_total_attempts += 1

          
          if attempt[4] == 'make':
            visualized_total_makes += 1


        if attempt[1] == "Right Middle":
              sum_of_precision_scores += (attempt[5][0])
              sum_of_abs_value += abs(attempt[5][0])
              
              visualized_total_attempts += 1

          
              if attempt[4] == 'make':
                visualized_total_makes += 1


    visualized_pct_made = visualized_total_makes / visualized_total_attempts * 100
    visualized_directional = sum_of_precision_scores / visualized_total_attempts
    visualized_deviation_from_middle = sum_of_abs_value / visualized_total_attempts
    

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.axis('off') # Turns off the x and y axes
    
    ax.text(3, 70, f"FG: {visualized_total_makes}/{visualized_total_attempts}\n% Made: {visualized_pct_made:.2f}%\nAverage Deviation from Middle: ±{visualized_deviation_from_middle:.2f}\nDirectional: {visualized_directional:.2f}", fontsize = 12, color = 'white' )
    
    # Plot the field
    ax.add_patch(patches.Rectangle((0, 0), 53.3, 60, facecolor='mediumseagreen')) # Adds a green rectangle for the field
    
    # Plot the end zone 
    ax.add_patch(patches.Rectangle((0, 50), 53.3, 10, facecolor='seagreen')) # Adds a green rectangle for the end zone
    ax.add_patch(patches.Rectangle((0, 60), 53.3, 70, facecolor='black')) # Adds a black rectangle as background
    
    # Plot the goal posts
    ax.plot([26.65, 26.65], [71, 60], color='yellow', linewidth=3) # Base goalpost
    ax.plot([20, 20], [101, 71], color='yellow', linewidth=3) # Left upright
    ax.plot([33.3, 33.3], [101, 71], color='yellow', linewidth=3) # Right upright
    
    ax.plot([21.33, 21.33], [101, 71], color='orange', linewidth=3) # Left College upright
    ax.plot([31.97, 31.97], [101, 71], color='orange', linewidth=3) # Right College upright
    
    # Plot the crossbar
    ax.plot([20, 33.3], [71, 71], color='yellow', linewidth=3) 
    
    
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
    ax.plot([17.75, 17.75], [0, 50], color='orange', linewidth=1, alpha = 0.75) # College Left Hash
    
      # Left hash marks
    for yard_line in range(50, 0, -1):
      ax.plot([12, 14.65], [yard_line, yard_line], color='white', linewidth=0.25)
    
      # Right Hash Mark
    ax.plot([39.975, 39.975], [0, 50], color='white', linewidth=1) # HS Right Hash
    ax.plot([35.55, 35.55], [0, 50], color='orange', linewidth=1, alpha = 0.75) # College Right Hash
    
      # Right hash marks
    for yard_line in range(50, 0, -1):
      ax.plot([38.65, 41.3], [yard_line, yard_line], color='white', linewidth=0.25)

    
    for attempt in attempts:
      xLocationOnField = 0 #xLocationOnField initialization
      xForFieldGoal = 0 #xForFieldGoal initialization
      
      yForFieldGoal = 71 + (attempt[5][1] * 3)
      distance = attempt[0]
      yPositionOnField = 60 - distance #convert distance to y-axis position

      plotcolor = "white"
      linestyle = ''
      linewidth = 1
      

      if visual_choice == "1":

        if attempt[1] == 'College Left Hash':
          xLocationOnField = 17.75
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)


        elif attempt[1] == 'Left Middle':
          xLocationOnField = 22.2
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)


        elif attempt[1] == 'Middle':
          xLocationOnField = 26.65
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)

        
        elif attempt[1] == 'Right Middle':
          xLocationOnField = 31.1
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)


        elif attempt[1] == 'College Right Hash':
          xLocationOnField = 35.55
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)
          
      
      elif visual_choice == "2":

        if attempt[1] == 'College Left Hash':
          xLocationOnField = 17.75

          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)

        elif attempt[1] == 'Left Middle':
          xLocationOnField = 22.2
          
          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)

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

        elif attempt[1] == 'College Right Hash':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0


      elif visual_choice == "3":

        if attempt[1] == 'College Left Hash':
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

          if attempt[5][0] == 0:
            xForFieldGoal = 26.65

          elif attempt[5][0] != 0:
            xForFieldGoal = 26.65 + (attempt[5][0] * .665)

        elif attempt[1] == 'Right Middle':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0

        elif attempt[1] == 'College Right Hash':
          xLocationOnField = 0
          xForFieldGoal = 0
          yForFieldGoal = 0
          yPositionOnField = 0


      elif visual_choice == "4":
          
          if attempt[1] == 'College Left Hash':
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
          
            if attempt[5][0] == 0:
              xForFieldGoal = 26.65

            elif attempt[5][0] != 0:
              xForFieldGoal = 26.65 + (attempt[5][0] * .665)

          elif attempt[1] == 'College Right Hash':
              xLocationOnField = 35.55

              if attempt[5][0] == 0:
                xForFieldGoal = 26.65

              elif attempt[5][0] != 0:
                xForFieldGoal = 26.65 + (attempt[5][0] * .665)

      

      if attempt[4] == 'make':
        plotcolor = 'green'
        linestyle = 'solid'
        linewidth = 0.75
        
      elif attempt[4] == 'miss':
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
  
