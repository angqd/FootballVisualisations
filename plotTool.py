import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from matplotlib.patches import FancyArrowPatch
import seaborn as sns


#PASS PLOTS 

# Function to plot pass map with different colors for different pass lengths
def plot_prog_pass_map(pass_dataframe,progressive_pass_counts_df, color_map, player_name, ):
    """
    Plots a football pitch with arrows representing passes from the given DataFrame.
    Different pass lengths are color-coded. A small circle is plotted at the source of each pass.
    The player's name is displayed at the top of the plot along with progressive pass count and completion percentage.

    Parameters:
    - pass_dataframe (pd.DataFrame): DataFrame containing pass events with 'location', 'pass_end_location', 'period', 'pass_outcome', and 'pass_length' columns.
    - color_map (dict): Dictionary with color mappings for different pass lengths.
    - player_name (str): Name of the player whose passes are being plotted.
    - progressive_pass_counts_df (pd.DataFrame): DataFrame containing progressive pass counts and completion percentages for players.
    """

    # Get the player's progressive pass stats from the DataFrame
    player_stats = progressive_pass_counts_df[progressive_pass_counts_df['player_name'] == player_name].iloc[0]
    progressive_pass_count = player_stats['progressive_pass_count']
    completion_percentage = player_stats['completion_percentage']

    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create a football pitch
    pitch = Pitch(pitch_type='statsbomb', line_color='black')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot the passes
    for i, row in pass_dataframe.iterrows():
        start_location = row['location']
        end_location = row['pass_end_location']
        period = row['period']
        pass_outcome = row['pass_outcome']
        pass_length = row['pass_length']
        
        # Check if start_location and end_location are valid lists with no NaN values
        if isinstance(start_location, list) and isinstance(end_location, list):
            if len(start_location) == 2 and len(end_location) == 2:
                # Extract x and y coordinates
                start_x, start_y = start_location
                end_x, end_y = end_location
                
                # Determine the color based on pass length and outcome
                if pass_outcome == 'Incomplete':
                    continue  # Skip incomplete passes
                else:
                    if pass_length <= 5:
                        arrow_color = color_map['short']
                    elif 5 < pass_length <= 15:
                        arrow_color = color_map['medium']
                    else:
                        arrow_color = color_map['long']
                
                # Plot the arrow if all coordinates are valid
                if not (pd.isna(start_x) or pd.isna(start_y) or pd.isna(end_x) or pd.isna(end_y)):
                    # Use FancyArrowPatch for a more customizable arrow
                    arrow = FancyArrowPatch(
                        (start_x, start_y), (end_x, end_y),
                        color=arrow_color,
                        linewidth=2,  # Width of the arrow tail
                        arrowstyle="->,head_length=0.4,head_width=0.2",  # Arrowhead style
                        mutation_scale=15  # Scale of the arrowhead
                    )
                    ax.add_patch(arrow)
                    
                    # Plot a small circle at the source of the pass
                    pitch.scatter(start_x, start_y, s=30, color=arrow_color, ax=ax)

    # Add the player's name as the title
    ax.set_title(f"{player_name}'s Progressive Passes", fontsize=20)

    # Add text with progressive pass count and completion percentage
    ax.text(1, 10, f"Prog Pass Count: {progressive_pass_count}", fontsize=12, ha='left', va='center')
    ax.text(1, 5, f"Completion %: {completion_percentage:.2f}%", fontsize=12, ha='left', va='center')

    # Show the plot
    plt.show()


