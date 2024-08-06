import pandas as pd
import numpy as np 
import mplsoccer as mpl 
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from statsbombpy import sb

#event manipulation functions are covered here 

#passing 


## classify if a specific pass is progressive or not 
def is_progressive(start_location, end_location):
    # Define the field boundaries
    own_half_end = 50  # The midpoint of the field

    # Calculate the distance moved closer to the opponent's goal
    distance_moved = end_location[0] - start_location[0]

    # Determine the criteria based on the location of the pass
    if start_location[0] < own_half_end and end_location[0] < own_half_end:
        # Both points in own half
        return distance_moved >= 30
    elif start_location[0] < own_half_end and end_location[0] >= own_half_end:
        # Points in different halves
        return distance_moved >= 15
    elif start_location[0] >= own_half_end:
        # Both points in opponent's half
        return distance_moved >= 10
    return False

## add label of nature of pass  in the events dataframe ( genetally progressive passing label )
def classify_passes(df):
    # Ensure the necessary columns are present
    required_columns = ['type', 'pass_end_location', 'location']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Create a new column 'pass_category'
    pass_categories = []

    for index, row in df.iterrows():
        if row['type'] == 'Pass':
            start_location = row['location']
            end_location = row['pass_end_location']

            if start_location and end_location:
                if end_location[0] > start_location[0]:
                    if is_progressive(start_location, end_location):
                        pass_categories.append('progressive')
                    else:
                        pass_categories.append('normal')
                else:
                    pass_categories.append('backwards')
            else:
                pass_categories.append('unknown')
        else:
            pass_categories.append('non_pass')

    df['pass_category'] = pass_categories
    return df